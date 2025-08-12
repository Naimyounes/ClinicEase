# API مؤقت للبحث - سيتم دمجه مع routes.py

from flask import request, jsonify
from clinic_app.models import Patient
from clinic_app import db
from datetime import datetime

def search_patients_api_temp():
    """API للبحث التلقائي عن المرضى"""
    term = request.args.get("term", "").strip()
    
    if not term or len(term) < 1:
        return jsonify([])
    
    try:
        # البحث المحسن في جميع الحقول المهمة
        patients = Patient.query.filter(
            db.or_(
                Patient.full_name.ilike(f"%{term}%"),
                Patient.phone.ilike(f"%{term}%"),
                Patient.address.ilike(f"%{term}%")
            )
        ).order_by(Patient.full_name.asc()).limit(8).all()
        
        # تحويل النتائج إلى JSON مع معلومات إضافية
        results = []
        for patient in patients:
            # حساب عمر المريض
            age = ""
            if patient.birth_date:
                today = datetime.now().date()
                age_years = today.year - patient.birth_date.year
                if today.month < patient.birth_date.month or (today.month == patient.birth_date.month and today.day < patient.birth_date.day):
                    age_years -= 1
                age = f"{age_years} ans"
            
            # تحويل الجنس للفرنسية
            gender_display = 'Non spécifié'
            if patient.gender == 'male':
                gender_display = 'Homme'
            elif patient.gender == 'female':
                gender_display = 'Femme'
            elif patient.gender == 'other':
                gender_display = 'Non spécifié'
            
            results.append({
                'id': patient.id,
                'full_name': patient.full_name or '',
                'phone': patient.phone or 'Non spécifié',
                'age': age,
                'gender': gender_display,
                'address': patient.address or 'Non spécifié',
                'view_url': f'/secretary/patient/{patient.id}',
                'edit_url': f'/secretary/patient/{patient.id}/edit',
                'ticket_url': f'/secretary/ticket/create/{patient.id}'
            })
        
        return jsonify(results)
        
    except Exception as e:
        print(f"Erreur dans la recherche: {str(e)}")
        return jsonify([]), 200