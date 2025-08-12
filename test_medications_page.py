#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
سكريپت لاختبار صفحة الأدوية
"""

import sys
import os

# إضافة مسار المشروع
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# استيراد التطبيق والنماذج
from clinic_app import create_app, db
from clinic_app.models import Medication, User

# إنشاء التطبيق
app = create_app()

def test_medications_functionality():
    """اختبار وظائف الأدوية"""
    
    with app.app_context():
        print("=== اختبار صفحة الأدوية ===")
        
        # عدد الأدوية الحالي
        total_medications = Medication.query.count()
        print(f"إجمالي الأدوية في قاعدة البيانات: {total_medications}")
        
        # اختبار إضافة دواء جديد
        test_medication = Medication(
            name="TEST_PARACETAMOL_FRENCH",
            dosage="500mg"
        )
        
        try:
            db.session.add(test_medication)
            db.session.commit()
            print("✅ تم إضافة دواء تجريبي بنجاح")
            
            # اختبار حذف الدواء
            db.session.delete(test_medication)
            db.session.commit()
            print("✅ تم حذف الدواء التجريبي بنجاح")
            
        except Exception as e:
            db.session.rollback()
            print(f"❌ خطأ في اختبار الأدوية: {e}")
        
        # عرض عينة من الأدوية
        print(f"\n=== عينة من الأدوية (أول 10) ===")
        sample_medications = Medication.query.limit(10).all()
        
        for i, med in enumerate(sample_medications, 1):
            dosage_info = f" - {med.dosage}" if med.dosage else " - بدون جرعة"
            print(f"{i:2d}. ID:{med.id} | {med.name}{dosage_info}")
        
        # التحقق من المستخدمين
        print(f"\n=== المستخدمون المسجلون ===")
        users = User.query.all()
        for user in users:
            print(f"- {user.username} ({user.role})")

def show_database_info():
    """عرض معلومات قاعدة البيانات"""
    
    with app.app_context():
        print(f"\n=== معلومات قاعدة البيانات ===")
        
        # إحصائيات الأدوية
        total_medications = Medication.query.count()
        print(f"إجمالي الأدوية: {total_medications}")
        
        # أدوية بدون جرعة
        no_dosage = Medication.query.filter(
            (Medication.dosage == None) | (Medication.dosage == '')
        ).count()
        print(f"أدوية بدون جرعة: {no_dosage}")
        print(f"أدوية بجرعة: {total_medications - no_dosage}")
        
        # إحصائيات المستخدمين
        total_users = User.query.count()
        doctors = User.query.filter_by(role='doctor').count()
        secretaries = User.query.filter_by(role='secretary').count()
        
        print(f"\nإجمالي المستخدمين: {total_users}")
        print(f"أطباء: {doctors}")
        print(f"سكرتيرات: {secretaries}")

if __name__ == "__main__":
    print("=== اختبار صفحة الأدوية ===")
    
    test_medications_functionality()
    show_database_info()
    
    print(f"\n=== تعليمات الاختبار ===")
    print("1. تشغيل التطبيق: python run.py")
    print("2. تسجيل الدخول كطبيب: username=doctor, password=doctor123")
    print("3. الذهاب إلى: http://localhost:5000/doctor/medications")
    print("4. اختبار إضافة دواء جديد")
    print("5. اختبار حذف دواء (يجب أن يعمل زر الحذف الآن)")
    print("6. اختبار البحث في الأدوية")
    
    print(f"\n✅ تم الانتهاء من الاختبار!")