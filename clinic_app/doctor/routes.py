from flask import Blueprint, render_template, url_for, flash, redirect, request, abort, current_app, jsonify, send_file
from flask_login import login_required, current_user
from clinic_app import db
from clinic_app.models import User, Patient, Ticket, Visit, Prescription, DoctorSettings, Medication, PrescriptionMedication, PredefinedPrescription, PredefinedPrescriptionMedication, Appointment
from clinic_app.doctor.forms import VisitForm, PrescriptionForm, DoctorSettingsForm, MedicationForm, PredefinedPrescriptionForm, AppointmentForm
from clinic_app.secretary.forms import PatientFormFrench
from clinic_app.doctor.utils import generate_prescription_pdf
from datetime import datetime
import os
import calendar
from functools import wraps

# Création du blueprint pour le médecin
doctor = Blueprint("doctor", __name__)


def doctor_required(f):
    """S'assurer que l'utilisateur est un médecin"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.role != "doctor":
            flash("Vous n'êtes pas autorisé à accéder à cette page", "danger")
            return redirect(url_for("auth.login"))
        return f(*args, **kwargs)
    return decorated_function


@doctor.route("/dashboard")
@login_required
@doctor_required
def dashboard():
    """Tableau de bord du médecin"""
    # الحصول على قائمة الانتظار الحالية مرتبة حسب الأولوية
    today = datetime.now().date()
    waiting_tickets = Ticket.query.filter(
        db.func.date(Ticket.created_at) == today,
        Ticket.status == "waiting"
    ).order_by(
        Ticket.priority.desc(),  # الأولوية أولاً
        Ticket.number.asc()      # ثم الرقم
    ).all()

    # الحصول على المريض الحالي - الذي لديه تذكرة بحالة called
    current_ticket = Ticket.query.filter(
        db.func.date(Ticket.created_at) == today,
        Ticket.status == "called"
    ).first()
    current_patient = None

    if current_ticket:
        current_patient = Patient.query.get(current_ticket.patient_id)

    # حساب الإحصائيات اليومية
    today = datetime.now().date()
    
    # زيارات اليوم
    daily_visits = Visit.query.filter(
        Visit.doctor_id == current_user.id,
        db.func.date(Visit.date) == today
    ).all()
    
    # إيرادات اليوم
    daily_revenue = sum(visit.price or 0 for visit in daily_visits if visit.payment_status == "مدفوع")
    
    # المرضى الجدد اليوم
    new_patients_today = Patient.query.filter(
        db.func.date(Patient.created_at) == today
    ).count()
    
    # مواعيد اليوم
    today_appointments = Appointment.query.filter(
        Appointment.doctor_id == current_user.id,
        db.func.date(Appointment.appointment_date) == today
    ).all()
    
    # المواعيد القادمة (من الغد فما بعد)
    upcoming_appointments = Appointment.query.filter(
        Appointment.doctor_id == current_user.id,
        Appointment.appointment_date > datetime.now(),
        Appointment.status == "مجدول"
    ).count()
    
    daily_stats = {
        'visits_count': len(daily_visits),
        'revenue': daily_revenue,
        'new_patients': new_patients_today,
        'today_appointments': len(today_appointments),
        'upcoming_appointments': upcoming_appointments
    }

    return render_template(
        "doctor/dashboard.html",
        title="لوحة تحكم الطبيب",
        waiting_tickets=waiting_tickets,
        current_ticket=current_ticket,
        current_patient=current_patient,
        daily_stats=daily_stats
    )





@doctor.route("/doctor/next-patient")
@login_required
@doctor_required
def next_patient():
    """استدعاء المريض التالي"""
    # التأكد من إنهاء الحالة الحالية إذا كانت موجودة
    current_ticket = Ticket.query.filter_by(status="called").first()
    if current_ticket:
        # تغيير حالة التذكرة الحالية إلى مكتمل
        current_ticket.status = "done"
        db.session.commit()

    # الحصول على المريض التالي في قائمة الانتظار
    next_ticket = Ticket.query.filter_by(status="waiting").order_by(Ticket.number).first()

    if next_ticket:
        next_ticket.status = "called"
        db.session.commit()
        flash(f"Patient appelé: {next_ticket.patient.full_name}", "success")
    else:
        flash("Aucun patient en liste d'attente", "info")

    return redirect(url_for("doctor.dashboard"))


@doctor.route("/doctor/patient/<int:patient_id>", methods=["GET", "POST"])
@login_required
@doctor_required
def patient_visit(patient_id):
    """إنشاء زيارة جديدة للمريض"""
    patient = Patient.query.get_or_404(patient_id)
    
    # الحصول على سعر الزيارة الافتراضي من إعدادات الطبيب
    settings = DoctorSettings.query.filter_by(user_id=current_user.id).first()
    default_price = 100.0
    if settings:
        default_price = settings.default_visit_price
    
    form = VisitForm()
    if request.method == "GET":
        form.price.data = default_price

    if form.validate_on_submit():
        # إنشاء زيارة جديدة
        visit = Visit(
            patient_id=patient.id,
            doctor_id=current_user.id,
            symptoms=form.symptoms.data,
            diagnosis=form.diagnosis.data,
            treatment=form.treatment.data,
            notes=form.notes.data,
            status=form.status.data,
            price=form.price.data,
            payment_status=form.payment_status.data
        )

        db.session.add(visit)
        db.session.commit()

        # إنشاء موعد تلقائياً إذا كانت الحالة "suivi" وتم تحديد تاريخ الموعد
        if form.status.data == "suivi" and form.follow_up_date.data:
            appointment = Appointment(
                patient_id=patient.id,
                doctor_id=current_user.id,
                visit_id=visit.id,
                appointment_date=form.follow_up_date.data,
                notes=form.follow_up_notes.data or "موعد متابعة تلقائي",
                status="مجدول"
            )
            db.session.add(appointment)
            db.session.commit()
            
            flash(f"تم حفظ معلومات الزيارة وحجز موعد المتابعة بتاريخ {appointment.appointment_date.strftime('%Y-%m-%d %H:%M')}", "success")
        else:
            flash("تم حفظ معلومات الزيارة بنجاح", "success")
            
        return redirect(url_for("doctor.create_prescription", visit_id=visit.id))

    # الحصول على تاريخ الزيارات السابقة للمريض
    previous_visits = Visit.query.filter_by(patient_id=patient.id).order_by(Visit.date.desc()).all()

    return render_template(
        "doctor/patient_visit.html",
        title=f"زيارة المريض - {patient.full_name}",
        patient=patient,
        form=form,
        previous_visits=previous_visits
    )


@doctor.route("/doctor/medications", methods=["GET", "POST"])
@login_required
@doctor_required
def medications():
    from flask import request
    
    form = MedicationForm()
    if form.validate_on_submit():
        try:
            # التحقق من عدم وجود دواء بنفس الاسم والجرعة
            existing_medication = Medication.query.filter_by(
                name=form.name.data.strip(),
                dosage=form.dosage.data.strip()
            ).first()
            
            if existing_medication:
                flash(f'Le médicament "{form.name.data}" avec le dosage "{form.dosage.data}" existe déjà!', 'warning')
            else:
                medication = Medication(
                    name=form.name.data.strip(),
                    dosage=form.dosage.data.strip()
                )
                db.session.add(medication)
                db.session.commit()
                flash(f'Le médicament "{form.name.data}" a été ajouté avec succès!', 'success')
                return redirect(url_for('doctor.medications'))
        except Exception as e:
            db.session.rollback()
            flash('Erreur lors de l\'ajout du médicament. Veuillez réessayer.', 'error')
    
    # معاملات البحث والصفحات
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '', type=str)
    per_page = request.args.get('per_page', 50, type=int)  # عدد الأدوية في كل صفحة
    
    # التأكد من أن per_page في نطاق معقول
    if per_page not in [25, 50, 100, 200]:
        per_page = 50
    
    # بناء الاستعلام
    query = Medication.query
    
    # إضافة البحث إذا كان موجوداً
    if search:
        search_filter = f"%{search}%"
        query = query.filter(
            db.or_(
                Medication.name.like(search_filter),
                Medication.dosage.like(search_filter)
            )
        )
    
    # ترتيب الأدوية أبجدياً وتطبيق الـ pagination
    medications = query.order_by(Medication.name.asc()).paginate(
        page=page,
        per_page=per_page,
        error_out=False
    )
    
    return render_template(
        'doctor/medications.html', 
        title='Gestion des médicaments', 
        form=form, 
        medications=medications,
        search=search,
        per_page=per_page
    )


@doctor.route("/doctor/medication/<int:medication_id>/delete", methods=["POST"])
@login_required
@doctor_required
def delete_medication(medication_id):
    try:
        medication = Medication.query.get_or_404(medication_id)
        medication_name = medication.name
        medication_dosage = medication.dosage
        
        db.session.delete(medication)
        db.session.commit()
        
        flash(f'Le médicament "{medication_name}" ({medication_dosage or "Dosage non spécifié"}) a été supprimé avec succès!', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Erreur lors de la suppression du médicament. Veuillez réessayer.', 'error')
    
    return redirect(url_for('doctor.medications'))


# Routes القديمة محذوفة - تم استبدالها بـ API routes جديدة


@doctor.route("/doctor/prescription/<int:visit_id>", methods=["GET", "POST"])
@login_required
@doctor_required
def create_prescription(visit_id):
    """إنشاء وصفة طبية لزيارة"""
    visit = Visit.query.get_or_404(visit_id)

    # التأكد من أن الزيارة تنتمي إلى المريض الصحيح
    if visit.doctor_id != current_user.id:
        flash("غير مسموح لك بالوصول إلى هذه الزيارة", "danger")
        return redirect(url_for("doctor.dashboard"))

    form = PrescriptionForm()
    form.predefined_prescription.choices = [(0, 'اختر وصفة جاهزة')] + [(p.id, p.name) for p in PredefinedPrescription.query.all()]
    
    # Populate medication choices for each entry in the FieldList
    medication_choices = [(m.id, f"{m.name} ({m.dosage})") for m in Medication.query.all()]
    for entry in form.medications.entries:
        entry.form.medication_id.choices = medication_choices

    if request.method == 'POST':
        # التحقق من وجود أدوية في الطلب
        medications_data = []
        
        # التحقق من البيانات الجديدة (JSON format)
        medications_json = request.form.get('medications_data')
        if medications_json:
            try:
                import json
                medications_data = json.loads(medications_json)
            except:
                flash("خطأ في تنسيق بيانات الأدوية", "danger")
        else:
            # التحقق من التنسيق القديم للتوافق مع الإصدارات السابقة
            for key, value in request.form.items():
                if key.startswith('medications-') and key.endswith('-medication_id') and value:
                    index = key.split('-')[1]
                    instructions_key = f'medications-{index}-instructions'
                    quantity_key = f'medications-{index}-quantity'
                    instructions = request.form.get(instructions_key, '')
                    quantity = request.form.get(quantity_key, '')
                    if instructions:
                        medications_data.append({
                            'medication_id': int(value),
                            'instructions': instructions,
                            'quantity': quantity
                        })
        
        if not medications_data:
            flash("يجب إضافة دواء واحد على الأقل للوصفة", "danger")
        else:
            try:
                # إنشاء الوصفة
                prescription = Prescription(visit_id=visit.id)
                db.session.add(prescription)
                db.session.flush()  # للحصول على ID الوصفة
                
                # إضافة الأدوية
                for med_data in medications_data:
                    # التعامل مع التنسيق الجديد والقديم
                    medication_id = med_data.get('id') or med_data.get('medication_id')
                    instructions = med_data.get('instructions', '')
                    quantity = med_data.get('quantity', '')
                    
                    prescription_medication = PrescriptionMedication(
                        prescription_id=prescription.id,
                        medication_id=int(medication_id),
                        instructions=instructions,
                        quantity=quantity
                    )
                    db.session.add(prescription_medication)
                
                db.session.commit()
                
                # تحديث حالة التذكرة
                ticket = Ticket.query.filter_by(patient_id=visit.patient_id, status="called").first()
                if ticket:
                    ticket.status = "done"
                    db.session.commit()
                
                # إنشاء ملف PDF للوصفة
                try:
                    pdf_path = generate_prescription_pdf(prescription, visit)
                    prescription.pdf_file = pdf_path
                    db.session.commit()
                except Exception as pdf_error:
                    print(f"خطأ في إنشاء PDF: {pdf_error}")
                
                flash("تم إنشاء الوصفة الطبية بنجاح!", "success")
                
                # إعادة توجيه لصفحة عرض الزيارة
                return redirect(url_for("doctor.view_visit", visit_id=visit.id))
                
            except Exception as e:
                db.session.rollback()
                flash(f"حدث خطأ في إنشاء الوصفة: {str(e)}", "danger")

    medications = Medication.query.all()
    predefined_prescriptions = PredefinedPrescription.query.all()
    return render_template("doctor/create_prescription.html", 
                         title="إنشاء وصفة طبية", 
                         form=form, 
                         visit=visit, 
                         medications=medications,
                         predefined_prescriptions=predefined_prescriptions)


@doctor.route("/doctor/prescription/<int:prescription_id>/view")
@login_required
@doctor_required
def view_prescription(prescription_id):
    """عرض تفاصيل الوصفة الطبية"""
    prescription = Prescription.query.get_or_404(prescription_id)
    visit = prescription.visit
    
    # التأكد من أن الوصفة تنتمي للطبيب الحالي
    if visit.doctor_id != current_user.id:
        flash("غير مسموح لك بالوصول إلى هذه الوصفة", "danger")
        return redirect(url_for("doctor.dashboard"))
    
    return render_template("doctor/view_prescription.html", 
                         title="تفاصيل الوصفة الطبية",
                         prescription=prescription,
                         visit=visit)


@doctor.route("/doctor/prescription/<int:prescription_id>/print")
@login_required
@doctor_required
def print_prescription(prescription_id):
    """طباعة الوصفة الطبية"""
    prescription = Prescription.query.get_or_404(prescription_id)
    visit = prescription.visit
    
    # التأكد من أن الوصفة تنتمي للطبيب الحالي
    if visit.doctor_id != current_user.id:
        flash("غير مسموح لك بالوصول إلى هذه الوصفة", "danger")
        return redirect(url_for("doctor.dashboard"))
    
    try:
        # التحقق من وجود ملف PDF موجود مسبقاً
        if prescription.pdf_file:
            existing_path = os.path.join(current_app.root_path, prescription.pdf_file)
            if os.path.exists(existing_path):
                # استخدام الملف الموجود
                return send_file(existing_path, 
                               as_attachment=False, 
                               download_name=f"prescription_{prescription.id}.pdf",
                               mimetype='application/pdf')
        
        # إنشاء ملف PDF جديد فقط إذا لم يكن موجوداً
        pdf_path = generate_prescription_pdf(prescription, visit)
        
        # تحديث مسار الملف في قاعدة البيانات
        prescription.pdf_file = pdf_path
        db.session.commit()
        
        # إنشاء المسار الكامل للملف
        full_path = os.path.join(current_app.root_path, pdf_path)
        
        # التحقق من وجود الملف
        if os.path.exists(full_path):
            return send_file(full_path, 
                           as_attachment=False, 
                           download_name=f"prescription_{prescription.id}.pdf",
                           mimetype='application/pdf')
        else:
            flash("لم يتم العثور على ملف الوصفة", "danger")
            return redirect(url_for("doctor.view_visit", visit_id=visit.id))
        
    except Exception as e:
        flash(f"حدث خطأ في إنشاء الوصفة: {str(e)}", "danger")
        return redirect(url_for("doctor.view_visit", visit_id=visit.id))


@doctor.route("/doctor/prescription/<int:prescription_id>/view_pdf")
@login_required
@doctor_required
def view_prescription_pdf(prescription_id):
    """عرض الوصفة الطبية كـ PDF في المتصفح"""
    prescription = Prescription.query.get_or_404(prescription_id)
    visit = prescription.visit
    
    # التأكد من أن الوصفة تنتمي للطبيب الحالي
    if visit.doctor_id != current_user.id:
        flash("غير مسموح لك بالوصول إلى هذه الوصفة", "danger")
        return redirect(url_for("doctor.dashboard"))
    
    try:
        # التحقق من وجود ملف PDF موجود مسبقاً
        if prescription.pdf_file:
            existing_path = os.path.join(current_app.root_path, prescription.pdf_file)
            if os.path.exists(existing_path):
                # استخدام الملف الموجود
                return send_file(existing_path, mimetype='application/pdf')
        
        # إنشاء ملف PDF جديد فقط إذا لم يكن موجوداً
        pdf_path = generate_prescription_pdf(prescription, visit)
        prescription.pdf_file = pdf_path
        db.session.commit()
        
        full_path = os.path.join(current_app.root_path, pdf_path)
        
        if os.path.exists(full_path):
            return send_file(full_path, mimetype='application/pdf')
        else:
            flash("لم يتم العثور على ملف الوصفة", "danger")
            return redirect(url_for("doctor.view_visit", visit_id=visit.id))
            
    except Exception as e:
        flash(f"حدث خطأ في عرض الوصفة: {str(e)}", "danger")
        return redirect(url_for("doctor.view_visit", visit_id=visit.id))


@doctor.route("/doctor/prescription/<int:prescription_id>/regenerate_pdf")
@login_required
@doctor_required
def regenerate_prescription_pdf(prescription_id):
    """إعادة إنشاء PDF للوصفة الطبية"""
    prescription = Prescription.query.get_or_404(prescription_id)
    visit = prescription.visit
    
    # التأكد من أن الوصفة تنتمي للطبيب الحالي
    if visit.doctor_id != current_user.id:
        flash("غير مسموح لك بالوصول إلى هذه الوصفة", "danger")
        return redirect(url_for("doctor.dashboard"))
    
    try:
        # حذف الملف القديم إذا كان موجوداً
        if prescription.pdf_file:
            old_path = os.path.join(current_app.root_path, prescription.pdf_file)
            if os.path.exists(old_path):
                os.remove(old_path)
        
        # إنشاء ملف PDF جديد
        pdf_path = generate_prescription_pdf(prescription, visit)
        prescription.pdf_file = pdf_path
        db.session.commit()
        
        flash("تم إعادة إنشاء الوصفة بنجاح!", "success")
        return redirect(url_for("doctor.view_prescription", prescription_id=prescription.id))
        
    except Exception as e:
        flash(f"حدث خطأ في إعادة إنشاء الوصفة: {str(e)}", "danger")
        return redirect(url_for("doctor.view_visit", visit_id=visit.id))


# Route محذوف - مكرر مع الـ API الجديد


@doctor.route("/doctor/visit-history")
@login_required
@doctor_required
def visit_history():
    """عرض تاريخ الزيارات"""
    # الحصول على جميع الزيارات التي قام بها الطبيب
    visits = Visit.query.filter_by(doctor_id=current_user.id).order_by(Visit.date.desc()).all()

    return render_template(
        "doctor/visit_history.html",
        title="سجل الزيارات",
        visits=visits
    )


@doctor.route("/doctor/view-visit/<int:visit_id>")
@login_required
@doctor_required
def view_visit(visit_id):
    """عرض تفاصيل زيارة معينة"""
    visit = Visit.query.get_or_404(visit_id)
    if visit.doctor != current_user:
        abort(403)
    return render_template("doctor/view_visit.html", title="تفاصيل الزيارة", visit=visit)


@doctor.route("/doctor/edit-visit/<int:visit_id>", methods=["GET", "POST"])
@login_required
@doctor_required
def edit_visit(visit_id):
    """تعديل زيارة موجودة"""
    visit = Visit.query.get_or_404(visit_id)
    if visit.doctor != current_user:
        abort(403)
    form = VisitForm()
    if form.validate_on_submit():
        visit.symptoms = form.symptoms.data
        visit.diagnosis = form.diagnosis.data
        visit.treatment = form.treatment.data
        visit.notes = form.notes.data
        visit.status = form.status.data
        visit.price = form.price.data
        visit.payment_status = form.payment_status.data
        db.session.commit()
        flash("تم تحديث معلومات الزيارة بنجاح", "success")
        return redirect(url_for("doctor.view_visit", visit_id=visit.id))
    elif request.method == "GET":
        form.symptoms.data = visit.symptoms
        form.diagnosis.data = visit.diagnosis
        form.treatment.data = visit.treatment
        form.notes.data = visit.notes
        form.status.data = visit.status
        form.price.data = visit.price
        form.payment_status.data = visit.payment_status
    return render_template("doctor/edit_visit.html", title="تعديل الزيارة", form=form, visit=visit)


# ==================== Predefined Prescriptions Routes ====================

@doctor.route("/doctor/predefined_prescriptions")
@login_required
@doctor_required
def predefined_prescriptions():
    """صفحة الوصفات المحددة مسبقاً"""
    medications = Medication.query.all()
    return render_template("doctor/predefined_prescriptions.html", 
                         title="الوصفات المحددة مسبقاً", 
                         medications=medications)


@doctor.route("/doctor/predefined_prescriptions_debug")
@login_required
@doctor_required
def predefined_prescriptions_debug():
    """صفحة تشخيص الوصفات المحددة مسبقاً"""
    medications = Medication.query.all()
    return render_template("doctor/predefined_prescriptions_debug.html", 
                         title="تشخيص الوصفات المحددة مسبقاً", 
                         medications=medications)


@doctor.route("/doctor/api/predefined_prescriptions", methods=["GET"])
@login_required
@doctor_required
def api_get_predefined_prescriptions():
    """API للحصول على الوصفات المحددة مسبقاً"""
    try:
        prescriptions = PredefinedPrescription.query.all()
        result = []
        
        for prescription in prescriptions:
            medications = []
            for ppm in prescription.medications:
                medications.append({
                    'medication': {
                        'id': ppm.medication.id,
                        'name': ppm.medication.name,
                        'dosage': ppm.medication.dosage
                    },
                    'quantity': ppm.quantity,
                    'instructions': ppm.instructions
                })
            
            result.append({
                'id': prescription.id,
                'name': prescription.name,
                'medications': medications
            })
        
        return jsonify(result)
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


@doctor.route("/doctor/api/predefined_prescriptions", methods=["POST"])
@login_required
@doctor_required
def api_add_predefined_prescription():
    """API لإضافة وصفة محددة مسبقاً"""
    try:
        data = request.get_json()
        name = data.get('name', '').strip()
        
        if not name:
            return jsonify({'success': False, 'message': 'اسم الوصفة مطلوب'})
        
        # التحقق من عدم وجود وصفة بنفس الاسم
        existing = PredefinedPrescription.query.filter_by(name=name).first()
        if existing:
            return jsonify({'success': False, 'message': 'يوجد وصفة بهذا الاسم مسبقاً'})
        
        prescription = PredefinedPrescription(name=name)
        db.session.add(prescription)
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'تم إضافة الوصفة بنجاح'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500


@doctor.route("/doctor/api/predefined_prescriptions/<int:prescription_id>", methods=["DELETE"])
@login_required
@doctor_required
def api_delete_predefined_prescription(prescription_id):
    """API لحذف وصفة محددة مسبقاً"""
    try:
        prescription = PredefinedPrescription.query.get_or_404(prescription_id)
        
        # حذف جميع الأدوية المرتبطة بالوصفة
        PredefinedPrescriptionMedication.query.filter_by(predefined_prescription_id=prescription_id).delete()
        
        # حذف الوصفة
        db.session.delete(prescription)
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'تم حذف الوصفة بنجاح'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500


@doctor.route("/doctor/api/predefined_prescriptions/<int:prescription_id>/medications", methods=["POST"])
@login_required
@doctor_required
def api_add_medication_to_predefined(prescription_id):
    """API لإضافة دواء لوصفة محددة مسبقاً"""
    try:
        prescription = PredefinedPrescription.query.get_or_404(prescription_id)
        data = request.get_json()
        
        medication_id = data.get('medication_id')
        quantity = data.get('quantity', '').strip()
        instructions = data.get('instructions', '').strip()
        
        if not medication_id:
            return jsonify({'success': False, 'message': 'يرجى اختيار دواء'})
        
        if not instructions:
            return jsonify({'success': False, 'message': 'التعليمات مطلوبة'})
        
        # التحقق من وجود الدواء
        medication = Medication.query.get(medication_id)
        if not medication:
            return jsonify({'success': False, 'message': 'الدواء غير موجود'})
        
        # التحقق من عدم إضافة نفس الدواء مرتين
        existing = PredefinedPrescriptionMedication.query.filter_by(
            predefined_prescription_id=prescription_id,
            medication_id=medication_id
        ).first()
        
        if existing:
            return jsonify({'success': False, 'message': 'هذا الدواء مضاف مسبقاً لهذه الوصفة'})
        
        # إضافة الدواء
        ppm = PredefinedPrescriptionMedication(
            predefined_prescription_id=prescription_id,
            medication_id=medication_id,
            quantity=quantity,
            instructions=instructions
        )
        db.session.add(ppm)
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'تم إضافة الدواء بنجاح'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500


@doctor.route("/doctor/api/predefined_prescriptions/<int:prescription_id>/medications/<int:medication_id>", methods=["DELETE"])
@login_required
@doctor_required
def api_remove_medication_from_predefined(prescription_id, medication_id):
    """API لحذف دواء من وصفة محددة مسبقاً"""
    try:
        ppm = PredefinedPrescriptionMedication.query.filter_by(
            predefined_prescription_id=prescription_id,
            medication_id=medication_id
        ).first_or_404()
        
        db.session.delete(ppm)
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'تم حذف الدواء بنجاح'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500


@doctor.route("/doctor/get_predefined_prescription_meds/<int:prescription_id>")
@login_required
@doctor_required
def get_predefined_prescription_meds(prescription_id):
    """API للحصول على أدوية وصفة محددة مسبقاً"""
    try:
        prescription = PredefinedPrescription.query.get_or_404(prescription_id)
        medications = []
        
        for ppm in prescription.medications:
            medications.append({
                'id': ppm.medication.id,
                'name': ppm.medication.name,
                'dosage': ppm.medication.dosage,
                'quantity': ppm.quantity,
                'instructions': ppm.instructions
            })
        
        return jsonify(medications)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@doctor.route("/doctor/delete-visit/<int:visit_id>", methods=["POST"])
@login_required
@doctor_required
def delete_visit(visit_id):
    """حذف زيارة"""
    visit = Visit.query.get_or_404(visit_id)
    if visit.doctor != current_user:
        abort(403)
    db.session.delete(visit)
    db.session.commit()
    flash("تم حذف الزيارة بنجاح", "success")
    return redirect(url_for("doctor.visit_history"))


@doctor.route("/doctor/settings", methods=["GET", "POST"])
@login_required
@doctor_required
def doctor_settings():
    import secrets
    from PIL import Image
    
    settings = DoctorSettings.query.filter_by(user_id=current_user.id).first()
    if not settings:
        settings = DoctorSettings(user_id=current_user.id)
        db.session.add(settings)
        db.session.commit()

    form = DoctorSettingsForm(obj=settings)

    if form.validate_on_submit():
        # معالجة رفع شعار العيادة
        if form.clinic_logo.data:
            # إنشاء مجلد الشعارات إذا لم يكن موجوداً
            logos_dir = os.path.join(current_app.root_path, 'static', 'logos')
            os.makedirs(logos_dir, exist_ok=True)
            
            # حذف الشعار القديم إذا كان موجوداً
            if settings.clinic_logo:
                old_logo_path = os.path.join(current_app.root_path, settings.clinic_logo.lstrip('/'))
                if os.path.exists(old_logo_path):
                    try:
                        os.remove(old_logo_path)
                    except:
                        pass
            
            # إنشاء اسم فريد للملف
            random_hex = secrets.token_hex(8)
            file_ext = form.clinic_logo.data.filename.split('.')[-1].lower()
            logo_filename = f"logo_{current_user.id}_{random_hex}.{file_ext}"
            logo_path = os.path.join(logos_dir, logo_filename)
            
            # حفظ وتحسين الصورة
            try:
                # فتح الصورة وتحسينها
                img = Image.open(form.clinic_logo.data)
                
                # تحويل إلى RGB إذا كانت PNG مع شفافية
                if img.mode in ('RGBA', 'LA', 'P'):
                    background = Image.new('RGB', img.size, (255, 255, 255))
                    if img.mode == 'P':
                        img = img.convert('RGBA')
                    background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
                    img = background
                
                # تغيير حجم الصورة إذا كانت كبيرة جداً
                max_size = (300, 300)
                img.thumbnail(max_size, Image.Resampling.LANCZOS)
                
                # حفظ الصورة
                img.save(logo_path, quality=85, optimize=True)
                
                # حفظ المسار النسبي في قاعدة البيانات
                settings.clinic_logo = f"static/logos/{logo_filename}"
                
            except Exception as e:
                flash(f'حدث خطأ في رفع الشعار: {str(e)}', 'danger')
                return redirect(url_for('doctor.doctor_settings'))
        
        # حفظ باقي الإعدادات
        settings.default_visit_price = form.default_visit_price.data
        settings.doctor_name_arabic = form.doctor_name_arabic.data
        settings.doctor_name_latin = form.doctor_name_latin.data
        settings.clinic_name = form.clinic_name.data
        settings.clinic_name_latin = form.clinic_name_latin.data
        settings.doctor_specialty = form.doctor_specialty.data
        settings.doctor_specialty_latin = form.doctor_specialty_latin.data
        
        db.session.commit()
        flash('تم حفظ الإعدادات بنجاح!', 'success')
        return redirect(url_for('doctor.doctor_settings'))

    return render_template('doctor/settings.html', title='إعدادات الطبيب', form=form, settings=settings)





from datetime import timedelta


@doctor.route("/doctor/payments")
@login_required
@doctor_required
def payments_list():
    """عرض قائمة المدفوعات مع إمكانية التصفية"""
    # الحصول على معايير التصفية من الطلب
    selected_month = request.args.get('month', type=int)
    selected_year = request.args.get('year', type=int)
    selected_status = request.args.get('status')
    
    # بناء الاستعلام الأساسي للزيارات التي قام بها الطبيب
    query = Visit.query.filter_by(doctor_id=current_user.id)
    
    # تطبيق التصفية حسب الشهر والسنة
    if selected_month and selected_year:
        query = query.filter(
            db.extract('month', Visit.date) == selected_month,
            db.extract('year', Visit.date) == selected_year
        )
    elif selected_year:
        query = query.filter(db.extract('year', Visit.date) == selected_year)
    elif selected_month:
        query = query.filter(db.extract('month', Visit.date) == selected_month)
    
    # تطبيق التصفية حسب حالة الدفع
    if selected_status:
        query = query.filter_by(payment_status=selected_status)
    
    # ترتيب النتائج حسب التاريخ (الأحدث أولاً)
    payments = query.order_by(Visit.date.desc()).all()
    
    # حساب الإحصائيات
    all_visits = Visit.query.filter_by(doctor_id=current_user.id).all()
    
    # المدفوعات المكتملة
    paid_visits = [v for v in all_visits if v.payment_status == "مدفوع"]
    paid_count = len(paid_visits)
    paid_amount = sum(v.price or 0 for v in paid_visits)
    
    # المدفوعات الجزئية
    partial_paid_visits = [v for v in all_visits if v.payment_status == "مدفوع جزئياً"]
    partial_paid_count = len(partial_paid_visits)
    partial_paid_amount = sum(v.price or 0 for v in partial_paid_visits)
    
    # المدفوعات المستحقة
    unpaid_visits = [v for v in all_visits if v.payment_status == "غير مدفوع"]
    unpaid_count = len(unpaid_visits)
    unpaid_amount = sum(v.price or 0 for v in unpaid_visits)
    
    # إجمالي المدفوعات
    total_paid = paid_amount + partial_paid_amount
    
    return render_template(
        "doctor/payments.html",
        title="المحاسبة",
        payments=payments,
        selected_month=selected_month,
        selected_year=selected_year,
        selected_status=selected_status,
        current_year=datetime.now().year,
        total_paid=total_paid,
        paid_count=paid_count,
        paid_amount=paid_amount,
        partial_paid_count=partial_paid_count,
        partial_paid_amount=partial_paid_amount,
        unpaid_count=unpaid_count,
        unpaid_amount=unpaid_amount
    )


@doctor.route("/patient-details/<int:patient_id>")
@login_required
@doctor_required
def patient_details(patient_id):
    """عرض تفاصيل المريض وتاريخ زياراته"""
    patient = Patient.query.get_or_404(patient_id)
    
    # الحصول على جميع زيارات المريض مع هذا الطبيب
    visits = Visit.query.filter_by(
        patient_id=patient.id,
        doctor_id=current_user.id
    ).order_by(Visit.date.desc()).all()
    
    return render_template(
        "doctor/patient_details.html",
        title=f"تفاصيل المريض - {patient.full_name}",
        patient=patient,
        visits=visits
    )


@doctor.route("/patients")
@login_required
@doctor_required
def list_patients():
    """قائمة المرضى المسجلين"""
    page = request.args.get("page", 1, type=int)
    search = request.args.get("search", "")

    if search:
        # البحث عن المرضى بالاسم أو رقم الهاتف
        patients = Patient.query.filter(Patient.full_name.ilike(f"%{search}%") | Patient.phone.ilike(f"%{search}%")).paginate(page=page, per_page=10)
    else:
        # عرض جميع المرضى مرتبين حسب تاريخ التسجيل (الأحدث أولاً)
        patients = Patient.query.order_by(Patient.created_at.desc()).paginate(page=page, per_page=10)

    return render_template("doctor/patients.html", title="قائمة المرضى", patients=patients, search=search)

# تعديل بيانات المريض من واجهة الطبيب
@doctor.route('/patient/<int:patient_id>/edit', methods=['GET', 'POST'])
@login_required
@doctor_required
def edit_patient_from_doctor(patient_id):
    patient = Patient.query.get_or_404(patient_id)
    form = PatientFormFrench()

    if form.validate_on_submit():
        patient.full_name = form.full_name.data
        patient.phone = form.phone.data
        patient.birth_date = form.birth_date.data
        patient.gender = form.gender.data or None
        patient.blood_group = form.blood_group.data or None
        patient.address = form.address.data or None
        db.session.commit()
        flash('تم تحديث بيانات المريض بنجاح', 'success')
        return redirect(url_for('doctor.list_patients'))

    # تعبئة النموذج عند GET
    if request.method == 'GET':
        form.full_name.data = patient.full_name
        form.phone.data = patient.phone
        form.birth_date.data = patient.birth_date
        form.gender.data = patient.gender or ''
        form.blood_group.data = patient.blood_group or ''
        form.address.data = patient.address or ''

    return render_template('doctor/patient_form_edit.html', title='Modifier le patient', form=form, patient=patient)

# إضافة مريض جديد من واجهة الطبيب
@doctor.route('/patient/new', methods=['GET', 'POST'])
@login_required
@doctor_required
def new_patient_doctor():
    form = PatientFormFrench()
    # Adapter les libellés en FR pour une expérience uniforme (déjà FR dans PatientFormFrench)
    if form.validate_on_submit():
        patient = Patient(
            full_name=form.full_name.data,
            phone=form.phone.data,
            birth_date=form.birth_date.data,
            gender=form.gender.data or None,
            blood_group=form.blood_group.data or None,
            address=form.address.data or None
        )
        db.session.add(patient)
        db.session.commit()
        flash('تم تسجيل المريض بنجاح', 'success')
        return redirect(url_for('doctor.patient_details', patient_id=patient.id))
    return render_template('doctor/patient_form_new.html', title='Ajouter un patient', form=form)

# المواعيد الأونلاين من واجهة الطبيب
@doctor.route('/online-appointments')
@login_required
@doctor_required
def online_appointments_doctor():
    import requests
    from datetime import datetime

    status_filter = request.args.get('status', '')
    date_filter = request.args.get('date', '')

    try:
        api_url = 'https://appointment-010t.onrender.com/api/appointments/all?token=123456'
        if status_filter:
            api_url += f'&status={status_filter}'
        if date_filter:
            api_url += f'&date={date_filter}'

        response = requests.get(api_url, timeout=15)
        if response.status_code == 200:
            data = response.json()
            appointments = data.get('appointments', [])
            count = data.get('count', 0)
            for appointment in appointments:
                try:
                    date_str = appointment.get('date', '')
                    time_str = appointment.get('time', '')
                    if date_str and time_str:
                        datetime_str = f"{date_str} {time_str}"
                        appointment['datetime_obj'] = datetime.strptime(datetime_str, '%Y-%m-%d %H:%M')
                    created_at = appointment.get('created_at', '')
                    if created_at:
                        appointment['created_at_obj'] = datetime.strptime(created_at, '%Y-%m-%d %H:%M:%S')
                except Exception:
                    pass
            available_statuses = ['قيد التأكيد', 'مؤكد', 'ملغي', 'مكتمل']
            return render_template('secretary/online_appointments.html',
                                   appointments=appointments,
                                   count=count,
                                   title='المواعيد الأونلاين',
                                   available_statuses=available_statuses,
                                   current_status_filter=status_filter,
                                   current_date_filter=date_filter)
        else:
            flash('فشل في جلب المواعيد الأونلاين', 'danger')
            return render_template('secretary/online_appointments.html',
                                   appointments=[], count=0, error='فشل في الاتصال بخدمة المواعيد',
                                   title='المواعيد الأونلاين', available_statuses=['قيد التأكيد', 'مؤكد', 'ملغي', 'مكتمل'],
                                   current_status_filter=status_filter, current_date_filter=date_filter)
    except requests.RequestException:
        flash('لا يمكن الاتصال بخدمة المواعيد الأونلاين. تأكد من اتصالك بالإنترنت.', 'warning')
        return render_template('secretary/online_appointments.html',
                               appointments=[], count=0, error='خدمة المواعيد غير متاحة حالياً',
                               title='المواعيد الأونلاين', available_statuses=['قيد التأكيد', 'مؤكد', 'ملغي', 'مكتمل'],
                               current_status_filter=status_filter, current_date_filter=date_filter)


@doctor.route("/api/search-patients")
@login_required
@doctor_required
def api_search_patients():
    """API للبحث التلقائي عن المرضى (واجهة الطبيب)"""
    term = request.args.get("term", "").trim() if hasattr(str, 'trim') else request.args.get("term", "").strip()
    term = term.strip()
    if not term or len(term) < 1:
        return jsonify([])
    try:
        patients = Patient.query.filter(
            db.or_(
                Patient.full_name.ilike(f"%{term}%"),
                Patient.phone.ilike(f"%{term}%"),
                Patient.address.ilike(f"%{term}%")
            )
        ).order_by(Patient.full_name.asc()).limit(8).all()
        results = []
        for patient in patients:
            results.append({
                "id": patient.id,
                "full_name": patient.full_name or "",
                "phone": patient.phone or "",
                "view_url": url_for("doctor.patient_details", patient_id=patient.id)
            })
        return jsonify(results)
    except Exception as e:
        current_app.logger.exception("Doctor search patients error: %s", e)
        return jsonify([]), 200


@doctor.route("/doctor/api/calendar-visits")
@login_required
@doctor_required
def calendar_daily_visits():
    """الحصول على زيارات يوم معين للتقويم"""
    date_str = request.args.get('date')
    if not date_str:
        return jsonify([])
    
    try:
        date = datetime.strptime(date_str, '%Y-%m-%d').date()
        
        # الحصول على زيارات اليوم
        visits = Visit.query.filter(
            Visit.doctor_id == current_user.id,
            db.func.date(Visit.date) == date
        ).order_by(Visit.date).all()
        
        visits_data = []
        for visit in visits:
            visits_data.append({
                'patient_name': visit.patient.full_name,
                'time': visit.date.strftime('%H:%M'),
                'status': visit.status or 'مكتملة',
                'url': url_for('doctor.view_visit', visit_id=visit.id)
            })
        
        return jsonify(visits_data)
    except ValueError:
        return jsonify([])


@doctor.route("/doctor/calendar")
@login_required
@doctor_required
def doctor_calendar():
    """عرض التقويم مع الزيارات"""
    # الحصول على الشهر والسنة من المعاملات
    year = request.args.get('year', type=int) or datetime.now().year
    month = request.args.get('month', type=int) or datetime.now().month
    
    # التأكد من صحة القيم
    if month < 1:
        month = 12
        year -= 1
    elif month > 12:
        month = 1
        year += 1
    
    # حساب الشهر السابق والتالي
    prev_month = month - 1 if month > 1 else 12
    prev_month_year = year if month > 1 else year - 1
    next_month = month + 1 if month < 12 else 1
    next_month_year = year if month < 12 else year + 1
    
    # إنشاء بيانات التقويم
    import calendar
    cal = calendar.monthcalendar(year, month)
    
    # الحصول على زيارات الشهر
    start_date = datetime(year, month, 1).date()
    if month == 12:
        end_date = datetime(year + 1, 1, 1).date()
    else:
        end_date = datetime(year, month + 1, 1).date()
    
    visits = Visit.query.filter(
        Visit.doctor_id == current_user.id,
        Visit.date >= start_date,
        Visit.date < end_date
    ).all()
    
    # تجميع الزيارات حسب التاريخ
    visits_by_date = {}
    for visit in visits:
        date_key = visit.date.date()
        if date_key not in visits_by_date:
            visits_by_date[date_key] = []
        visits_by_date[date_key].append(visit)
    
    # إنشاء بيانات التقويم مع الزيارات
    calendar_data = []
    for week in cal:
        week_data = []
        for day in week:
            if day == 0:
                # يوم من الشهر السابق أو التالي
                if len(week_data) < 4:  # بداية الشهر
                    prev_month_days = calendar.monthrange(prev_month_year, prev_month)[1]
                    actual_day = prev_month_days - (6 - len(week_data))
                    # التأكد من أن اليوم ضمن النطاق الصحيح للشهر
                    actual_day = max(1, min(actual_day, prev_month_days))
                    date_obj = datetime(prev_month_year, prev_month, actual_day).date()
                else:  # نهاية الشهر
                    actual_day = len(week_data) - 6
                    # التأكد من أن اليوم ضمن النطاق الصحيح للشهر
                    next_month_days = calendar.monthrange(next_month_year, next_month)[1]
                    actual_day = max(1, min(actual_day, next_month_days))
                    date_obj = datetime(next_month_year, next_month, actual_day).date()
            else:
                date_obj = datetime(year, month, day).date()
            
            day_visits = visits_by_date.get(date_obj, [])
            week_data.append({
                'date': date_obj,
                'visits': day_visits
            })
        calendar_data.append(week_data)
    
    # حساب إحصائيات الشهر
    total_visits = len(visits)
    unique_patients = len(set(visit.patient_id for visit in visits))
    avg_daily_visits = round(total_visits / 30, 1) if total_visits > 0 else 0
    
    return render_template(
        "doctor/calendar.html",
        title="التقويم",
        calendar_data=calendar_data,
        current_month=month,
        current_year=year,
        prev_month_month=prev_month,
        prev_month_year=prev_month_year,
        next_month_month=next_month,
        next_month_year=next_month_year,
        today=datetime.now().date(),
        total_visits=total_visits,
        unique_patients=unique_patients,
        avg_daily_visits=avg_daily_visits
    )


# ==================== طرق المواعيد ====================

@doctor.route("/appointments")
@login_required
@doctor_required
def appointments():
    """عرض قائمة المواعيد"""
    page = request.args.get('page', 1, type=int)
    status_filter = request.args.get('status', 'all')
    
    # بناء الاستعلام
    query = Appointment.query.filter_by(doctor_id=current_user.id)
    
    if status_filter != 'all':
        query = query.filter_by(status=status_filter)
    
    # ترتيب حسب تاريخ الموعد
    appointments = query.order_by(Appointment.appointment_date.asc()).paginate(
        page=page, per_page=10, error_out=False
    )
    
    return render_template('doctor/appointments.html', 
                         appointments=appointments, 
                         status_filter=status_filter)


@doctor.route("/create_appointment/<int:visit_id>", methods=['GET', 'POST'])
@login_required
@doctor_required
def create_appointment(visit_id):
    """إنشاء موعد جديد من زيارة معلقة"""
    visit = Visit.query.get_or_404(visit_id)
    
    # التأكد أن الزيارة للطبيب الحالي وأن حالتها معلقة
    if visit.doctor_id != current_user.id:
        abort(403)
    
    if visit.status != "معلقة":
        flash("يمكن إنشاء موعد فقط للزيارات المعلقة", "warning")
        return redirect(url_for('doctor.view_visit', visit_id=visit_id))
    
    form = AppointmentForm()
    
    if form.validate_on_submit():
        # التحقق من عدم وجود موعد مسبق لنفس الزيارة
        existing_appointment = Appointment.query.filter_by(visit_id=visit_id).first()
        if existing_appointment:
            flash("يوجد موعد مسبق لهذه الزيارة", "warning")
            return redirect(url_for('doctor.view_visit', visit_id=visit_id))
        
        # إنشاء الموعد الجديد
        appointment = Appointment(
            patient_id=visit.patient_id,
            doctor_id=current_user.id,
            visit_id=visit_id,
            appointment_date=form.appointment_date.data,
            notes=form.notes.data,
            status="مجدول"
        )
        
        db.session.add(appointment)
        db.session.commit()
        
        flash(f"تم حجز موعد للمريض {visit.patient.full_name} بتاريخ {appointment.appointment_date.strftime('%Y-%m-%d %H:%M')}", "success")
        return redirect(url_for('doctor.appointments'))
    
    return render_template('doctor/create_appointment.html', 
                         form=form, 
                         visit=visit)


@doctor.route("/appointment/<int:appointment_id>")
@login_required
@doctor_required
def view_appointment(appointment_id):
    """عرض تفاصيل موعد"""
    appointment = Appointment.query.get_or_404(appointment_id)
    
    # التأكد أن الموعد للطبيب الحالي
    if appointment.doctor_id != current_user.id:
        abort(403)
    
    return render_template('doctor/view_appointment.html', appointment=appointment)


@doctor.route("/appointment/<int:appointment_id>/update_status", methods=['POST'])
@login_required
@doctor_required
def update_appointment_status(appointment_id):
    """تحديث حالة الموعد"""
    appointment = Appointment.query.get_or_404(appointment_id)
    
    # التأكد أن الموعد للطبيب الحالي
    if appointment.doctor_id != current_user.id:
        abort(403)
    
    new_status = request.form.get('status')
    valid_statuses = ['مجدول', 'مكتمل', 'ملغي', 'فائت']
    
    if new_status in valid_statuses:
        appointment.status = new_status
        appointment.updated_at = datetime.utcnow()
        db.session.commit()
        
        flash(f"تم تحديث حالة الموعد إلى: {new_status}", "success")
    else:
        flash("حالة غير صحيحة", "error")
    
    return redirect(url_for('doctor.view_appointment', appointment_id=appointment_id))


@doctor.route("/appointment/<int:appointment_id>/delete", methods=['POST'])
@login_required
@doctor_required
def delete_appointment(appointment_id):
    """حذف موعد"""
    appointment = Appointment.query.get_or_404(appointment_id)
    
    # التأكد أن الموعد للطبيب الحالي
    if appointment.doctor_id != current_user.id:
        abort(403)
    
    # لا يمكن حذف المواعيد المكتملة
    if appointment.status == "مكتمل":
        flash("لا يمكن حذف موعد مكتمل", "error")
        return redirect(url_for('doctor.view_appointment', appointment_id=appointment_id))
    
    patient_name = appointment.patient.full_name
    db.session.delete(appointment)
    db.session.commit()
    
    flash(f"تم حذف موعد المريض {patient_name}", "success")
    return redirect(url_for('doctor.appointments'))


# ==================== إدارة قائمة الانتظار للطبيب ====================

@doctor.route("/call_next_patient", methods=['POST'])
@login_required
@doctor_required
def call_next_patient():
    """استدعاء المريض التالي مع إعطاء الأولوية للمواعيد"""
    try:
        today = datetime.now().date()
        
        # إنهاء التذكرة المستدعاة حالياً إذا كانت موجودة
        current_ticket = Ticket.query.filter(
            db.func.date(Ticket.created_at) == today,
            Ticket.status == "called"
        ).first()
        
        if current_ticket:
            current_ticket.status = "examined"
            db.session.commit()
        
        # البحث عن التذكرة التالية مع إعطاء الأولوية للمواعيد
        # أولاً: البحث عن تذاكر الأولوية (المواعيد)
        next_ticket = Ticket.query.filter(
            db.func.date(Ticket.created_at) == today,
            Ticket.status == "waiting"
        ).order_by(
            Ticket.priority.desc(),  # الأولوية أولاً (1 = أولوية، 0 = عادي)
            Ticket.number.asc()      # ثم الرقم تصاعدياً
        ).first()
        
        if next_ticket:
            # تحديث حالة التذكرة إلى مستدعاة
            next_ticket.status = "called"
            db.session.commit()
            
            # رسالة مختلفة حسب نوع التذكرة
            if next_ticket.priority == 1:
                flash(f"تم استدعاء التذكرة ذات الأولوية رقم {next_ticket.display_number} - {next_ticket.patient.full_name} (لديه موعد)", "success")
            else:
                flash(f"تم استدعاء التذكرة رقم {next_ticket.display_number} - {next_ticket.patient.full_name}", "success")
        else:
            flash("لا توجد تذاكر في قائمة الانتظار", "info")
            
    except Exception as e:
        db.session.rollback()
        flash(f"حدث خطأ أثناء استدعاء المريض: {str(e)}", "error")
    
    return redirect(url_for('doctor.dashboard'))


@doctor.route("/waiting_queue_status")
@login_required
@doctor_required
def waiting_queue_status():
    """عرض حالة قائمة الانتظار للطبيب"""
    today = datetime.now().date()
    
    # الحصول على التذاكر المنتظرة مرتبة حسب الأولوية
    waiting_tickets = Ticket.query.filter(
        db.func.date(Ticket.created_at) == today,
        Ticket.status == "waiting"
    ).order_by(
        Ticket.priority.desc(),  # الأولوية أولاً
        Ticket.number.asc()      # ثم الرقم
    ).all()
    
    # الحصول على التذكرة المستدعاة حالياً
    called_ticket = Ticket.query.filter(
        db.func.date(Ticket.created_at) == today,
        Ticket.status == "called"
    ).first()
    
    # تصنيف التذاكر حسب الأولوية
    priority_tickets = [t for t in waiting_tickets if t.priority >= 1]  # أولوية 1 و 2
    regular_tickets = [t for t in waiting_tickets if t.priority == 0]   # عادي
    
    return render_template('doctor/waiting_queue_status.html',
                         waiting_tickets=waiting_tickets,
                         called_ticket=called_ticket,
                         priority_tickets=priority_tickets,
                         regular_tickets=regular_tickets)


@doctor.route("/api/emergency-tickets-count")
@login_required
@doctor_required
def emergency_tickets_count():
    """API endpoint لإرجاع عدد التذاكر الطارئة"""
    from datetime import datetime
    
    today = datetime.now().date()
    
    # عدد التذاكر الحرجة
    critical_count = Ticket.query.filter(
        db.func.date(Ticket.created_at) == today,
        Ticket.status == "waiting",
        Ticket.priority == 2
    ).count()
    
    # عدد التذاكر ذات الأولوية
    priority_count = Ticket.query.filter(
        db.func.date(Ticket.created_at) == today,
        Ticket.status == "waiting",
        Ticket.priority == 1
    ).count()
    
    return jsonify({
        'critical': critical_count,
        'priority': priority_count,
        'total': critical_count + priority_count
    })


@doctor.route("/create_test_emergency_ticket")
@login_required
@doctor_required
def create_test_emergency_ticket():
    """إنشاء تذكرة طارئة للاختبار"""
    from datetime import datetime
    
    # البحث عن أول مريض
    patient = Patient.query.first()
    if not patient:
        flash("لا يوجد مرضى في النظام", "error")
        return redirect(url_for('doctor.dashboard'))
    
    today = datetime.now().date()
    
    # الحصول على آخر رقم تذكرة اليوم
    last_ticket = Ticket.query.filter(
        db.func.date(Ticket.created_at) == today
    ).order_by(Ticket.number.desc()).first()
    
    next_number = (last_ticket.number + 1) if last_ticket else 1
    
    # إنشاء تذكرة طارئة
    emergency_ticket = Ticket(
        patient_id=patient.id,
        number=next_number,
        status="waiting",
        ticket_type="emergency",
        priority=2,  # أولوية عالية جداً
        notes="حالة طارئة - اختبار",
        created_at=datetime.now()
    )
    
    db.session.add(emergency_ticket)
    
    # إنشاء تذكرة أولوية عادية
    priority_ticket = Ticket(
        patient_id=patient.id,
        number=next_number + 1,
        status="waiting",
        ticket_type="reservation",
        priority=1,  # أولوية عادية
        notes="موعد محجوز - اختبار",
        created_at=datetime.now()
    )
    
    db.session.add(priority_ticket)
    db.session.commit()
    
    flash("تم إنشاء تذاكر الاختبار بنجاح!", "success")
    return redirect(url_for('doctor.dashboard'))


@doctor.route("/payments")
@login_required
@doctor_required
def doctor_payments():
    """قائمة المدفوعات للطبيب مع فلتر التاريخ"""
    from datetime import date, timedelta
    
    # الحصول على المعاملات من الطلب
    selected_month = request.args.get('month', type=int)
    selected_year = request.args.get('year', type=int)
    selected_status = request.args.get('status', '')
    start_date = request.args.get('start_date', '')
    end_date = request.args.get('end_date', '')
    
    # بناء الاستعلام الأساسي
    query = Visit.query.filter_by(doctor_id=current_user.id)
    
    # تطبيق فلتر الشهر والسنة
    if selected_month and selected_year:
        query = query.filter(
            db.extract('month', Visit.date) == selected_month,
            db.extract('year', Visit.date) == selected_year
        )
    elif selected_year:
        query = query.filter(db.extract('year', Visit.date) == selected_year)
    elif selected_month:
        current_year = datetime.now().year
        query = query.filter(
            db.extract('month', Visit.date) == selected_month,
            db.extract('year', Visit.date) == current_year
        )
    
    # تطبيق فلتر التاريخ المخصص
    if start_date:
        try:
            start_date_obj = datetime.strptime(start_date, '%Y-%m-%d').date()
            query = query.filter(db.func.date(Visit.date) >= start_date_obj)
        except ValueError:
            flash("تاريخ البداية غير صحيح", "error")
    
    if end_date:
        try:
            end_date_obj = datetime.strptime(end_date, '%Y-%m-%d').date()
            query = query.filter(db.func.date(Visit.date) <= end_date_obj)
        except ValueError:
            flash("تاريخ النهاية غير صحيح", "error")
    
    # تطبيق فلتر حالة الدفع
    if selected_status:
        # تحويل القيم العربية إلى الفرنسية
        status_mapping = {
            'مدفوع': 'payé',
            'غير مدفوع': 'non_payé', 
            'مدفوع جزئياً': 'partiellement_payé'
        }
        mapped_status = status_mapping.get(selected_status, selected_status)
        query = query.filter_by(payment_status=mapped_status)
    
    # ترتيب النتائج
    payments = query.order_by(Visit.date.desc()).all()
    
    # حساب الإحصائيات - استخدام نفس query المطبق على payments
    # بدلاً من إنشاء query جديد، نستخدم نفس الفلاتر المطبقة على البيانات الرئيسية
    stats_query = Visit.query.filter_by(doctor_id=current_user.id)
    
    # تطبيق فلتر الشهر والسنة
    if selected_month and selected_year:
        stats_query = stats_query.filter(
            db.extract('month', Visit.date) == selected_month,
            db.extract('year', Visit.date) == selected_year
        )
    elif selected_year:
        stats_query = stats_query.filter(db.extract('year', Visit.date) == selected_year)
    elif selected_month:
        current_year = datetime.now().year
        stats_query = stats_query.filter(
            db.extract('month', Visit.date) == selected_month,
            db.extract('year', Visit.date) == current_year
        )
    
    # تطبيق فلتر التاريخ المخصص
    if start_date:
        try:
            start_date_obj = datetime.strptime(start_date, '%Y-%m-%d').date()
            stats_query = stats_query.filter(db.func.date(Visit.date) >= start_date_obj)
        except ValueError:
            pass
    
    if end_date:
        try:
            end_date_obj = datetime.strptime(end_date, '%Y-%m-%d').date()
            stats_query = stats_query.filter(db.func.date(Visit.date) <= end_date_obj)
        except ValueError:
            pass
    
    # ملاحظة: لا نطبق فلتر حالة الدفع على الإحصائيات لأننا نريد عرض جميع الحالات
    # حتى لو كان المستخدم يفلتر بحالة معينة
    
    # حساب الإحصائيات لكل حالة دفع
    paid_visits = stats_query.filter_by(payment_status='payé').all()
    unpaid_visits = stats_query.filter_by(payment_status='non_payé').all()
    partial_visits = stats_query.filter_by(payment_status='partiellement_payé').all()
    
    paid_count = len(paid_visits)
    unpaid_count = len(unpaid_visits)
    partial_paid_count = len(partial_visits)
    
    paid_amount = sum(visit.price or 0 for visit in paid_visits)
    unpaid_amount = sum(visit.price or 0 for visit in unpaid_visits)
    partial_paid_amount = sum(visit.price or 0 for visit in partial_visits)
    
    total_paid = paid_amount + partial_paid_amount
    
    return render_template('doctor/payments.html',
                         payments=payments,
                         selected_month=selected_month,
                         selected_year=selected_year,
                         selected_status=selected_status,
                         start_date=start_date,
                         end_date=end_date,
                         current_year=datetime.now().year,
                         total_paid=total_paid,
                         paid_count=paid_count,
                         unpaid_count=unpaid_count,
                         partial_paid_count=partial_paid_count,
                         paid_amount=paid_amount,
                         unpaid_amount=unpaid_amount,
                         partial_paid_amount=partial_paid_amount)
