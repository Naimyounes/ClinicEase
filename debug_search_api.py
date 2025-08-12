#!/usr/bin/env python3
"""
تشخيص مشكلة API البحث
"""

from clinic_app import create_app, db
from clinic_app.models import Patient
from datetime import datetime

def debug_search():
    """تشخيص البحث"""
    app = create_app()
    
    with app.app_context():
        try:
            print("=== تشخيص مشكلة البحث ===")
            
            # التحقق من وجود مرضى في قاعدة البيانات
            total_patients = Patient.query.count()
            print(f"عدد المرضى في قاعدة البيانات: {total_patients}")
            
            if total_patients == 0:
                print("❌ لا يوجد مرضى في قاعدة البيانات")
                return
                
            # عرض بعض المرضى
            patients = Patient.query.limit(3).all()
            print("\nأمثلة على المرضى:")
            for p in patients:
                print(f"- ID: {p.id}, الاسم: {p.full_name}, الهاتف: {p.phone}")
            
            # اختبار البحث يدوياً
            print("\n=== اختبار البحث اليدوي ===")
            search_term = "test"
            
            search_results = Patient.query.filter(
                db.or_(
                    Patient.full_name.ilike(f"%{search_term}%"),
                    Patient.phone.ilike(f"%{search_term}%"),
                    Patient.address.ilike(f"%{search_term}%")
                )
            ).order_by(Patient.full_name.asc()).limit(8).all()
            
            print(f"نتائج البحث عن '{search_term}': {len(search_results)}")
            
            for patient in search_results:
                # حساب العمر
                age = ""
                if patient.birth_date:
                    today = datetime.now().date()
                    age_years = today.year - patient.birth_date.year
                    if today.month < patient.birth_date.month or (today.month == patient.birth_date.month and today.day < patient.birth_date.day):
                        age_years -= 1
                    age = f"{age_years} ans"
                
                # تحويل الجنس
                gender_display = 'Non spécifié'
                if patient.gender == 'male':
                    gender_display = 'Homme'
                elif patient.gender == 'female':
                    gender_display = 'Femme'
                
                result = {
                    'id': patient.id,
                    'full_name': patient.full_name or '',
                    'phone': patient.phone or 'Non spécifié',
                    'age': age,
                    'gender': gender_display,
                    'address': patient.address or 'Non spécifié'
                }
                
                print(f"  - {result}")
                
            print("✅ البحث اليدوي نجح")
            
        except Exception as e:
            print(f"❌ خطأ في التشخيص: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    debug_search()