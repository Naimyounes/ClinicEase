#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
from datetime import datetime, date

# إضافة مسار المشروع
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from clinic_app import create_app, db
from clinic_app.models import Patient

def add_test_patients():
    """إضافة مرضى تجريبيين لاختبار البحث"""
    app = create_app()
    
    with app.app_context():
        # التحقق من وجود مرضى
        existing_count = Patient.query.count()
        print(f"عدد المرضى الحاليين: {existing_count}")
        
        if existing_count > 0:
            print("يوجد مرضى في قاعدة البيانات بالفعل")
            # عرض أول 5 مرضى
            patients = Patient.query.limit(5).all()
            for patient in patients:
                print(f"- {patient.full_name} ({patient.phone})")
            return
        
        # إضافة مرضى تجريبيين
        test_patients = [
            {
                'full_name': 'أحمد محمد علي',
                'phone': '0123456789',
                'birth_date': date(1985, 5, 15),
                'gender': 'male',
                'blood_group': 'O+',
                'address': 'الرياض، المملكة العربية السعودية'
            },
            {
                'full_name': 'فاطمة أحمد السعيد',
                'phone': '0123456790',
                'birth_date': date(1990, 8, 22),
                'gender': 'female',
                'blood_group': 'A+',
                'address': 'جدة، المملكة العربية السعودية'
            },
            {
                'full_name': 'محمد عبدالله الأحمد',
                'phone': '0123456791',
                'birth_date': date(1978, 12, 10),
                'gender': 'male',
                'blood_group': 'B+',
                'address': 'الدمام، المملكة العربية السعودية'
            },
            {
                'full_name': 'نورا سعد المطيري',
                'phone': '0123456792',
                'birth_date': date(1995, 3, 8),
                'gender': 'female',
                'blood_group': 'AB+',
                'address': 'مكة المكرمة، المملكة العربية السعودية'
            },
            {
                'full_name': 'خالد عبدالرحمن القحطاني',
                'phone': '0123456793',
                'birth_date': date(1982, 7, 25),
                'gender': 'male',
                'blood_group': 'O-',
                'address': 'المدينة المنورة، المملكة العربية السعودية'
            }
        ]
        
        for patient_data in test_patients:
            patient = Patient(**patient_data)
            db.session.add(patient)
        
        db.session.commit()
        print(f"تم إضافة {len(test_patients)} مرضى تجريبيين بنجاح!")
        
        # التحقق من الإضافة
        total_patients = Patient.query.count()
        print(f"إجمالي المرضى الآن: {total_patients}")

if __name__ == '__main__':
    add_test_patients()