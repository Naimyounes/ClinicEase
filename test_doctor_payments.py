#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
اختبار صفحة المدفوعات للطبيب
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from clinic_app import create_app
from clinic_app.models import Visit, Patient, User
from datetime import datetime, date, timedelta

def test_doctor_payments():
    """اختبار route المدفوعات للطبيب"""
    
    app = create_app()
    
    with app.app_context():
        from clinic_app import db
        
        print("=== اختبار صفحة المدفوعات للطبيب ===")
        
        # البحث عن طبيب
        doctor = User.query.filter_by(role='doctor').first()
        if not doctor:
            print("❌ لا يوجد طبيب في قاعدة البيانات")
            return
        
        print(f"✅ تم العثور على الطبيب: {doctor.username}")
        
        # البحث عن زيارات الطبيب
        visits = Visit.query.filter_by(doctor_id=doctor.id).all()
        print(f"📊 **إجمالي زيارات الطبيب:** {len(visits)}")
        
        if not visits:
            print("❌ لا توجد زيارات للطبيب")
            return
        
        # تحليل حالات الدفع
        paid_visits = [v for v in visits if v.payment_status == 'payé']
        unpaid_visits = [v for v in visits if v.payment_status == 'non_payé']
        partial_visits = [v for v in visits if v.payment_status == 'partiellement_payé']
        
        print(f"\n📈 **إحصائيات المدفوعات:**")
        print(f"   • مدفوعة (payé): {len(paid_visits)} زيارة")
        print(f"   • غير مدفوعة (non_payé): {len(unpaid_visits)} زيارة")
        print(f"   • مدفوعة جزئياً (partiellement_payé): {len(partial_visits)} زيارة")
        
        # حساب المبالغ
        paid_amount = sum(visit.price or 0 for visit in paid_visits)
        unpaid_amount = sum(visit.price or 0 for visit in unpaid_visits)
        partial_amount = sum(visit.price or 0 for visit in partial_visits)
        
        print(f"\n💰 **المبالغ:**")
        print(f"   • مدفوعة: {paid_amount} DA")
        print(f"   • غير مدفوعة: {unpaid_amount} DA")
        print(f"   • مدفوعة جزئياً: {partial_amount} DA")
        print(f"   • إجمالي المدفوعات: {paid_amount + partial_amount} DA")
        
        # اختبار فلتر التاريخ
        print(f"\n📅 **اختبار فلتر التاريخ:**")
        today = date.today()
        last_month = today - timedelta(days=30)
        
        recent_visits = [v for v in visits if v.date.date() >= last_month]
        print(f"   • زيارات آخر 30 يوم: {len(recent_visits)}")
        
        # اختبار فلتر الشهر
        current_month_visits = [v for v in visits if v.date.month == today.month and v.date.year == today.year]
        print(f"   • زيارات الشهر الحالي: {len(current_month_visits)}")
        
        # عرض عينة من البيانات
        print(f"\n📋 **عينة من الزيارات:**")
        for i, visit in enumerate(visits[:5]):
            patient_name = visit.patient.full_name if visit.patient else "غير معروف"
            price = visit.price or 0
            status = visit.payment_status
            date_str = visit.date.strftime('%Y-%m-%d')
            
            print(f"   {i+1}. {patient_name} - {date_str} - {price} DA - {status}")

def show_route_info():
    """عرض معلومات route"""
    
    print("=== معلومات Route المدفوعات ===")
    
    print("🔗 **URL:** /doctor/payments")
    print("📝 **Method:** GET")
    print("🔐 **Authentication:** login_required + doctor_required")
    
    print(f"\n📊 **المعاملات المدعومة:**")
    print("   • month: رقم الشهر (1-12)")
    print("   • year: السنة")
    print("   • status: حالة الدفع (مدفوع، غير مدفوع، مدفوع جزئياً)")
    print("   • start_date: تاريخ البداية (YYYY-MM-DD)")
    print("   • end_date: تاريخ النهاية (YYYY-MM-DD)")
    
    print(f"\n🎯 **أمثلة على الاستخدام:**")
    print("   • /doctor/payments")
    print("   • /doctor/payments?month=12&year=2024")
    print("   • /doctor/payments?status=مدفوع")
    print("   • /doctor/payments?start_date=2024-01-01&end_date=2024-12-31")
    print("   • /doctor/payments?start_date=2024-12-01&end_date=2024-12-31&status=غير مدفوع")

def show_template_features():
    """عرض ميزات Template"""
    
    print("=== ميزات صفحة المدفوعات ===")
    
    print("🎨 **الترجمة:**")
    print("   • جميع النصوص مترجمة للفرنسية")
    print("   • حالات الدفع: Payé, Non payé, Partiellement payé")
    print("   • العملة: DA بدلاً من ريال")
    
    print(f"\n🔍 **الفلاتر:**")
    print("   • فلتر الشهر والسنة")
    print("   • فلتر حالة الدفع")
    print("   • فلتر التاريخ المخصص (من تاريخ إلى تاريخ)")
    print("   • زر إعادة تعيين")
    
    print(f"\n📊 **كروت الإحصائيات:**")
    print("   • كرت أخضر: Paiements complets")
    print("   • كرت أصفر: Paiements partiels")
    print("   • كرت أحمر: Paiements en attente")
    print("   • عرض عدد الزيارات والمبلغ الإجمالي")
    
    print(f"\n📋 **الجدول:**")
    print("   • عرض اسم المريض (مع رابط لتفاصيل المريض)")
    print("   • تاريخ الزيارة")
    print("   • التشخيص (مقطوع إلى 30 حرف)")
    print("   • المبلغ بالدينار الجزائري")
    print("   • حالة الدفع مع ألوان مميزة")
    
    print(f"\n⚡ **JavaScript:**")
    print("   • التحقق من صحة التواريخ")
    print("   • تأثيرات بصرية للكروت")
    print("   • تحسين تجربة المستخدم")

if __name__ == "__main__":
    print("=== اختبار صفحة المدفوعات للطبيب ===")
    
    choice = input("\nاختر:\n1. اختبار البيانات\n2. معلومات Route\n3. ميزات Template\nالاختيار: ")
    
    if choice == "1":
        test_doctor_payments()
    elif choice == "2":
        show_route_info()
    elif choice == "3":
        show_template_features()
    else:
        print("اختيار غير صحيح")
        show_route_info()
        show_template_features()