#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
سكريپت لحذف جميع الأدوية وإعادة استيرادها بطريقة صحيحة
"""

import pandas as pd
import sys
import os

# إضافة مسار المشروع
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# استيراد التطبيق والنماذج
from clinic_app import create_app, db
from clinic_app.models import Medication

# إنشاء التطبيق
app = create_app()

def delete_all_medications():
    """حذف جميع الأدوية من قاعدة البيانات"""
    
    with app.app_context():
        try:
            # عدد الأدوية قبل الحذف
            count_before = Medication.query.count()
            print(f"عدد الأدوية قبل الحذف: {count_before}")
            
            # حذف جميع الأدوية
            Medication.query.delete()
            db.session.commit()
            
            # التحقق من الحذف
            count_after = Medication.query.count()
            print(f"عدد الأدوية بعد الحذف: {count_after}")
            print("تم حذف جميع الأدوية بنجاح!")
            
            return True
            
        except Exception as e:
            db.session.rollback()
            print(f"خطأ في حذف الأدوية: {e}")
            return False

def import_all_medications_correctly():
    """استيراد جميع الأدوية بطريقة صحيحة (الاسم + الجرعة = دواء فريد)"""
    
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
            added_count = 0
            skipped_count = 0
            error_count = 0
            
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
                    
                    # التحقق من وجود الدواء بنفس الاسم والجرعة
                    existing_medication = Medication.query.filter_by(
                        name=medication_name, 
                        dosage=dosage if dosage else None
                    ).first()
                    
                    if existing_medication:
                        skipped_count += 1
                        continue
                    
                    # إضافة الدواء الجديد
                    new_medication = Medication(
                        name=medication_name,
                        dosage=dosage if dosage else None
                    )
                    
                    db.session.add(new_medication)
                    added_count += 1
                    
                    # طباعة التقدم كل 100 دواء
                    if added_count % 100 == 0:
                        print(f"تم إضافة {added_count} دواء...")
                        db.session.commit()  # حفظ مؤقت
                    
                except Exception as e:
                    error_count += 1
                    print(f"خطأ في الصف {index + 1}: {e}")
                    continue
            
            # حفظ الباقي
            try:
                db.session.commit()
                
                print(f"\n=== النتائج النهائية ===")
                print(f"تم إضافة {added_count} دواء جديد")
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

def show_sample_data():
    """عرض عينة من البيانات المستوردة"""
    
    with app.app_context():
        print(f"\n=== عينة من الأدوية المستوردة ===")
        
        # عرض أول 20 دواء
        medications = Medication.query.limit(20).all()
        for i, med in enumerate(medications, 1):
            dosage_info = f" - {med.dosage}" if med.dosage else " - بدون جرعة"
            print(f"{i:2d}. {med.name}{dosage_info}")
        
        # إحصائيات
        total = Medication.query.count()
        no_dosage = Medication.query.filter(
            (Medication.dosage == None) | (Medication.dosage == '')
        ).count()
        
        print(f"\n=== إحصائيات ===")
        print(f"إجمالي الأدوية: {total}")
        print(f"أدوية بدون جرعة: {no_dosage}")
        print(f"أدوية بجرعة: {total - no_dosage}")

def verify_unique_combinations():
    """التحقق من أن كل مزيج (اسم + جرعة) فريد"""
    
    with app.app_context():
        # البحث عن المزيجات المكررة
        duplicates = db.session.query(
            Medication.name,
            Medication.dosage,
            db.func.count(Medication.id).label('count')
        ).group_by(
            Medication.name,
            Medication.dosage
        ).having(
            db.func.count(Medication.id) > 1
        ).all()
        
        print(f"\n=== التحقق من التكرارات ===")
        if duplicates:
            print(f"تم العثور على {len(duplicates)} مزيج مكرر:")
            for name, dosage, count in duplicates:
                dosage_info = f" - {dosage}" if dosage else " - بدون جرعة"
                print(f"'{name}{dosage_info}' ({count} مرة)")
        else:
            print("ممتاز! لا توجد مزيجات مكررة.")

if __name__ == "__main__":
    print("=== إعادة تعيين وإستيراد الأدوية ===")
    print("تحذير: سيتم حذف جميع الأدوية الحالية!")
    
    confirm = input("هل أنت متأكد من المتابعة؟ (اكتب 'نعم' للمتابعة): ")
    
    if confirm.lower() in ['نعم', 'yes', 'y']:
        print("\n1. حذف جميع الأدوية الحالية...")
        if delete_all_medications():
            print("\n2. إستيراد الأدوية من ملف Excel...")
            if import_all_medications_correctly():
                print("\n3. عرض عينة من البيانات...")
                show_sample_data()
                print("\n4. التحقق من التكرارات...")
                verify_unique_combinations()
                print("\nتم الانتهاء بنجاح!")
            else:
                print("فشل في إستيراد الأدوية!")
        else:
            print("فشل في حذف الأدوية الحالية!")
    else:
        print("تم إلغاء العملية.")