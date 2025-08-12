#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
إضافة بيانات اختبار للمدفوعات
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from clinic_app import create_app
from clinic_app.models import User, Patient, Visit
from datetime import datetime, date, timedelta
import random

def add_test_payments():
    """إضافة بيانات اختبار للمدفوعات"""
    
    app = create_app()
    
    with app.app_context():
        from clinic_app import db
        
        print("=== إضافة بيانات اختبار للمدفوعات ===")
        
        # البحث عن طبيب
        doctor = User.query.filter_by(role='doctor').first()
        if not doctor:
            print("❌ لا يوجد طبيب في قاعدة البيانات")
            return
        
        print(f"✅ تم العثور على الطبيب: {doctor.username}")
        
        # البحث عن مرضى
        patients = Patient.query.all()
        if len(patients) < 3:
            print("❌ يجب وجود 3 مرضى على الأقل")
            return
        
        print(f"✅ تم العثور على {len(patients)} مريض")
        
        # إنشاء زيارات اختبار
        payment_statuses = ['payé', 'non_payé', 'partiellement_payé']
        diagnoses = [
            'Consultation générale',
            'Contrôle de routine',
            'Grippe saisonnière',
            'Hypertension artérielle',
            'Diabète type 2',
            'Mal de dos',
            'Migraine',
            'Allergie',
            'Infection respiratoire',
            'Bilan de santé'
        ]
        
        visits_created = 0
        
        # إنشاء زيارات للشهرين الماضيين
        for i in range(30):  # 30 زيارة
            # تاريخ عشوائي في آخر 60 يوم
            days_ago = random.randint(0, 60)
            visit_date = datetime.now() - timedelta(days=days_ago)
            
            # مريض عشوائي
            patient = random.choice(patients)
            
            # حالة دفع عشوائية
            payment_status = random.choice(payment_statuses)
            
            # سعر عشوائي
            price = random.choice([2000, 2500, 3000, 3500, 4000, 4500, 5000])
            
            # تشخيص عشوائي
            diagnosis = random.choice(diagnoses)
            
            # إنشاء الزيارة
            visit = Visit(
                patient_id=patient.id,
                doctor_id=doctor.id,
                date=visit_date,
                diagnosis=diagnosis,
                treatment=f"Traitement prescrit pour {diagnosis.lower()}",
                price=price,
                payment_status=payment_status,
                status='مكتمل'
            )
            
            try:
                db.session.add(visit)
                db.session.commit()
                visits_created += 1
                
                status_fr = {
                    'payé': 'Payé',
                    'non_payé': 'Non payé',
                    'partiellement_payé': 'Partiellement payé'
                }[payment_status]
                
                print(f"   ✅ زيارة {visits_created}: {patient.full_name} - {visit_date.strftime('%Y-%m-%d')} - {price} DA - {status_fr}")
                
            except Exception as e:
                db.session.rollback()
                print(f"   ❌ خطأ في إنشاء الزيارة: {str(e)}")
        
        print(f"\n🎉 تم إنشاء {visits_created} زيارة بنجاح!")
        
        # عرض الإحصائيات
        all_visits = Visit.query.filter_by(doctor_id=doctor.id).all()
        paid_visits = [v for v in all_visits if v.payment_status == 'payé']
        unpaid_visits = [v for v in all_visits if v.payment_status == 'non_payé']
        partial_visits = [v for v in all_visits if v.payment_status == 'partiellement_payé']
        
        print(f"\n📊 **إحصائيات إجمالية:**")
        print(f"   • إجمالي الزيارات: {len(all_visits)}")
        print(f"   • مدفوعة: {len(paid_visits)}")
        print(f"   • غير مدفوعة: {len(unpaid_visits)}")
        print(f"   • مدفوعة جزئياً: {len(partial_visits)}")
        
        paid_amount = sum(visit.price or 0 for visit in paid_visits)
        unpaid_amount = sum(visit.price or 0 for visit in unpaid_visits)
        partial_amount = sum(visit.price or 0 for visit in partial_visits)
        
        print(f"\n💰 **المبالغ:**")
        print(f"   • مدفوعة: {paid_amount} DA")
        print(f"   • غير مدفوعة: {unpaid_amount} DA")
        print(f"   • مدفوعة جزئياً: {partial_amount} DA")
        print(f"   • إجمالي المدفوعات: {paid_amount + partial_amount} DA")

if __name__ == "__main__":
    add_test_payments()