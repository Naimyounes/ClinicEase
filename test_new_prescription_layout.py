#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
اختبار التصميم الجديد لصفحة إنشاء الوصفة الطبية
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

def check_available_visits():
    """فحص الزيارات المتاحة للاختبار"""
    
    with app.app_context():
        print("=== الزيارات المتاحة للاختبار ===")
        
        visits = Visit.query.order_by(Visit.date.desc()).limit(5).all()
        
        if visits:
            print(f"عدد الزيارات المتاحة: {len(visits)}")
            for i, visit in enumerate(visits, 1):
                print(f"{i}. ID: {visit.id}")
                print(f"   المريض: {visit.patient.full_name}")
                print(f"   التاريخ: {visit.date.strftime('%Y-%m-%d %H:%M')}")
                print(f"   الحالة: {visit.status}")
                print(f"   الرابط: http://localhost:5000/doctor/prescription/{visit.id}")
                print()
        else:
            print("❌ لا توجد زيارات للاختبار")

def show_new_layout_features():
    """عرض ميزات التصميم الجديد"""
    
    print("=== ميزات التصميم الجديد ===")
    
    print("✅ 1. إزالة medications-container")
    print("✅ 2. وضع الدواء الأول مباشرة في الـ card")
    print("✅ 3. زر 'إضافة' في الدواء الأول")
    print("✅ 4. تحويل الزر إلى 'حذف' عند الإضافة")
    print("✅ 5. container منفصل للأدوية الإضافية")
    print("✅ 6. تصميم أنظف وأكثر وضوحاً")
    
    print(f"\n=== كيفية العمل ===")
    print("1. الدواء الأول: موجود بالفعل مع زر 'إضافة'")
    print("2. عند النقر على 'إضافة': يتحول إلى 'حذف' ويضاف دواء جديد")
    print("3. الأدوية الجديدة: تظهر مع زر 'حذف' مباشرة")
    print("4. لا يمكن حذف آخر دواء (يجب وجود دواء واحد على الأقل)")

def show_search_functionality():
    """عرض وظيفة البحث"""
    
    with app.app_context():
        print(f"\n=== وظيفة البحث في الأدوية ===")
        
        total_meds = Medication.query.count()
        print(f"إجمالي الأدوية: {total_meds}")
        
        # أمثلة على البحث
        search_examples = [
            ('PARA', 'PARACETAMOL'),
            ('500MG', 'أدوية بجرعة 500mg'),
            ('AMOX', 'AMOXICILLIN'),
            ('CETIRIZINE', 'أدوية الحساسية')
        ]
        
        print(f"\nأمثلة على البحث:")
        for term, description in search_examples:
            results = Medication.query.filter(
                db.or_(
                    Medication.name.like(f'%{term}%'),
                    Medication.dosage.like(f'%{term}%')
                )
            ).limit(3).all()
            
            print(f"• '{term}' ({description}): {len(results)} نتيجة")

def show_css_improvements():
    """عرض تحسينات CSS"""
    
    print(f"\n=== تحسينات CSS المطبقة ===")
    
    print("✅ z-index: 9999 للقائمة المنسدلة")
    print("✅ position: absolute !important")
    print("✅ overflow: visible على جميع الـ containers")
    print("✅ z-index ديناميكي عند التفاعل")
    print("✅ تأثيرات بصرية محسنة")
    print("✅ تصميم responsive للهواتف")
    print("✅ أيقونات Font Awesome")
    print("✅ ألوان Bootstrap محسنة")

def show_testing_checklist():
    """قائمة فحص للاختبار"""
    
    print(f"\n=== قائمة فحص الاختبار ===")
    
    print("🔍 اختبار البحث:")
    print("  □ البحث يعمل بعد كتابة حرفين")
    print("  □ النتائج تظهر فوق جميع العناصر")
    print("  □ يمكن الاختيار بالنقر")
    print("  □ يمكن التنقل بالأسهم + Enter")
    print("  □ يمكن الإغلاق بـ Escape")
    
    print(f"\n➕ اختبار إضافة الأدوية:")
    print("  □ الدواء الأول يظهر مع زر 'إضافة'")
    print("  □ عند النقر: يتحول إلى 'حذف' ويضاف دواء جديد")
    print("  □ الأدوية الجديدة تظهر مع زر 'حذف'")
    print("  □ لا يمكن حذف آخر دواء")
    
    print(f"\n📱 اختبار التوافق:")
    print("  □ يعمل على Chrome/Firefox/Safari/Edge")
    print("  □ يعمل على الهواتف المحمولة")
    print("  □ يعمل على الأجهزة اللوحية")
    print("  □ القائمة تظهر بشكل صحيح على جميع الأحجام")

def show_troubleshooting():
    """دليل حل المشاكل"""
    
    print(f"\n=== حل المشاكل المحتملة ===")
    
    print("❌ القائمة لا تظهر:")
    print("  → تأكد من وجود أدوية في قاعدة البيانات")
    print("  → تحقق من console للأخطاء")
    print("  → تأكد من تحميل JavaScript")
    
    print(f"\n❌ القائمة مخفية:")
    print("  → تم إصلاح z-index إلى 9999")
    print("  → تم إزالة overflow restrictions")
    print("  → تم إضافة positioning محسن")
    
    print(f"\n❌ البحث لا يعمل:")
    print("  → تحقق من تحميل قائمة الأدوية")
    print("  → تأكد من عمل JavaScript")
    print("  → تحقق من console للأخطاء")

if __name__ == "__main__":
    print("=== اختبار التصميم الجديد لصفحة إنشاء الوصفة الطبية ===")
    
    check_available_visits()
    show_new_layout_features()
    show_search_functionality()
    show_css_improvements()
    show_testing_checklist()
    show_troubleshooting()
    
    print(f"\n=== خطوات الاختبار السريع ===")
    print("1. python run.py")
    print("2. تسجيل دخول: doctor / doctor123")
    print("3. http://localhost:5000/doctor/prescription/13")
    print("4. اختبار البحث والإضافة")
    
    print(f"\n🎉 التصميم الجديد جاهز للاختبار!")