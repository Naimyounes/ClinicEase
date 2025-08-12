#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
تحديث قاعدة البيانات لإضافة جداول الوصفات المحددة مسبقاً
"""

import sys
import os

# إضافة مسار المشروع
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from clinic_app import create_app, db
from clinic_app.models import PredefinedPrescription, PredefinedPrescriptionMedication, Medication

def update_database():
    """تحديث قاعدة البيانات"""
    
    print("=== تحديث قاعدة البيانات للوصفات المحددة مسبقاً ===")
    
    app = create_app()
    
    with app.app_context():
        try:
            # إنشاء الجداول الجديدة
            print("إنشاء الجداول الجديدة...")
            db.create_all()
            
            # التحقق من وجود الجداول
            inspector = db.inspect(db.engine)
            tables = inspector.get_table_names()
            
            if 'predefined_prescription' in tables:
                print("✅ جدول predefined_prescription تم إنشاؤه بنجاح")
            else:
                print("❌ فشل في إنشاء جدول predefined_prescription")
            
            if 'predefined_prescription_medication' in tables:
                print("✅ جدول predefined_prescription_medication تم إنشاؤه بنجاح")
            else:
                print("❌ فشل في إنشاء جدول predefined_prescription_medication")
            
            # إضافة بعض الوصفات التجريبية
            print("\nإضافة وصفات تجريبية...")
            
            # التحقق من وجود أدوية
            medications_count = Medication.query.count()
            print(f"عدد الأدوية المتاحة: {medications_count}")
            
            if medications_count > 0:
                # إضافة وصفة للبرد والإنفلونزا
                cold_prescription = PredefinedPrescription.query.filter_by(name="وصفة البرد والإنفلونزا").first()
                if not cold_prescription:
                    cold_prescription = PredefinedPrescription(name="وصفة البرد والإنفلونزا")
                    db.session.add(cold_prescription)
                    db.session.commit()
                    print("✅ تم إضافة وصفة البرد والإنفلونزا")
                
                # إضافة وصفة للصداع
                headache_prescription = PredefinedPrescription.query.filter_by(name="وصفة الصداع").first()
                if not headache_prescription:
                    headache_prescription = PredefinedPrescription(name="وصفة الصداع")
                    db.session.add(headache_prescription)
                    db.session.commit()
                    print("✅ تم إضافة وصفة الصداع")
                
                # إضافة وصفة للحساسية
                allergy_prescription = PredefinedPrescription.query.filter_by(name="وصفة الحساسية").first()
                if not allergy_prescription:
                    allergy_prescription = PredefinedPrescription(name="وصفة الحساسية")
                    db.session.add(allergy_prescription)
                    db.session.commit()
                    print("✅ تم إضافة وصفة الحساسية")
                
                print(f"\nعدد الوصفات المحددة مسبقاً: {PredefinedPrescription.query.count()}")
            else:
                print("⚠️ لا توجد أدوية في قاعدة البيانات")
            
            print("\n🎉 تم تحديث قاعدة البيانات بنجاح!")
            
        except Exception as e:
            print(f"❌ خطأ في تحديث قاعدة البيانات: {e}")
            db.session.rollback()

def show_database_info():
    """عرض معلومات قاعدة البيانات"""
    
    print(f"\n=== معلومات قاعدة البيانات ===")
    
    app = create_app()
    
    with app.app_context():
        try:
            # عرض الجداول
            inspector = db.inspect(db.engine)
            tables = inspector.get_table_names()
            
            print(f"الجداول الموجودة ({len(tables)}):")
            for table in sorted(tables):
                print(f"  • {table}")
            
            # عرض إحصائيات
            print(f"\n=== الإحصائيات ===")
            print(f"عدد الأدوية: {Medication.query.count()}")
            print(f"عدد الوصفات المحددة مسبقاً: {PredefinedPrescription.query.count()}")
            print(f"عدد أدوية الوصفات المحددة مسبقاً: {PredefinedPrescriptionMedication.query.count()}")
            
            # عرض الوصفات المحددة مسبقاً
            prescriptions = PredefinedPrescription.query.all()
            if prescriptions:
                print(f"\n=== الوصفات المحددة مسبقاً ===")
                for prescription in prescriptions:
                    meds_count = len(prescription.medications)
                    print(f"  • {prescription.name} ({meds_count} أدوية)")
            
        except Exception as e:
            print(f"❌ خطأ في عرض معلومات قاعدة البيانات: {e}")

if __name__ == "__main__":
    print("=== تحديث قاعدة البيانات للوصفات المحددة مسبقاً ===")
    
    update_database()
    show_database_info()
    
    print(f"\n=== التالي ===")
    print("1. شغل الخادم: python run.py")
    print("2. سجل دخول كطبيب: doctor / doctor123")
    print("3. اذهب إلى: http://localhost:5000/doctor/predefined_prescriptions")
    print("4. جرب الوظائف الجديدة!")