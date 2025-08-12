#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
سكريپت لاستيراد الأدوية من ملف Excel إلى قاعدة البيانات
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

def preview_excel_file():
    """معاينة محتوى ملف Excel"""
    excel_file = 'clinic_app/static/médicament.xlsx'
    
    try:
        # قراءة ملف Excel
        df = pd.read_excel(excel_file)
        
        print("=== معاينة ملف Excel ===")
        print(f"عدد الصفوف: {len(df)}")
        print(f"أسماء الأعمدة: {list(df.columns)}")
        print("\n=== أول 10 صفوف ===")
        print(df.head(10))
        
        return df
        
    except Exception as e:
        print(f"خطأ في قراءة ملف Excel: {e}")
        return None

def import_medications_from_excel():
    """استيراد الأدوية من ملف Excel"""
    excel_file = 'clinic_app/static/médicament.xlsx'
    
    try:
        # قراءة ملف Excel
        df = pd.read_excel(excel_file)
        
        print(f"تم العثور على {len(df)} دواء في ملف Excel")
        
        # إنشاء السياق للتطبيق
        with app.app_context():
            # إنشاء الجداول إذا لم تكن موجودة
            db.create_all()
            
            added_count = 0
            skipped_count = 0
            
            # تحديد أسماء الأعمدة (قد تختلف حسب ملف Excel)
            # سنحاول التعرف على الأعمدة تلقائياً
            name_column = None
            dosage_column = None
            
            # البحث عن عمود الاسم
            for col in df.columns:
                col_lower = str(col).lower()
                if any(keyword in col_lower for keyword in ['name', 'nom', 'اسم', 'دواء', 'médicament']):
                    name_column = col
                    break
            
            # البحث عن عمود الجرعة
            for col in df.columns:
                col_lower = str(col).lower()
                if any(keyword in col_lower for keyword in ['dosage', 'dose', 'جرعة', 'تركيز', 'concentration']):
                    dosage_column = col
                    break
            
            if name_column is None:
                print("لم يتم العثور على عمود الاسم. سيتم استخدام العمود الأول.")
                name_column = df.columns[0]
            
            if dosage_column is None and len(df.columns) > 1:
                print("لم يتم العثور على عمود الجرعة. سيتم استخدام العمود الثاني.")
                dosage_column = df.columns[1]
            
            print(f"عمود الاسم: {name_column}")
            print(f"عمود الجرعة: {dosage_column}")
            
            # معالجة كل صف
            for index, row in df.iterrows():
                try:
                    # الحصول على اسم الدواء
                    medication_name = str(row[name_column]).strip()
                    
                    # تخطي الصفوف الفارغة
                    if pd.isna(row[name_column]) or medication_name == '' or medication_name.lower() == 'nan':
                        continue
                    
                    # الحصول على الجرعة
                    dosage = ''
                    if dosage_column and not pd.isna(row[dosage_column]):
                        dosage = str(row[dosage_column]).strip()
                    
                    # التحقق من وجود الدواء مسبقاً
                    existing_medication = Medication.query.filter_by(name=medication_name).first()
                    
                    if existing_medication:
                        print(f"تم تخطي الدواء (موجود مسبقاً): {medication_name}")
                        skipped_count += 1
                        continue
                    
                    # إضافة الدواء الجديد
                    new_medication = Medication(
                        name=medication_name,
                        dosage=dosage if dosage else None
                    )
                    
                    db.session.add(new_medication)
                    added_count += 1
                    print(f"تم إضافة الدواء: {medication_name} - {dosage}")
                    
                except Exception as e:
                    print(f"خطأ في معالجة الصف {index + 1}: {e}")
                    continue
            
            # حفظ التغييرات
            try:
                db.session.commit()
                print(f"\n=== النتائج ===")
                print(f"تم إضافة {added_count} دواء جديد")
                print(f"تم تخطي {skipped_count} دواء (موجود مسبقاً)")
                print(f"إجمالي الأدوية في قاعدة البيانات: {Medication.query.count()}")
                
            except Exception as e:
                db.session.rollback()
                print(f"خطأ في حفظ البيانات: {e}")
                
    except Exception as e:
        print(f"خطأ عام: {e}")

if __name__ == "__main__":
    print("=== استيراد الأدوية من ملف Excel ===")
    
    # معاينة الملف أولاً
    df = preview_excel_file()
    
    if df is not None:
        print("\n" + "="*50)
        response = input("هل تريد المتابعة مع استيراد البيانات؟ (y/n): ")
        
        if response.lower() in ['y', 'yes', 'نعم']:
            import_medications_from_excel()
        else:
            print("تم إلغاء العملية.")
    else:
        print("فشل في قراءة ملف Excel.")