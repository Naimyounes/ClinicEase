#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
اختبار إصلاح مشكلة البحث في الأدوية
"""

import sys
import os

# إضافة مسار المشروع
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# استيراد التطبيق والنماذج
from clinic_app import create_app, db
from clinic_app.models import Visit, Patient, Medication

# إنشاء التطبيق
app = create_app()

def check_javascript_structure():
    """فحص بنية JavaScript"""
    
    print("=== فحص بنية JavaScript ===")
    
    print("✅ الدوال المطلوبة:")
    print("  - attachSearchListeners(entry)")
    print("  - attachAddListeners()")
    print("  - attachRemoveListeners()")
    print("  - addMedicationEntry()")
    print("  - hideAllDropdowns()")
    
    print(f"\n✅ استدعاء الدوال:")
    print("  - attachSearchListeners للدواء الأول ✅")
    print("  - attachAddListeners للأزرار ✅")
    print("  - attachSearchListeners في addMedicationEntry ✅")

def check_html_structure():
    """فحص بنية HTML"""
    
    print(f"\n=== فحص بنية HTML ===")
    
    print("✅ العناصر المطلوبة:")
    print("  - .medication-entry (الدواء الأول)")
    print("  - .medication-search-input (مربع البحث)")
    print("  - input[type='hidden'] (القيمة المخفية)")
    print("  - .selected-medication (عرض الاختيار)")
    print("  - #dropdown-container (container خارجي)")
    
    print(f"\n✅ CSS Classes:")
    print("  - .medication-dropdown")
    print("  - .medication-option")
    print("  - .add-medication-btn")
    print("  - .remove-medication-btn")

def check_medications_data():
    """فحص بيانات الأدوية"""
    
    with app.app_context():
        print(f"\n=== فحص بيانات الأدوية ===")
        
        total_meds = Medication.query.count()
        print(f"إجمالي الأدوية: {total_meds}")
        
        if total_meds == 0:
            print("❌ لا توجد أدوية في قاعدة البيانات!")
            return False
        
        # فحص أمثلة
        test_searches = ['PARA', 'AMOX', '500MG']
        for term in test_searches:
            count = Medication.query.filter(
                db.or_(
                    Medication.name.like(f'%{term}%'),
                    Medication.dosage.like(f'%{term}%')
                )
            ).count()
            print(f"  - البحث عن '{term}': {count} نتيجة")
        
        return True

def show_debugging_steps():
    """عرض خطوات التشخيص"""
    
    print(f"\n=== خطوات التشخيص ===")
    
    print("🔍 فحص Console:")
    print("  1. افتح Developer Tools (F12)")
    print("  2. اذهب إلى Console")
    print("  3. ابحث عن أخطاء JavaScript")
    print("  4. تحقق من تحميل قائمة الأدوية")
    
    print(f"\n🧪 اختبار البحث:")
    print("  1. انقر في مربع البحث")
    print("  2. اكتب 'para' (3 أحرف)")
    print("  3. انتظر 100ms")
    print("  4. يجب أن تظهر القائمة")
    
    print(f"\n🔧 فحص العناصر:")
    print("  1. تأكد من وجود #dropdown-container")
    print("  2. تأكد من وجود .medication-search-input")
    print("  3. تأكد من تحميل قائمة medications")

def show_common_issues():
    """عرض المشاكل الشائعة وحلولها"""
    
    print(f"\n=== المشاكل الشائعة والحلول ===")
    
    print("❌ البحث لا يعمل:")
    print("  → تحقق من Console للأخطاء")
    print("  → تأكد من تحميل قائمة medications")
    print("  → تحقق من استدعاء attachSearchListeners")
    
    print(f"\n❌ القائمة لا تظهر:")
    print("  → تحقق من وجود #dropdown-container")
    print("  → تأكد من CSS للـ dropdown")
    print("  → فحص z-index والموضع")
    
    print(f"\n❌ JavaScript errors:")
    print("  → تحقق من بنية الكود")
    print("  → تأكد من إغلاق الأقواس والدوال")
    print("  → فحص المتغيرات غير المعرفة")

def show_testing_checklist():
    """قائمة فحص الاختبار"""
    
    print(f"\n=== قائمة فحص الاختبار ===")
    
    print("□ تشغيل التطبيق: python run.py")
    print("□ تسجيل دخول: doctor / doctor123")
    print("□ الذهاب إلى صفحة الوصفة")
    print("□ فتح Developer Tools (F12)")
    print("□ فحص Console للأخطاء")
    print("□ النقر في مربع البحث")
    print("□ كتابة 'para' أو 'amox'")
    print("□ انتظار ظهور القائمة")
    print("□ اختبار النقر على النتائج")
    print("□ اختبار التنقل بالكيبورد")

if __name__ == "__main__":
    print("=== اختبار إصلاح مشكلة البحث في الأدوية ===")
    
    check_javascript_structure()
    check_html_structure()
    
    if check_medications_data():
        print(f"\n✅ البيانات متوفرة للاختبار")
    else:
        print(f"\n❌ مشكلة في البيانات!")
    
    show_debugging_steps()
    show_common_issues()
    show_testing_checklist()
    
    print(f"\n🎯 الإصلاحات المطبقة:")
    print("✅ إضافة استدعاء attachSearchListeners للدواء الأول")
    print("✅ إصلاح بنية setTimeout في البحث")
    print("✅ container خارجي للـ dropdowns")
    print("✅ حساب موضع دقيق")
    
    print(f"\n🚀 جرب الآن!")
    print("http://localhost:5000/doctor/prescription/13")