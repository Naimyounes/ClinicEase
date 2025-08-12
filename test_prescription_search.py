#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
اختبار تحسينات صفحة إنشاء الوصفة الطبية
"""

import sys
import os

# إضافة مسار المشروع
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# استيراد التطبيق والنماذج
from clinic_app import create_app, db
from clinic_app.models import Medication, Visit, Patient

# إنشاء التطبيق
app = create_app()

def test_medications_for_prescription():
    """اختبار الأدوية المتاحة للوصفة الطبية"""
    
    with app.app_context():
        print("=== اختبار الأدوية للوصفة الطبية ===")
        
        # إجمالي الأدوية
        total_medications = Medication.query.count()
        print(f"إجمالي الأدوية المتاحة: {total_medications}")
        
        # عينة من الأدوية الشائعة
        common_medications = [
            'PARACETAMOL',
            'IBUPROFEN', 
            'AMOXICILLIN',
            'CETIRIZINE',
            'OMEPRAZOLE'
        ]
        
        print(f"\n=== البحث عن أدوية شائعة ===")
        for med_name in common_medications:
            results = Medication.query.filter(
                Medication.name.like(f'%{med_name}%')
            ).limit(5).all()
            
            print(f"\n{med_name}: {len(results)} نتيجة")
            for i, med in enumerate(results, 1):
                dosage_info = f" ({med.dosage})" if med.dosage else ""
                print(f"  {i}. ID:{med.id} - {med.name}{dosage_info}")

def test_visit_data():
    """اختبار بيانات الزيارات"""
    
    with app.app_context():
        print(f"\n=== اختبار بيانات الزيارات ===")
        
        # عدد الزيارات
        total_visits = Visit.query.count()
        print(f"إجمالي الزيارات: {total_visits}")
        
        if total_visits > 0:
            # أحدث زيارة
            latest_visit = Visit.query.order_by(Visit.date.desc()).first()
            print(f"\nأحدث زيارة:")
            print(f"  - ID: {latest_visit.id}")
            print(f"  - المريض: {latest_visit.patient.full_name}")
            print(f"  - التاريخ: {latest_visit.date}")
            print(f"  - الحالة: {latest_visit.status}")
            
            # رابط إنشاء الوصفة
            print(f"\nرابط إنشاء الوصفة:")
            print(f"http://localhost:5000/doctor/prescription/{latest_visit.id}")
        else:
            print("لا توجد زيارات في قاعدة البيانات")

def show_search_examples():
    """عرض أمثلة على البحث"""
    
    with app.app_context():
        print(f"\n=== أمثلة على البحث في الأدوية ===")
        
        search_terms = ['PARA', 'MG', '500', 'AMOX', 'CETIRIZINE']
        
        for term in search_terms:
            results = Medication.query.filter(
                db.or_(
                    Medication.name.like(f'%{term}%'),
                    Medication.dosage.like(f'%{term}%')
                )
            ).limit(3).all()
            
            print(f"\nبحث عن '{term}': {len(results)} نتيجة")
            for med in results:
                dosage_info = f" - {med.dosage}" if med.dosage else ""
                print(f"  • {med.name}{dosage_info}")

def generate_test_data():
    """إنشاء بيانات تجريبية إذا لزم الأمر"""
    
    with app.app_context():
        print(f"\n=== فحص البيانات التجريبية ===")
        
        # فحص وجود مرضى
        patients_count = Patient.query.count()
        print(f"عدد المرضى: {patients_count}")
        
        # فحص وجود زيارات
        visits_count = Visit.query.count()
        print(f"عدد الزيارات: {visits_count}")
        
        if visits_count == 0:
            print("\n⚠️  لا توجد زيارات لاختبار إنشاء الوصفة الطبية")
            print("يمكنك إنشاء زيارة جديدة من خلال:")
            print("1. تسجيل الدخول كطبيب")
            print("2. الذهاب إلى قائمة المرضى")
            print("3. إنشاء زيارة جديدة")

def show_features():
    """عرض الميزات الجديدة"""
    
    print(f"\n=== الميزات الجديدة في صفحة إنشاء الوصفة ===")
    print("✅ مربع بحث للأدوية بدلاً من القائمة المنسدلة")
    print("✅ بحث فوري أثناء الكتابة")
    print("✅ عرض أول 10 نتائج مع إمكانية رؤية المزيد")
    print("✅ التنقل بالكيبورد (أسهم + Enter + Escape)")
    print("✅ عرض الدواء المحدد مع إمكانية المسح")
    print("✅ تصميم محسن مع أيقونات")
    print("✅ تأثيرات بصرية وانيميشن")
    print("✅ دعم الهواتف المحمولة")
    print("✅ ترجمة كاملة للفرنسية")
    
    print(f"\n=== كيفية الاستخدام ===")
    print("1. اكتب اسم الدواء أو جزء منه")
    print("2. اختر من القائمة المنسدلة")
    print("3. أو استخدم الأسهم + Enter للاختيار")
    print("4. يمكن مسح الاختيار والبحث مرة أخرى")

if __name__ == "__main__":
    print("=== اختبار تحسينات صفحة إنشاء الوصفة الطبية ===")
    
    test_medications_for_prescription()
    test_visit_data()
    show_search_examples()
    generate_test_data()
    show_features()
    
    print(f"\n=== للاختبار ===")
    print("1. شغل التطبيق: python run.py")
    print("2. سجل دخول كطبيب: doctor / doctor123")
    print("3. اذهب إلى زيارة مريض")
    print("4. انقر على 'إنشاء وصفة طبية'")
    print("5. جرب البحث في الأدوية!")
    
    print(f"\n✅ تم تحسين صفحة إنشاء الوصفة الطبية بنجاح!")