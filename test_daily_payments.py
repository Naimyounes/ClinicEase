#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
اختبار كارت المدفوعات اليومية في dashboard السكريتير
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from clinic_app import create_app
from clinic_app.models import Visit, Patient
from datetime import datetime

def show_feature_summary():
    """ملخص الميزة الجديدة"""
    
    print("=== كارت المدفوعات اليومية ===")
    
    print("🎯 **الميزة الجديدة:**")
    print("   • تم تحويل كارت 'Nouveaux patients' إلى 'Paiements du jour'")
    print("   • يظهر إجمالي المبلغ المدفوع اليوم")
    print("   • يظهر عدد الزيارات المدفوعة اليوم")
    print("   • لون أخضر للإشارة للنجاح")
    
    print(f"\n📊 **المعلومات المعروضة:**")
    print("   • المبلغ الإجمالي المدفوع اليوم (DA)")
    print("   • عدد الزيارات المدفوعة")
    print("   • أيقونة المال")
    
    print(f"\n🔧 **التحديثات المطبقة:**")
    print("   ✅ إضافة حساب total_paid_today في route dashboard")
    print("   ✅ إضافة حساب paid_visits_count")
    print("   ✅ تحديث الكارت في template")
    print("   ✅ تحديث التقارير JavaScript")

def debug_daily_payments():
    """فحص المدفوعات اليومية"""
    
    app = create_app()
    
    with app.app_context():
        from clinic_app import db
        
        today = datetime.now().date()
        
        print("=== فحص المدفوعات اليومية ===")
        print(f"التاريخ: {today}")
        
        # جميع الزيارات اليوم
        all_visits_today = Visit.query.filter(
            db.func.date(Visit.date) == today
        ).all()
        print(f"إجمالي الزيارات اليوم: {len(all_visits_today)}")
        
        # الزيارات المدفوعة اليوم
        paid_visits_today = Visit.query.filter(
            db.func.date(Visit.date) == today,
            Visit.payment_status == "payé"
        ).all()
        print(f"الزيارات المدفوعة اليوم: {len(paid_visits_today)}")
        
        # الزيارات غير المدفوعة اليوم
        unpaid_visits_today = Visit.query.filter(
            db.func.date(Visit.date) == today,
            Visit.payment_status == "non_payé"
        ).all()
        print(f"الزيارات غير المدفوعة اليوم: {len(unpaid_visits_today)}")
        
        # حساب المبلغ الإجمالي المدفوع اليوم
        total_paid_today = sum(visit.price or 0 for visit in paid_visits_today)
        print(f"إجمالي المبلغ المدفوع اليوم: {total_paid_today} DA")
        
        # تفاصيل الزيارات المدفوعة اليوم
        if paid_visits_today:
            print(f"\nتفاصيل الزيارات المدفوعة اليوم:")
            for visit in paid_visits_today:
                print(f"  - المريض: {visit.patient.full_name}, المبلغ: {visit.price} DA")
        
        # تفاصيل الزيارات غير المدفوعة اليوم
        if unpaid_visits_today:
            print(f"\nتفاصيل الزيارات غير المدفوعة اليوم:")
            for visit in unpaid_visits_today:
                print(f"  - المريض: {visit.patient.full_name}, المبلغ: {visit.price} DA")

def create_test_paid_visit():
    """إنشاء زيارة تجريبية مدفوعة اليوم"""
    
    app = create_app()
    
    with app.app_context():
        from clinic_app import db
        
        # البحث عن أول مريض
        patient = Patient.query.first()
        if not patient:
            print("لا يوجد مرضى في قاعدة البيانات")
            return
        
        # إنشاء زيارة تجريبية مدفوعة
        test_visit = Visit(
            patient_id=patient.id,
            doctor_id=1,  # افتراض وجود طبيب بـ ID 1
            symptoms="أعراض تجريبية",
            diagnosis="تشخيص تجريبي",
            treatment="علاج تجريبي",
            payment_status="payé",
            price=150.0,
            date=datetime.now()
        )
        
        db.session.add(test_visit)
        db.session.commit()
        
        print(f"تم إنشاء زيارة تجريبية مدفوعة للمريض: {patient.full_name}")
        print(f"المبلغ: {test_visit.price} DA")
        print(f"ID الزيارة: {test_visit.id}")

def show_testing_steps():
    """خطوات الاختبار"""
    
    print(f"\n=== خطوات الاختبار ===")
    
    print("🧪 **1. فحص البيانات الحالية:**")
    print("   python test_daily_payments.py")
    print("   اختر '1' لفحص المدفوعات اليومية")
    
    print(f"\n🧪 **2. إنشاء زيارة تجريبية مدفوعة:**")
    print("   python test_daily_payments.py")
    print("   اختر '2' لإنشاء زيارة مدفوعة اليوم")
    
    print(f"\n🧪 **3. اختبار dashboard السكريتير:**")
    print("   1. شغل الخادم: python run.py")
    print("   2. سجل دخول كسكريتير: secretary / secretary123")
    print("   3. اذهب إلى: http://localhost:5000/dashboard/secretary")
    print("   4. ابحث عن كارت 'Paiements du jour' الأخضر")
    
    print(f"\n🧪 **4. اختبار التقارير:**")
    print("   1. انقر على زر 'تقرير المدفوعات'")
    print("   2. انقر على زر 'تقرير يومي'")
    print("   3. تحقق من ظهور المدفوعات اليومية")

def show_expected_behavior():
    """السلوك المتوقع"""
    
    print(f"\n=== السلوك المتوقع ===")
    
    print("✅ **كارت 'Paiements du jour':**")
    print("   • لون أخضر")
    print("   • يظهر إجمالي المبلغ المدفوع اليوم")
    print("   • يظهر عدد الزيارات المدفوعة")
    print("   • أيقونة المال")
    
    print(f"\n✅ **التقارير:**")
    print("   • تقرير المدفوعات يشمل المدفوعات اليومية")
    print("   • التقرير اليومي يشمل كارت المدفوعات")
    print("   • جميع المبالغ بعملة DA")
    
    print(f"\n✅ **التحديث التلقائي:**")
    print("   • عند تحويل زيارة من non_payé إلى payé")
    print("   • يتحدث الكارت تلقائياً")
    print("   • يزيد المبلغ والعدد")

if __name__ == "__main__":
    print("=== اختبار كارت المدفوعات اليومية ===")
    
    show_feature_summary()
    
    choice = input("\nاختر:\n1. فحص المدفوعات اليومية\n2. إنشاء زيارة تجريبية مدفوعة\n3. عرض خطوات الاختبار\nالاختيار: ")
    
    if choice == "1":
        debug_daily_payments()
    elif choice == "2":
        create_test_paid_visit()
        print("\nفحص البيانات بعد الإنشاء:")
        debug_daily_payments()
    elif choice == "3":
        show_testing_steps()
        show_expected_behavior()
    else:
        print("اختيار غير صحيح")
        show_testing_steps()
        show_expected_behavior()