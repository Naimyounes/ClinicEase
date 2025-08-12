#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from clinic_app import create_app, db
from clinic_app.models import Patient
from datetime import date

app = create_app()

with app.app_context():
    # التحقق من وجود مرضى
    patients_count = Patient.query.count()
    print(f"عدد المرضى الحالي: {patients_count}")
    
    # عرض بعض المرضى الموجودين
    patients = Patient.query.limit(5).all()
    print("\nالمرضى الموجودون:")
    for patient in patients:
        print(f"- {patient.full_name} - {patient.phone}")
    
    # إضافة مريض تجريبي إذا لم يكن موجوداً
    test_patient = Patient.query.filter_by(full_name="أحمد محمد").first()
    if not test_patient:
        test_patient = Patient(
            full_name="أحمد محمد",
            phone="0123456789",
            birth_date=date(1990, 1, 1),
            gender="male",
            blood_group="A+",
            address="الرياض"
        )
        db.session.add(test_patient)
        
        # إضافة مريض آخر
        test_patient2 = Patient(
            full_name="فاطمة علي",
            phone="0987654321",
            birth_date=date(1985, 5, 15),
            gender="female",
            blood_group="O+",
            address="جدة"
        )
        db.session.add(test_patient2)
        
        db.session.commit()
        print("\nتم إضافة مرضى تجريبيين")
    else:
        print("\nالمرضى التجريبيون موجودون بالفعل")
    
    # التحقق النهائي
    final_count = Patient.query.count()
    print(f"\nالعدد النهائي للمرضى: {final_count}")