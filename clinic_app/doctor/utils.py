from flask import current_app
import os
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak, KeepTogether, HRFlowable
from reportlab.lib.units import mm
from reportlab.lib.enums import TA_RIGHT, TA_CENTER, TA_LEFT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from arabic_reshaper import reshape
from bidi.algorithm import get_display

def generate_prescription_pdf(prescription, visit):
    from clinic_app.models import DoctorSettings
    
    # تسجيل الخط العربي
    arabic_font = 'Helvetica'  # افتراضي
    try:
        arabic_font_path = os.path.join(current_app.root_path, 'static', 'fonts', 'DroidArabicKufi.ttf')
        if os.path.exists(arabic_font_path):
            # تسجيل الخط العادي والغامق
            pdfmetrics.registerFont(TTFont('Arabic', arabic_font_path))
            pdfmetrics.registerFont(TTFont('Arabic-Bold', arabic_font_path))
            arabic_font = 'Arabic'
    except Exception as e:
        print(f"خطأ في تسجيل الخط العربي: {e}")
    
    # دالة لمعالجة النصوص العربية
    def process_arabic_text(text):
        if text and any('\u0600' <= c <= '\u06FF' for c in text):
            try:
                reshaped_text = reshape(text)
                return get_display(reshaped_text)
            except:
                return text
        return text
    
    # الحصول على إعدادات الطبيب
    doctor_settings = DoctorSettings.query.filter_by(user_id=visit.doctor_id).first()
    
    # إنشاء مجلد للوصفات الطبية
    static_folder = os.path.join(current_app.root_path, "static")
    prescriptions_dir = os.path.join(static_folder, "prescriptions")
    os.makedirs(prescriptions_dir, exist_ok=True)

    # إنشاء اسم الملف
    current_date = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"prescription_{visit.patient_id}_{visit.id}_{current_date}.pdf"
    file_path = os.path.join(prescriptions_dir, filename)

    # إنشاء ملف PDF بحجم A4
    doc = SimpleDocTemplate(
        file_path, 
        pagesize=A4, 
        rightMargin=15*mm, 
        leftMargin=15*mm, 
        topMargin=10*mm, 
        bottomMargin=15*mm
    )
    base_styles = getSampleStyleSheet()
    story = []
    
    # إعدادات الخطوط والألوان
    navy_blue = colors.Color(0.1, 0.2, 0.4)
    
    # أنماط الخطوط العربية (بدون bold)
    def create_arabic_style(size, alignment=TA_RIGHT):
        return ParagraphStyle(
            f'ArabicStyle{size}{alignment}',
            parent=base_styles['Normal'],
            alignment=alignment,
            fontName=arabic_font,
            fontSize=size,
            textColor=colors.black,
            wordWrap='RTL' if alignment == TA_RIGHT else None
        )
    
    # أنماط الخطوط اللاتينية
    def create_latin_style(size, alignment=TA_LEFT, bold=False):
        font_name = 'Helvetica-Bold' if bold else 'Helvetica'
        return ParagraphStyle(
            f'LatinStyle{size}{alignment}',
            parent=base_styles['Normal'],
            alignment=alignment,
            fontName=font_name,
            fontSize=size,
            textColor=colors.black
        )
    
    # إنشاء الأنماط
    custom_styles = {
        'doctor_name_latin': create_latin_style(14, TA_LEFT, True),
        'doctor_name_arabic': create_arabic_style(14, TA_RIGHT),
        'specialty_latin': create_latin_style(11),
        'specialty_arabic': create_arabic_style(11),
        'order_number': create_latin_style(10, TA_CENTER, True),
        'patient_info': create_latin_style(12, TA_LEFT, True),
        'date_location': create_latin_style(11, TA_RIGHT),
        'prescription_title': create_latin_style(24, TA_CENTER, True),
        'medication_number': create_latin_style(12, TA_LEFT, True),
        'medication_name': create_latin_style(11, TA_LEFT, True),
        'medication_instructions': create_latin_style(10, TA_LEFT),
        'qsp': create_latin_style(11, TA_RIGHT, True),
        'footer_warning': create_arabic_style(10, TA_CENTER),
        'footer_contact': create_arabic_style(9, TA_CENTER)
    }
    
    # رأس الوصفة - معلومات الطبيب
    # جمع بيانات الطبيب
    doctor_name_latin = getattr(doctor_settings, 'doctor_name_latin', None) or f"Dr. {visit.doctor.username}"
    doctor_name_arabic = process_arabic_text(
        getattr(doctor_settings, 'doctor_name', None) or f"الدكتور {visit.doctor.username}"
    )
    
    specialty_latin = getattr(doctor_settings, 'doctor_specialty_latin', None) or "Specialist"
    specialty_arabic = process_arabic_text(
        getattr(doctor_settings, 'doctor_specialty', None) or "أخصائي"
    )
    
    order_number = getattr(doctor_settings, 'order_number', None) or "N/A"
    
    # إنشاء جدول الرأس
    header_table = Table([
        [
            Paragraph(doctor_name_latin, custom_styles['doctor_name_latin']),
            Paragraph(process_arabic_text(f"رقم الأمر: {order_number}"), custom_styles['order_number']),
            Paragraph(doctor_name_arabic, custom_styles['doctor_name_arabic'])
        ],
        [
            Paragraph(specialty_latin, custom_styles['specialty_latin']),
            "",
            Paragraph(specialty_arabic, custom_styles['specialty_arabic'])
        ]
    ], colWidths=[160, 100, 160])
    
    header_table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('ALIGN', (0, 0), (0, -1), 'LEFT'),
        ('ALIGN', (1, 0), (1, -1), 'CENTER'),
        ('ALIGN', (2, 0), (2, -1), 'RIGHT'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('TOPPADDING', (0, 0), (-1, 0), 0),
        ('TOPPADDING', (0, 1), (-1, 1), 2),
    ]))
    
    story.append(header_table)
    story.append(Spacer(1, 15))
    
    # معلومات المريض
    patient_name = ""
    if hasattr(visit.patient, 'first_name') and hasattr(visit.patient, 'last_name'):
        patient_name = f"{visit.patient.first_name} {visit.patient.last_name}"
    elif hasattr(visit.patient, 'full_name'):
        patient_name = visit.patient.full_name
    else:
        patient_name = "غير محدد"
    
    patient_age = ""
    if hasattr(visit.patient, 'birth_date') and visit.patient.birth_date:
        today = datetime.now().date()
        birth_date = visit.patient.birth_date
        age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
        patient_age = f"{age} ans"
    else:
        patient_age = "غير محدد"
    
    # جدول معلومات المريض
    patient_info_table = Table([
        [
            Paragraph(f"Nom & Prénom: {patient_name.upper()}", custom_styles['patient_info']),
            Paragraph(f"Oued Rhiou, le: {visit.date.strftime('%d/%m/%Y')}", custom_styles['date_location'])
        ],
        [
            Paragraph(f"Age: {patient_age}", custom_styles['patient_info']),
            ""
        ]
    ], colWidths=[300, 200])
    
    patient_info_table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
    ]))
    
    story.append(patient_info_table)
    
    # خط فاصل
    story.append(HRFlowable(width="100%", thickness=1, spaceBefore=5, spaceAfter=10, color=colors.black))
    
    # عنوان الوصفة
    story.append(Paragraph("ORDONNANCE", custom_styles['prescription_title']))
    story.append(Spacer(1, 15))
    
    # قائمة الأدوية
    for i, med in enumerate(prescription.prescription_medications, 1):
        # اسم الدواء والجرعة
        med_name = med.medication.name.upper()
        if med.quantity:
            med_name += f" {med.quantity.upper()}"
        
        story.append(Paragraph(f"{i}. {med_name}", custom_styles['medication_name']))
        
        # تعليمات الاستخدام
        if med.instructions:
            story.append(Paragraph(med.instructions, custom_styles['medication_instructions']))
        
        # QSP
        story.append(Paragraph("QSP 7 Jour(s)", custom_styles['qsp']))
        story.append(Spacer(1, 10))
    
    # مساحة للتوقيع
    story.append(Spacer(1, 50))
    
    # خط فاصل سفلي
    story.append(HRFlowable(width="100%", thickness=1, spaceBefore=10, spaceAfter=10, color=colors.black))
    
    # تحذير
    warning_text = process_arabic_text("لا تتركوا الأدوية في متناول الأطفال")
    story.append(Paragraph(warning_text, custom_styles['footer_warning']))
    story.append(Spacer(1, 5))
    
    # معلومات الاتصال
    email = getattr(doctor_settings, 'email', None) or "drhamerassorl@gmail.com"
    phone = getattr(doctor_settings, 'phone', None) or "0560 08 95 61"
    address = process_arabic_text(
        getattr(doctor_settings, 'address', None) or 
        "العنوان : حي 20 مسكن ترقوي إقامة النور عمارة ط الطابق الأرضي - بناب الملعب البلدي القديم - وادي الرايو - غليزان"
    )
    
    # إضافة معلومات الاتصال بشكل عمودي
    story.append(Paragraph(process_arabic_text(f"✉ {email}"), custom_styles['footer_contact']))
    story.append(Paragraph(process_arabic_text(f"📱 {phone}"), custom_styles['footer_contact']))
    story.append(Paragraph(process_arabic_text(f"📍 {address}"), custom_styles['footer_contact']))
    
    # إنشاء الملف النهائي
    doc.build(story)
    
    # إرجاع المسار النسبي للملف
    relative_path = os.path.join("static", "prescriptions", filename)
    return relative_path