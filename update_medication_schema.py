#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
سكريپت لتحديث هيكل جدول الأدوية لدعم الأدوية بنفس الاسم وجرعات مختلفة
"""

import sys
import os
import sqlite3

# إضافة مسار المشروع
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# استيراد التطبيق والنماذج
from clinic_app import create_app, db
from clinic_app.models import Medication

# إنشاء التطبيق
app = create_app()

def backup_current_medications():
    """نسخ احتياطي من الأدوية الحالية"""
    
    with app.app_context():
        medications = Medication.query.all()
        backup_data = []
        
        for med in medications:
            backup_data.append({
                'id': med.id,
                'name': med.name,
                'dosage': med.dosage
            })
        
        print(f"تم إنشاء نسخة احتياطية من {len(backup_data)} دواء")
        return backup_data

def recreate_medication_table():
    """إعادة إنشاء جدول الأدوية بالهيكل الجديد"""
    
    # الحصول على مسار قاعدة البيانات
    db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'instance', 'clinic.db')
    
    try:
        # الاتصال بقاعدة البيانات مباشرة
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        print("1. حذف جدول الأدوية القديم...")
        cursor.execute("DROP TABLE IF EXISTS medication")
        
        print("2. إنشاء جدول الأدوية الجديد...")
        cursor.execute("""
            CREATE TABLE medication (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name VARCHAR(100) NOT NULL,
                dosage VARCHAR(100),
                CONSTRAINT unique_medication UNIQUE (name, dosage)
            )
        """)
        
        conn.commit()
        conn.close()
        
        print("تم إعادة إنشاء جدول الأدوية بنجاح!")
        return True
        
    except Exception as e:
        print(f"خطأ في إعادة إنشاء الجدول: {e}")
        return False

def import_medications_with_new_schema():
    """استيراد الأدوية مع الهيكل الجديد"""
    
    import pandas as pd
    
    excel_file = 'clinic_app/static/médicament.xlsx'
    
    try:
        # قراءة ملف Excel
        df = pd.read_excel(excel_file)
        print(f"تم قراءة {len(df)} صف من ملف Excel")
        
        name_column = df.columns[0]
        dosage_column = df.columns[1] if len(df.columns) > 1 else None
        
        with app.app_context():
            # إنشاء الجداول (سيتم إنشاء جدول الأدوية بالهيكل الجديد)
            db.create_all()
            
            added_count = 0
            skipped_count = 0
            error_count = 0
            
            # تتبع المزيجات المضافة
            added_combinations = set()
            
            # معالجة كل صف
            for index, row in df.iterrows():
                try:
                    # الحصول على اسم الدواء
                    medication_name = str(row[name_column]).strip()
                    
                    # تخطي الصفوف الفارغة
                    if pd.isna(row[name_column]) or medication_name == '' or medication_name.lower() == 'nan':
                        skipped_count += 1
                        continue
                    
                    # الحصول على الجرعة
                    dosage = ''
                    if dosage_column and not pd.isna(row[dosage_column]):
                        dosage = str(row[dosage_column]).strip()
                    
                    # إنشاء مفتاح فريد للمزيج
                    combination_key = (medication_name, dosage)
                    
                    # تخطي إذا تم إضافة هذا المزيج مسبقاً
                    if combination_key in added_combinations:
                        skipped_count += 1
                        continue
                    
                    # إضافة الدواء الجديد
                    new_medication = Medication(
                        name=medication_name,
                        dosage=dosage if dosage else None
                    )
                    
                    db.session.add(new_medication)
                    added_combinations.add(combination_key)
                    added_count += 1
                    
                    # طباعة التقدم كل 100 دواء
                    if added_count % 100 == 0:
                        print(f"تم إضافة {added_count} دواء...")
                        db.session.commit()  # حفظ مؤقت
                    
                except Exception as e:
                    error_count += 1
                    print(f"خطأ في الصف {index + 1}: {e}")
                    db.session.rollback()
                    continue
            
            # حفظ الباقي
            try:
                db.session.commit()
                
                print(f"\n=== النتائج النهائية ===")
                print(f"تم إضافة {added_count} دواء فريد")
                print(f"تم تخطي {skipped_count} صف (فارغ أو مكرر)")
                print(f"أخطاء: {error_count}")
                print(f"إجمالي الأدوية في قاعدة البيانات: {Medication.query.count()}")
                
                return True
                
            except Exception as e:
                db.session.rollback()
                print(f"خطأ في حفظ البيانات: {e}")
                return False
                
    except Exception as e:
        print(f"خطأ في قراءة ملف Excel: {e}")
        return False

def verify_new_schema():
    """التحقق من الهيكل الجديد"""
    
    with app.app_context():
        # اختبار إضافة أدوية بنفس الاسم وجرعات مختلفة
        try:
            # محاولة إضافة دوائين بنفس الاسم وجرعات مختلفة
            med1 = Medication(name="TEST_PARACETAMOL", dosage="500MG")
            med2 = Medication(name="TEST_PARACETAMOL", dosage="100MG")
            
            db.session.add(med1)
            db.session.add(med2)
            db.session.commit()
            
            print("✅ اختبار نجح: يمكن إضافة أدوية بنفس الاسم وجرعات مختلفة")
            
            # حذف الأدوية التجريبية
            Medication.query.filter(Medication.name == "TEST_PARACETAMOL").delete()
            db.session.commit()
            
            return True
            
        except Exception as e:
            db.session.rollback()
            print(f"❌ اختبار فشل: {e}")
            return False

def show_sample_results():
    """عرض عينة من النتائج"""
    
    with app.app_context():
        print(f"\n=== عينة من الأدوية المستوردة ===")
        
        # البحث عن أدوية بنفس الاسم وجرعات مختلفة
        common_names = ['PARACETAMOL', 'IBUPROFEN', 'AMOXICILLIN']
        
        for name in common_names:
            medications = Medication.query.filter(
                Medication.name.like(f'%{name}%')
            ).limit(5).all()
            
            if medications:
                print(f"\n{name}:")
                for med in medications:
                    dosage_info = f" - {med.dosage}" if med.dosage else " - بدون جرعة"
                    print(f"  • {med.name}{dosage_info}")

if __name__ == "__main__":
    print("=== تحديث هيكل جدول الأدوية ===")
    print("سيتم إعادة إنشاء جدول الأدوية لدعم الأدوية بنفس الاسم وجرعات مختلفة")
    
    confirm = input("هل تريد المتابعة؟ (اكتب 'نعم' للمتابعة): ")
    
    if confirm.lower() in ['نعم', 'yes', 'y']:
        print("\n1. إعادة إنشاء جدول الأدوية...")
        if recreate_medication_table():
            print("\n2. اختبار الهيكل الجديد...")
            if verify_new_schema():
                print("\n3. استيراد الأدوية من ملف Excel...")
                if import_medications_with_new_schema():
                    print("\n4. عرض عينة من النتائج...")
                    show_sample_results()
                    print("\n✅ تم الانتهاء بنجاح!")
                else:
                    print("❌ فشل في استيراد الأدوية!")
            else:
                print("❌ فشل في اختبار الهيكل الجديد!")
        else:
            print("❌ فشل في إعادة إنشاء الجدول!")
    else:
        print("تم إلغاء العملية.")