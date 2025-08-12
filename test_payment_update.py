#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
اختبار تحديث حالة الدفع إلى payé
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from clinic_app import create_app
from clinic_app.models import Visit, Patient
from datetime import datetime

def test_payment_status_update():
    """اختبار تحديث حالة الدفع"""
    
    app = create_app()
    
    with app.app_context():
        from clinic_app import db
        
        print("=== اختبار تحديث حالة الدفع ===")
        
        # البحث عن زيارة غير مدفوعة
        unpaid_visit = Visit.query.filter_by(payment_status='non_payé').first()
        
        if not unpaid_visit:
            print("❌ لا توجد زيارات غير مدفوعة")
            print("دعني أنشئ زيارة تجريبية...")
            
            # إنشاء زيارة تجريبية
            patient = Patient.query.first()
            if not patient:
                print("❌ لا يوجد مرضى في قاعدة البيانات")
                return
            
            test_visit = Visit(
                patient_id=patient.id,
                doctor_id=1,
                symptoms="أعراض تجريبية",
                diagnosis="تشخيص تجريبي", 
                treatment="علاج تجريبي",
                payment_status="non_payé",
                price=300.0,
                date=datetime.now()
            )
            
            db.session.add(test_visit)
            db.session.commit()
            
            unpaid_visit = test_visit
            print(f"✅ تم إنشاء زيارة تجريبية: ID {unpaid_visit.id}")
        
        print(f"\n📋 **معلومات الزيارة قبل التحديث:**")
        print(f"   • ID الزيارة: {unpaid_visit.id}")
        print(f"   • المريض: {unpaid_visit.patient.full_name}")
        print(f"   • حالة الدفع: '{unpaid_visit.payment_status}'")
        print(f"   • المبلغ: {unpaid_visit.price} DA")
        
        # محاكاة تحديث حالة الدفع
        print(f"\n🔄 **تحديث حالة الدفع...**")
        old_status = unpaid_visit.payment_status
        unpaid_visit.payment_status = 'payé'
        db.session.commit()
        
        print(f"✅ **تم التحديث بنجاح!**")
        print(f"   • الحالة السابقة: '{old_status}'")
        print(f"   • الحالة الجديدة: '{unpaid_visit.payment_status}'")
        
        # التحقق من التحديث
        updated_visit = Visit.query.get(unpaid_visit.id)
        if updated_visit.payment_status == 'payé':
            print(f"✅ **التحقق:** حالة الدفع = '{updated_visit.payment_status}'")
            print(f"✅ **النتيجة:** سيظهر في الواجهة كـ 'Payé' (شارة خضراء)")
        else:
            print(f"❌ **خطأ:** حالة الدفع = '{updated_visit.payment_status}'")
        
        # اختبار الفلتر
        print(f"\n🔍 **اختبار الفلتر:**")
        paid_visits = Visit.query.filter_by(payment_status='payé').all()
        unpaid_visits = Visit.query.filter_by(payment_status='non_payé').all()
        partial_visits = Visit.query.filter_by(payment_status='partiellement_payé').all()
        
        print(f"   • زيارات مدفوعة (payé): {len(paid_visits)}")
        print(f"   • زيارات غير مدفوعة (non_payé): {len(unpaid_visits)}")
        print(f"   • زيارات مدفوعة جزئياً (partiellement_payé): {len(partial_visits)}")

def show_expected_display():
    """عرض كيف ستظهر في الواجهة"""
    
    print("=== كيف ستظهر في الواجهة ===")
    
    print("🎨 **عرض حالة الدفع في الجدول:**")
    print("   • payment_status = 'payé' → <span class='badge bg-success'>Payé</span>")
    print("   • payment_status = 'non_payé' → <span class='badge bg-danger'>Non payé</span>")
    print("   • payment_status = 'partiellement_payé' → <span class='badge bg-warning'>Partiellement payé</span>")
    
    print(f"\n🔘 **الأزرار المتاحة:**")
    print("   • إذا كانت الحالة 'payé': زر واحد فقط (عرض المريض)")
    print("   • إذا كانت الحالة 'non_payé': 3 أزرار (عرض المريض + تحديث + تحديد كمدفوع)")
    print("   • إذا كانت الحالة 'partiellement_payé': 3 أزرار (عرض المريض + تحديث + تحديد كمدفوع)")
    
    print(f"\n📊 **الفلتر:**")
    print("   • 'Tous les statuts' → يظهر جميع الزيارات")
    print("   • 'Payé' → يظهر فقط الزيارات بحالة 'payé'")
    print("   • 'Non payé' → يظهر فقط الزيارات بحالة 'non_payé'")
    print("   • 'Partiellement payé' → يظهر فقط الزيارات بحالة 'partiellement_payé'")

def show_testing_steps():
    """خطوات الاختبار"""
    
    print("=== خطوات الاختبار ===")
    
    print("🧪 **1. تشغيل الخادم:**")
    print("   python run.py")
    
    print(f"\n🧪 **2. الذهاب لصفحة المدفوعات:**")
    print("   http://localhost:5000/payments")
    
    print(f"\n🧪 **3. البحث عن زيارة غير مدفوعة:**")
    print("   • ابحث عن شارة حمراء 'Non payé'")
    print("   • يجب أن ترى 3 أزرار في عمود 'Actions'")
    
    print(f"\n🧪 **4. النقر على الزر الأزرق (✓):**")
    print("   • انقر على الزر الأزرق مع علامة ✓")
    print("   • يجب أن يظهر تأكيد: 'Êtes-vous sûr de marquer cette visite comme payée ?'")
    print("   • انقر 'OK'")
    
    print(f"\n🧪 **5. التحقق من النتيجة:**")
    print("   • يجب أن تظهر رسالة نجاح")
    print("   • الشارة تتحول من 'Non payé' (أحمر) إلى 'Payé' (أخضر)")
    print("   • الأزرار تختفي (يبقى فقط زر عرض المريض)")
    print("   • عداد 'Non payé' ينقص بـ 1")
    
    print(f"\n🧪 **6. اختبار الفلتر:**")
    print("   • جرب فلتر 'Payé' - يجب أن تظهر الزيارة المحدثة")
    print("   • جرب فلتر 'Non payé' - يجب ألا تظهر الزيارة المحدثة")

if __name__ == "__main__":
    print("=== اختبار تحديث حالة الدفع إلى payé ===")
    
    choice = input("\nاختر:\n1. اختبار تلقائي\n2. عرض كيف ستظهر في الواجهة\n3. خطوات الاختبار\nالاختيار: ")
    
    if choice == "1":
        test_payment_status_update()
    elif choice == "2":
        show_expected_display()
    elif choice == "3":
        show_testing_steps()
    else:
        print("اختيار غير صحيح")
        show_testing_steps()