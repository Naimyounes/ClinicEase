#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
سكريپت لرفع جميع الأدوية من ملف Excel كما هي بدون أي تعديل
"""

import pandas as pd
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

def recreate_medication_table_simple():
    """إعادة إنشاء جدول الأدوية بدون قيود فريدة"""
    
    # الحصول على مسار قاعدة البيانات
    db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'instance', 'clinic.db')
    
    try:
        # الاتصال بقاعدة البيانات مباشرة
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        print("1. حذف جدول الأدوية القديم...")
        cursor.execute("DROP TABLE IF EXISTS medication")
        
        print("2. إنشاء جدول الأدوية الجديد (بدون قيود فريدة)...")
        cursor.execute("""
            CREATE TABLE medication (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name VARCHAR(100) NOT NULL,
                dosage VARCHAR(100)
            )
        """)
        
        conn.commit()
        conn.close()
        
        print("تم إعادة إنشاء جدول الأدوية بنجاح!")
        return True
        
    except Exception as e:
        print(f"خطأ في إعادة إنشاء الجدول: {e}")
        return False

def import_all_medications_exactly():
    """استيراد جميع الأدوية من Excel كما هي تماماً"""
    
    excel_file = 'clinic_app/static/médicament.xlsx'
    
    try:
        # قراءة ملف Excel
        df = pd.read_excel(excel_file)
        print(f"تم قراءة {len(df)} صف من ملف Excel")
        
        name_column = df.columns[0]
        dosage_column = df.columns[1] if len(df.columns) > 1 else None
        
        print(f"عمود الاسم: {name_column}")
        print(f"عمود الجرعة: {dosage_column}")
        
        with app.app_context():
            # إنشاء الجداول
            db.create_all()
            
            added_count = 0
            skipped_count = 0
            error_count = 0
            
            print("\nبدء استيراد الأدوية...")
            
            # معالجة كل صف بدون أي فلترة
            for index, row in df.iterrows():
                try:
                    # الحصول على اسم الدواء
                    medication_name = str(row[name_column]).strip()
                    
                    # تخطي الصفوف الفارغة فقط
                    if pd.isna(row[name_column]) or medication_name == '' or medication_name.lower() == 'nan':
                        skipped_count += 1
                        continue
                    
                    # الحصول على الجرعة
                    dosage = ''
                    if dosage_column and not pd.isna(row[dosage_column]):
                        dosage = str(row[dosage_column]).strip()
                    
                    # إضافة الدواء بدون أي تحقق من التكرار
                    new_medication = Medication(
                        name=medication_name,
                        dosage=dosage if dosage else None
                    )
                    
                    db.session.add(new_medication)
                    added_count += 1
                    
                    # طباعة التقدم كل 200 دواء
                    if added_count % 200 == 0:
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
                print(f"تم إضافة {added_count} دواء")
                print(f"تم تخطي {skipped_count} صف فارغ")
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

def show_import_statistics():
    """عرض إحصائيات الاستيراد"""
    
    with app.app_context():
        total = Medication.query.count()
        
        print(f"\n=== إحصائيات الاستيراد ===")
        print(f"إجمالي الأدوية المستوردة: {total}")
        
        # أدوية بدون جرعة
        no_dosage = Medication.query.filter(
            (Medication.dosage == None) | (Medication.dosage == '')
        ).count()
        print(f"أدوية بدون جرعة: {no_dosage}")
        print(f"أدوية بجرعة: {total - no_dosage}")
        
        # عرض أول 10 أدوية
        print(f"\n=== أول 10 أدوية مستوردة ===")
        first_medications = Medication.query.limit(10).all()
        for i, med in enumerate(first_medications, 1):
            dosage_info = f" - {med.dosage}" if med.dosage else " - بدون جرعة"
            print(f"{i:2d}. {med.name}{dosage_info}")
        
        # عرض آخر 10 أدوية
        print(f"\n=== آخر 10 أدوية مستوردة ===")
        last_medications = Medication.query.order_by(Medication.id.desc()).limit(10).all()
        for i, med in enumerate(last_medications, 1):
            dosage_info = f" - {med.dosage}" if med.dosage else " - بدون جرعة"
            print(f"{i:2d}. {med.name}{dosage_info}")

def verify_total_count():
    """التحقق من العدد الإجمالي"""
    
    excel_file = 'clinic_app/static/médicament.xlsx'
    
    try:
        # قراءة ملف Excel
        df = pd.read_excel(excel_file)
        excel_rows = len(df)
        
        # عد الصفوف الفارغة
        name_column = df.columns[0]
        empty_rows = df[df[name_column].isna() | (df[name_column] == '') | (df[name_column].astype(str).str.strip() == '')].shape[0]
        valid_rows = excel_rows - empty_rows
        
        with app.app_context():
            db_count = Medication.query.count()
            
            print(f"\n=== التحقق من العدد ===")
            print(f"صفوف في ملف Excel: {excel_rows}")
            print(f"صفوف فارغة: {empty_rows}")
            print(f"صفوف صالحة في Excel: {valid_rows}")
            print(f"أدوية في قاعدة البيانات: {db_count}")
            
            if db_count == valid_rows:
                print("✅ تم استيراد جميع الأدوية بنجاح!")
            else:
                print(f"⚠️ هناك فرق: {valid_rows - db_count} دواء")
                
    except Exception as e:
        print(f"خطأ في التحقق: {e}")

if __name__ == "__main__":
    print("=== استيراد جميع الأدوية كما هي ===")
    print("سيتم استيراد جميع الأدوية من ملف Excel بدون أي تعديل أو حذف")
    
    confirm = input("هل تريد المتابعة؟ (اكتب 'نعم' للمتابعة): ")
    
    if confirm.lower() in ['نعم', 'yes', 'y']:
        print("\n1. إعادة إنشاء جدول الأدوية...")
        if recreate_medication_table_simple():
            print("\n2. استيراد جميع الأدوية...")
            if import_all_medications_exactly():
                print("\n3. عرض الإحصائيات...")
                show_import_statistics()
                print("\n4. التحقق من العدد...")
                verify_total_count()
                print("\n✅ تم الانتهاء بنجاح!")
            else:
                print("❌ فشل في استيراد الأدوية!")
        else:
            print("❌ فشل في إعادة إنشاء الجدول!")
    else:
        print("تم إلغاء العملية.")