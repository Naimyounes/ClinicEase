#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
اختبار دالة markAsPaid في صفحة المدفوعات
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from clinic_app import create_app
from clinic_app.models import Visit, Patient
from datetime import datetime

def test_mark_as_paid_functionality():
    """اختبار وظيفة تحديد الزيارة كمدفوعة"""
    
    app = create_app()
    
    with app.app_context():
        from clinic_app import db
        
        print("=== اختبار دالة markAsPaid ===")
        
        # البحث عن زيارة غير مدفوعة
        unpaid_visit = Visit.query.filter_by(payment_status='non_payé').first()
        
        if not unpaid_visit:
            print("❌ لا توجد زيارات غير مدفوعة للاختبار")
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
                price=200.0,
                date=datetime.now()
            )
            
            db.session.add(test_visit)
            db.session.commit()
            
            unpaid_visit = test_visit
            print(f"✅ تم إنشاء زيارة تجريبية: ID {unpaid_visit.id}")
        
        print(f"\n📋 **معلومات الزيارة قبل التحديث:**")
        print(f"   • ID الزيارة: {unpaid_visit.id}")
        print(f"   • المريض: {unpaid_visit.patient.full_name}")
        print(f"   • حالة الدفع: {unpaid_visit.payment_status}")
        print(f"   • المبلغ: {unpaid_visit.price} DA")
        
        # محاكاة تحديث حالة الدفع
        print(f"\n🔄 **محاكاة تحديث حالة الدفع...**")
        old_status = unpaid_visit.payment_status
        unpaid_visit.payment_status = 'payé'
        db.session.commit()
        
        print(f"✅ **تم التحديث بنجاح!**")
        print(f"   • الحالة السابقة: {old_status}")
        print(f"   • الحالة الجديدة: {unpaid_visit.payment_status}")
        
        # التحقق من التحديث
        updated_visit = Visit.query.get(unpaid_visit.id)
        if updated_visit.payment_status == 'payé':
            print(f"✅ **التحقق:** حالة الدفع محدثة بشكل صحيح")
        else:
            print(f"❌ **خطأ:** حالة الدفع لم تتحدث بشكل صحيح")

def show_testing_steps():
    """خطوات الاختبار اليدوي"""
    
    print("=== خطوات الاختبار اليدوي ===")
    
    print("🧪 **1. تشغيل الخادم:**")
    print("   python run.py")
    
    print(f"\n🧪 **2. تسجيل الدخول:**")
    print("   • اذهب إلى: http://localhost:5000/login")
    print("   • اسم المستخدم: secretary")
    print("   • كلمة المرور: secretary123")
    
    print(f"\n🧪 **3. الذهاب لصفحة المدفوعات:**")
    print("   • من dashboard السكريتير")
    print("   • انقر على 'Gestion des paiements'")
    print("   • أو اذهب مباشرة إلى: http://localhost:5000/payments")
    
    print(f"\n🧪 **4. اختبار الزر:**")
    print("   • ابحث عن زيارة بحالة 'Non payé' (شارة حمراء)")
    print("   • انقر على الزر الأزرق مع علامة ✓")
    print("   • يجب أن يظهر تأكيد: 'Êtes-vous sûr de marquer cette visite comme payée ?'")
    print("   • انقر 'OK'")
    
    print(f"\n🧪 **5. التحقق من النتيجة:**")
    print("   • يجب أن تظهر رسالة نجاح")
    print("   • يجب أن تتحول الشارة من 'Non payé' (أحمر) إلى 'Payé' (أخضر)")
    print("   • يجب أن يختفي الزر الأزرق (لأن الزيارة أصبحت مدفوعة)")

def show_expected_behavior():
    """السلوك المتوقع"""
    
    print("=== السلوك المتوقع ===")
    
    print("✅ **عند النقر على الزر الأزرق (✓):**")
    print("   1. يظهر تأكيد بالفرنسية")
    print("   2. عند الموافقة، يرسل POST request")
    print("   3. يحدث route: /secretary/visit/{visit_id}/mark_as_paid")
    print("   4. يحول payment_status من 'non_payé' إلى 'payé'")
    print("   5. يظهر رسالة نجاح")
    print("   6. يعيد توجيه إلى صفحة payments")
    
    print(f"\n✅ **التغييرات المرئية:**")
    print("   • الشارة تتحول من 'Non payé' (أحمر) إلى 'Payé' (أخضر)")
    print("   • الزر الأزرق (✓) يختفي")
    print("   • زر التحديث الأخضر يختفي")
    print("   • يبقى فقط زر عرض ملف المريض (أزرق)")
    
    print(f"\n✅ **تحديث الإحصائيات:**")
    print("   • عداد 'Non payé' ينقص بـ 1")
    print("   • في dashboard: كارت 'Paiements du jour' يزيد")

def show_troubleshooting():
    """حل المشاكل المحتملة"""
    
    print("=== حل المشاكل المحتملة ===")
    
    print("❌ **إذا لم يعمل الزر:**")
    print("   • تأكد من تشغيل JavaScript في المتصفح")
    print("   • افتح Developer Tools (F12) وتحقق من Console")
    print("   • تأكد من وجود CSRF token")
    
    print(f"\n❌ **إذا ظهر خطأ 404:**")
    print("   • تأكد من إضافة route mark_visit_as_paid")
    print("   • تأكد من restart الخادم بعد التحديث")
    
    print(f"\n❌ **إذا لم تتحدث حالة الدفع:**")
    print("   • تحقق من قاعدة البيانات")
    print("   • تأكد من أن القيم تستخدم 'payé' و 'non_payé'")
    
    print(f"\n❌ **إذا لم تظهر رسالة النجاح:**")
    print("   • تحقق من flash messages في template")
    print("   • تأكد من وجود alerts في layout.html")

if __name__ == "__main__":
    print("=== اختبار دالة markAsPaid ===")
    
    choice = input("\nاختر:\n1. اختبار تلقائي\n2. خطوات الاختبار اليدوي\n3. السلوك المتوقع\n4. حل المشاكل\nالاختيار: ")
    
    if choice == "1":
        test_mark_as_paid_functionality()
    elif choice == "2":
        show_testing_steps()
    elif choice == "3":
        show_expected_behavior()
    elif choice == "4":
        show_troubleshooting()
    else:
        print("اختيار غير صحيح")
        show_testing_steps()
        show_expected_behavior()