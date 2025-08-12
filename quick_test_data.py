#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
إضافة بيانات اختبار سريعة للمدفوعات
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from clinic_app import create_app
from clinic_app.models import User, Patient, Visit
from datetime import datetime, date, timedelta

def add_quick_test_data():
    """إضافة بيانات اختبار سريعة"""
    
    app = create_app()
    
    with app.app_context():
        from clinic_app import db
        
        print("=== إضافة بيانات اختبار سريعة ===")
        
        # البحث عن طبيب
        doctor = User.query.filter_by(role='doctor').first()
        if not doctor:
            print("❌ لا يوجد طبيب في قاعدة البيانات")
            return
        
        # البحث عن مريض أو إنشاء واحد
        patient = Patient.query.first()
        if not patient:
            patient = Patient(
                full_name="مريض تجريبي",
                phone="0123456789",
                birth_date=date(1990, 1, 1),
                gender="male"
            )
            db.session.add(patient)
            db.session.commit()
            print("✅ تم إنشاء مريض تجريبي")
        
        # إنشاء 10 زيارات تجريبية
        visits_data = [
            {"status": "payé", "price": 3000, "days_ago": 1},
            {"status": "payé", "price": 2500, "days_ago": 2},
            {"status": "non_payé", "price": 4000, "days_ago": 3},
            {"status": "partiellement_payé", "price": 3500, "days_ago": 5},
            {"status": "payé", "price": 2000, "days_ago": 7},
            {"status": "non_payé", "price": 5000, "days_ago": 10},
            {"status": "payé", "price": 3000, "days_ago": 15},
            {"status": "partiellement_payé", "price": 4500, "days_ago": 20},
            {"status": "non_payé", "price": 2500, "days_ago": 25},
            {"status": "payé", "price": 3500, "days_ago": 30},
        ]
        
        for i, visit_data in enumerate(visits_data):
            visit_date = datetime.now() - timedelta(days=visit_data["days_ago"])
            
            visit = Visit(
                patient_id=patient.id,
                doctor_id=doctor.id,
                date=visit_date,
                diagnosis=f"Consultation {i+1}",
                treatment=f"Traitement {i+1}",
                price=visit_data["price"],
                payment_status=visit_data["status"],
                status='مكتمل'
            )
            
            try:
                db.session.add(visit)
                db.session.commit()
                print(f"✅ زيارة {i+1}: {visit_data['status']} - {visit_data['price']} DA")
            except Exception as e:
                db.session.rollback()
                print(f"❌ خطأ في الزيارة {i+1}: {str(e)}")
        
        print("\n🎉 تم إنشاء البيانات التجريبية بنجاح!")
        print("📝 يمكنك الآن اختبار صفحة المدفوعات على: http://localhost:5000/doctor/payments")

if __name__ == "__main__":
    add_quick_test_data()