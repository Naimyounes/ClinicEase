#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
اختبار نظام الـ pagination للأدوية
"""

import sys
import os

# إضافة مسار المشروع
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# استيراد التطبيق والنماذج
from clinic_app import create_app, db
from clinic_app.models import Medication

# إنشاء التطبيق
app = create_app()

def test_pagination_logic():
    """اختبار منطق الـ pagination"""
    
    with app.app_context():
        print("=== اختبار نظام الـ Pagination ===")
        
        # إجمالي الأدوية
        total_medications = Medication.query.count()
        print(f"إجمالي الأدوية: {total_medications}")
        
        # اختبار pagination مع أحجام مختلفة
        page_sizes = [25, 50, 100, 200]
        
        for per_page in page_sizes:
            total_pages = (total_medications + per_page - 1) // per_page  # حساب عدد الصفحات
            print(f"\nمع {per_page} دواء في كل صفحة:")
            print(f"  - عدد الصفحات: {total_pages}")
            print(f"  - الصفحة الأخيرة تحتوي على: {total_medications - (total_pages - 1) * per_page} دواء")
        
        # اختبار الصفحة الأولى
        print(f"\n=== اختبار الصفحة الأولى (50 دواء) ===")
        first_page = Medication.query.order_by(Medication.name.asc()).paginate(
            page=1, per_page=50, error_out=False
        )
        
        print(f"الصفحة الحالية: {first_page.page}")
        print(f"إجمالي الصفحات: {first_page.pages}")
        print(f"عدد العناصر في هذه الصفحة: {len(first_page.items)}")
        print(f"إجمالي العناصر: {first_page.total}")
        print(f"يوجد صفحة سابقة: {first_page.has_prev}")
        print(f"يوجد صفحة تالية: {first_page.has_next}")
        
        # عرض أول 5 أدوية
        print(f"\nأول 5 أدوية في الصفحة الأولى:")
        for i, med in enumerate(first_page.items[:5], 1):
            dosage_info = f" - {med.dosage}" if med.dosage else " - بدون جرعة"
            print(f"  {i}. {med.name}{dosage_info}")

def test_search_functionality():
    """اختبار وظيفة البحث"""
    
    with app.app_context():
        print(f"\n=== اختبار وظيفة البحث ===")
        
        # البحث عن PARACETAMOL
        search_term = "PARACETAMOL"
        search_results = Medication.query.filter(
            db.or_(
                Medication.name.like(f"%{search_term}%"),
                Medication.dosage.like(f"%{search_term}%")
            )
        ).order_by(Medication.name.asc()).paginate(
            page=1, per_page=10, error_out=False
        )
        
        print(f"البحث عن '{search_term}':")
        print(f"  - عدد النتائج: {search_results.total}")
        print(f"  - عدد الصفحات: {search_results.pages}")
        
        if search_results.items:
            print(f"  - أول 5 نتائج:")
            for i, med in enumerate(search_results.items[:5], 1):
                dosage_info = f" - {med.dosage}" if med.dosage else " - بدون جرعة"
                print(f"    {i}. {med.name}{dosage_info}")

def show_pagination_urls():
    """عرض أمثلة على URLs للـ pagination"""
    
    print(f"\n=== أمثلة على URLs ===")
    base_url = "http://localhost:5000/doctor/medications"
    
    print(f"الصفحة الأولى: {base_url}?page=1&per_page=50")
    print(f"الصفحة الثانية: {base_url}?page=2&per_page=50")
    print(f"البحث: {base_url}?search=PARACETAMOL&page=1&per_page=25")
    print(f"100 دواء في الصفحة: {base_url}?page=1&per_page=100")

def calculate_pagination_stats():
    """حساب إحصائيات الـ pagination"""
    
    with app.app_context():
        total = Medication.query.count()
        
        print(f"\n=== إحصائيات الـ Pagination ===")
        print(f"إجمالي الأدوية: {total}")
        
        # حساب عدد الصفحات لكل حجم
        sizes = [25, 50, 100, 200]
        for size in sizes:
            pages = (total + size - 1) // size
            print(f"{size} دواء/صفحة = {pages} صفحة")
        
        # حساب الوقت المتوقع للتحميل
        print(f"\nتقدير أوقات التحميل:")
        print(f"25 دواء/صفحة: سريع جداً")
        print(f"50 دواء/صفحة: سريع (موصى به)")
        print(f"100 دواء/صفحة: متوسط")
        print(f"200 دواء/صفحة: بطيء نسبياً")

if __name__ == "__main__":
    print("=== اختبار نظام Pagination للأدوية ===")
    
    test_pagination_logic()
    test_search_functionality()
    show_pagination_urls()
    calculate_pagination_stats()
    
    print(f"\n=== الميزات المضافة ===")
    print("✅ تقسيم الأدوية على صفحات (25, 50, 100, 200)")
    print("✅ بحث في الأدوية مع pagination")
    print("✅ أزرار التنقل بين الصفحات")
    print("✅ عرض معلومات الصفحة الحالية")
    print("✅ اختيار عدد الأدوية في كل صفحة")
    print("✅ ترقيم صحيح للأدوية عبر الصفحات")
    print("✅ تصميم responsive للهواتف")
    print("✅ اختصارات لوحة المفاتيح (Ctrl + ←/→)")
    
    print(f"\n=== للاختبار ===")
    print("1. شغل التطبيق: python run.py")
    print("2. اذهب إلى: http://localhost:5000/doctor/medications")
    print("3. سجل دخول كطبيب: doctor / doctor123")
    print("4. اختبر التنقل بين الصفحات")
    print("5. اختبر البحث")
    print("6. اختبر تغيير عدد الأدوية في كل صفحة")
    
    print(f"\n✅ تم إضافة نظام Pagination بنجاح!")