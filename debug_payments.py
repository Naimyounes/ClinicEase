#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
فحص بيانات المدفوعات
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from clinic_app import create_app
from clinic_app.models import User, Patient, Visit

def debug_payments():
    """فحص بيانات المدفوعات"""
    
    app = create_app()
    
    with app.app_context():
        from clinic_app import db
        
        print("=== فحص بيانات المدفوعات ===")
        
        # البحث عن طبيب
        doctor = User.query.filter_by(role='doctor').first()
        if not doctor:
            print("❌ لا يوجد طبيب في قاعدة البيانات")
            return
        
        print(f"✅ تم العثور على الطبيب: {doctor.username} (ID: {doctor.id})")
        
        # البحث عن جميع الزيارات
        all_visits = Visit.query.filter_by(doctor_id=doctor.id).all()
        print(f"📊 إجمالي زيارات الطبيب: {len(all_visits)}")
        
        if not all_visits:
            print("❌ لا توجد زيارات للطبيب")
            print("💡 تشغيل: python add_test_payments.py لإضافة بيانات اختبار")
            return
        
        # تحليل حالات الدفع
        payment_statuses = {}
        for visit in all_visits:
            status = visit.payment_status or 'غير محدد'
            if status not in payment_statuses:
                payment_statuses[status] = []
            payment_statuses[status].append(visit)
        
        print(f"\n📈 تحليل حالات الدفع:")
        for status, visits in payment_statuses.items():
            count = len(visits)
            total_amount = sum(visit.price or 0 for visit in visits)
            print(f"   • {status}: {count} زيارة - {total_amount} DA")
        
        # فحص الإحصائيات كما في الكود
        paid_visits = [v for v in all_visits if v.payment_status == 'payé']
        unpaid_visits = [v for v in all_visits if v.payment_status == 'non_payé']
        partial_visits = [v for v in all_visits if v.payment_status == 'partiellement_payé']
        
        print(f"\n🔍 الإحصائيات المتوقعة في الكروت:")
        print(f"   • Paiements complets: {len(paid_visits)} زيارة - {sum(visit.price or 0 for visit in paid_visits)} DA")
        print(f"   • Paiements partiels: {len(partial_visits)} زيارة - {sum(visit.price or 0 for visit in partial_visits)} DA")
        print(f"   • Paiements en attente: {len(unpaid_visits)} زيارة - {sum(visit.price or 0 for visit in unpaid_visits)} DA")
        
        # عرض عينة من البيانات
        print(f"\n📋 عينة من الزيارات:")
        for i, visit in enumerate(all_visits[:10]):
            patient_name = visit.patient.full_name if visit.patient else "غير معروف"
            price = visit.price or 0
            status = visit.payment_status or 'غير محدد'
            date_str = visit.date.strftime('%Y-%m-%d') if visit.date else 'غير محدد'
            
            print(f"   {i+1}. {patient_name} - {date_str} - {price} DA - {status}")
        
        # فحص إذا كانت هناك مشاكل في البيانات
        print(f"\n🔧 فحص جودة البيانات:")
        visits_without_price = [v for v in all_visits if v.price is None]
        visits_without_status = [v for v in all_visits if v.payment_status is None]
        visits_without_patient = [v for v in all_visits if v.patient is None]
        
        if visits_without_price:
            print(f"   ⚠️  {len(visits_without_price)} زيارة بدون سعر")
        if visits_without_status:
            print(f"   ⚠️  {len(visits_without_status)} زيارة بدون حالة دفع")
        if visits_without_patient:
            print(f"   ⚠️  {len(visits_without_patient)} زيارة بدون مريض")
        
        if not visits_without_price and not visits_without_status and not visits_without_patient:
            print("   ✅ جميع البيانات سليمة")

if __name__ == "__main__":
    debug_payments()