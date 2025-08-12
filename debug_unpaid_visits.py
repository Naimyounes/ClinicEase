#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
فحص الزيارات غير المدفوعة في قاعدة البيانات
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from clinic_app import create_app
from clinic_app.models import Visit, Patient

def debug_unpaid_visits():
    """فحص الزيارات غير المدفوعة"""
    
    app = create_app()
    
    with app.app_context():
        print("=== فحص الزيارات غير المدفوعة ===")
        
        # البحث عن جميع الزيارات
        all_visits = Visit.query.all()
        print(f"إجمالي الزيارات: {len(all_visits)}")
        
        # البحث عن الزيارات غير المدفوعة
        unpaid_visits = Visit.query.filter_by(payment_status="non_payé").all()
        print(f"الزيارات غير المدفوعة: {len(unpaid_visits)}")
        
        # البحث عن الزيارات بحالات مختلفة
        paye_visits = Visit.query.filter_by(payment_status="payé").all()
        print(f"الزيارات المدفوعة: {len(paye_visits)}")
        
        partially_paid = Visit.query.filter_by(payment_status="partiellement_payé").all()
        print(f"الزيارات المدفوعة جزئياً: {len(partially_paid)}")
        
        # عرض جميع حالات الدفع الموجودة
        unique_statuses = Visit.query.with_entities(Visit.payment_status).distinct().all()
        print(f"\nحالات الدفع الموجودة:")
        for status in unique_statuses:
            count = Visit.query.filter_by(payment_status=status[0]).count()
            print(f"  - '{status[0]}': {count} زيارة")
        
        # عرض تفاصيل آخر 5 زيارات غير مدفوعة
        if unpaid_visits:
            print(f"\nآخر 5 زيارات غير مدفوعة:")
            recent_unpaid = Visit.query.filter_by(payment_status="non_payé").order_by(Visit.date.desc()).limit(5).all()
            for visit in recent_unpaid:
                print(f"  - ID: {visit.id}, المريض: {visit.patient.full_name}, السعر: {visit.price}, التاريخ: {visit.date}")
        
        # حساب إجمالي المبالغ المستحقة
        total_unpaid = sum(visit.price or 0 for visit in unpaid_visits)
        print(f"\nإجمالي المبالغ المستحقة: {total_unpaid}")
        
        # الحصول على آخر زيارة غير مدفوعة
        last_unpaid = Visit.query.filter_by(payment_status="non_payé").order_by(Visit.date.desc()).first()
        if last_unpaid:
            print(f"\nآخر زيارة غير مدفوعة:")
            print(f"  - ID: {last_unpaid.id}")
            print(f"  - المريض: {last_unpaid.patient.full_name}")
            print(f"  - السعر: {last_unpaid.price}")
            print(f"  - التاريخ: {last_unpaid.date}")
            print(f"  - حالة الدفع: '{last_unpaid.payment_status}'")
        else:
            print("\nلا توجد زيارات غير مدفوعة")

def create_test_unpaid_visit():
    """إنشاء زيارة تجريبية غير مدفوعة"""
    
    app = create_app()
    
    with app.app_context():
        from clinic_app import db
        from datetime import datetime
        
        # البحث عن أول مريض
        patient = Patient.query.first()
        if not patient:
            print("لا يوجد مرضى في قاعدة البيانات")
            return
        
        # إنشاء زيارة تجريبية
        test_visit = Visit(
            patient_id=patient.id,
            doctor_id=1,  # افتراض وجود طبيب بـ ID 1
            symptoms="أعراض تجريبية",
            diagnosis="تشخيص تجريبي",
            treatment="علاج تجريبي",
            payment_status="non_payé",
            price=100.0,
            date=datetime.now()
        )
        
        db.session.add(test_visit)
        db.session.commit()
        
        print(f"تم إنشاء زيارة تجريبية غير مدفوعة للمريض: {patient.full_name}")
        print(f"ID الزيارة: {test_visit.id}")

if __name__ == "__main__":
    print("=== أداة فحص الزيارات غير المدفوعة ===")
    
    choice = input("اختر:\n1. فحص البيانات الحالية\n2. إنشاء زيارة تجريبية غير مدفوعة\nالاختيار: ")
    
    if choice == "1":
        debug_unpaid_visits()
    elif choice == "2":
        create_test_unpaid_visit()
        print("\nفحص البيانات بعد الإنشاء:")
        debug_unpaid_visits()
    else:
        print("اختيار غير صحيح")