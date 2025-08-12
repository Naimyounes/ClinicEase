#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
سكريپت لتحليل بيانات ملف Excel بالتفصيل
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

def analyze_excel_file():
    """تحليل مفصل لملف Excel"""
    excel_file = 'clinic_app/static/médicament.xlsx'
    
    try:
        # قراءة ملف Excel
        df = pd.read_excel(excel_file)
        
        print("=== تحليل ملف Excel ===")
        print(f"إجمالي الصفوف: {len(df)}")
        print(f"أسماء الأعمدة: {list(df.columns)}")
        
        # تحديد أعمدة الاسم والجرعة
        name_column = df.columns[0]
        dosage_column = df.columns[1] if len(df.columns) > 1 else None
        
        print(f"عمود الاسم: {name_column}")
        print(f"عمود الجرعة: {dosage_column}")
        
        # تحليل البيانات
        print(f"\n=== تحليل البيانات ===")
        
        # الصفوف الفارغة
        empty_names = df[df[name_column].isna() | (df[name_column] == '') | (df[name_column].astype(str).str.strip() == '')].shape[0]
        print(f"صفوف بأسماء فارغة: {empty_names}")
        
        # الصفوف الصالحة
        valid_rows = df[~(df[name_column].isna() | (df[name_column] == '') | (df[name_column].astype(str).str.strip() == ''))].copy()
        print(f"صفوف صالحة: {len(valid_rows)}")
        
        # تنظيف أسماء الأدوية
        valid_rows['clean_name'] = valid_rows[name_column].astype(str).str.strip()
        
        # الأسماء الفريدة
        unique_names = valid_rows['clean_name'].nunique()
        print(f"أسماء فريدة: {unique_names}")
        
        # الأسماء المكررة
        duplicated_names = valid_rows['clean_name'].duplicated().sum()
        print(f"أسماء مكررة: {duplicated_names}")
        
        # عرض أكثر الأسماء تكراراً
        print(f"\n=== أكثر الأدوية تكراراً ===")
        top_duplicates = valid_rows['clean_name'].value_counts().head(10)
        for name, count in top_duplicates.items():
            if count > 1:
                print(f"{name}: {count} مرة")
        
        # تحليل الجرعات
        if dosage_column:
            print(f"\n=== تحليل الجرعات ===")
            empty_dosages = valid_rows[valid_rows[dosage_column].isna() | (valid_rows[dosage_column] == '')].shape[0]
            print(f"صفوف بجرعات فارغة: {empty_dosages}")
            print(f"صفوف بجرعات صالحة: {len(valid_rows) - empty_dosages}")
        
        # عرض عينة من البيانات
        print(f"\n=== عينة من البيانات ===")
        sample_data = valid_rows.head(20)
        for idx, row in sample_data.iterrows():
            name = row['clean_name']
            dosage = row[dosage_column] if dosage_column and not pd.isna(row[dosage_column]) else "بدون جرعة"
            print(f"{idx+1:3d}. {name} - {dosage}")
        
        return valid_rows
        
    except Exception as e:
        print(f"خطأ في قراءة ملف Excel: {e}")
        return None

def compare_with_database():
    """مقارنة بيانات Excel مع قاعدة البيانات"""
    
    # تحليل ملف Excel
    excel_data = analyze_excel_file()
    if excel_data is None:
        return
    
    with app.app_context():
        # الحصول على الأدوية من قاعدة البيانات
        db_medications = Medication.query.all()
        db_names = set(med.name.strip() for med in db_medications)
        
        print(f"\n=== مقارنة مع قاعدة البيانات ===")
        print(f"أدوية في قاعدة البيانات: {len(db_names)}")
        
        # الأسماء الفريدة في Excel
        excel_names = set(excel_data['clean_name'].unique())
        print(f"أسماء فريدة في Excel: {len(excel_names)}")
        
        # الأسماء المفقودة
        missing_names = excel_names - db_names
        print(f"أسماء مفقودة من قاعدة البيانات: {len(missing_names)}")
        
        if missing_names:
            print(f"\n=== أول 20 اسم مفقود ===")
            for i, name in enumerate(list(missing_names)[:20], 1):
                print(f"{i:2d}. {name}")
        
        # الأسماء الموجودة
        existing_names = excel_names & db_names
        print(f"\nأسماء موجودة في قاعدة البيانات: {len(existing_names)}")
        
        return missing_names, excel_data

def import_missing_medications():
    """استيراد الأدوية المفقودة فقط"""
    
    missing_names, excel_data = compare_with_database()
    
    if not missing_names:
        print("جميع الأدوية موجودة في قاعدة البيانات!")
        return
    
    print(f"\n=== استيراد {len(missing_names)} دواء مفقود ===")
    
    name_column = excel_data.columns[0]
    dosage_column = excel_data.columns[1] if len(excel_data.columns) > 1 else None
    
    with app.app_context():
        added_count = 0
        
        # معالجة كل صف في Excel
        for idx, row in excel_data.iterrows():
            try:
                medication_name = str(row['clean_name']).strip()
                
                # تخطي إذا كان الاسم موجود في قاعدة البيانات
                if medication_name not in missing_names:
                    continue
                
                # الحصول على الجرعة
                dosage = ''
                if dosage_column and not pd.isna(row[dosage_column]):
                    dosage = str(row[dosage_column]).strip()
                
                # التحقق من عدم وجود الدواء (للتأكد)
                existing = Medication.query.filter_by(name=medication_name).first()
                if existing:
                    continue
                
                # إضافة الدواء الجديد
                new_medication = Medication(
                    name=medication_name,
                    dosage=dosage if dosage else None
                )
                
                db.session.add(new_medication)
                added_count += 1
                print(f"تم إضافة: {medication_name} - {dosage}")
                
                # حفظ كل 100 دواء
                if added_count % 100 == 0:
                    db.session.commit()
                    print(f"تم حفظ {added_count} دواء...")
                
            except Exception as e:
                print(f"خطأ في معالجة الصف {idx + 1}: {e}")
                continue
        
        # حفظ الباقي
        try:
            db.session.commit()
            print(f"\n=== النتائج النهائية ===")
            print(f"تم إضافة {added_count} دواء جديد")
            print(f"إجمالي الأدوية في قاعدة البيانات: {Medication.query.count()}")
            
        except Exception as e:
            db.session.rollback()
            print(f"خطأ في حفظ البيانات: {e}")

def create_unique_medications_list():
    """إنشاء قائمة فريدة من الأدوية من Excel"""
    
    excel_file = 'clinic_app/static/médicament.xlsx'
    
    try:
        # قراءة ملف Excel
        df = pd.read_excel(excel_file)
        
        name_column = df.columns[0]
        dosage_column = df.columns[1] if len(df.columns) > 1 else None
        
        # تنظيف البيانات
        valid_rows = df[~(df[name_column].isna() | (df[name_column] == '') | (df[name_column].astype(str).str.strip() == ''))].copy()
        valid_rows['clean_name'] = valid_rows[name_column].astype(str).str.strip()
        
        # إنشاء قائمة فريدة
        unique_medications = []
        seen_names = set()
        
        for idx, row in valid_rows.iterrows():
            name = row['clean_name']
            
            if name not in seen_names:
                dosage = ''
                if dosage_column and not pd.isna(row[dosage_column]):
                    dosage = str(row[dosage_column]).strip()
                
                unique_medications.append({
                    'name': name,
                    'dosage': dosage
                })
                seen_names.add(name)
        
        print(f"=== قائمة الأدوية الفريدة ===")
        print(f"إجمالي الأدوية في Excel: {len(df)}")
        print(f"أدوية صالحة: {len(valid_rows)}")
        print(f"أدوية فريدة: {len(unique_medications)}")
        
        # حفظ القائمة الفريدة
        unique_df = pd.DataFrame(unique_medications)
        unique_df.to_excel('unique_medications.xlsx', index=False)
        print(f"تم حفظ القائمة الفريدة في ملف 'unique_medications.xlsx'")
        
        return unique_medications
        
    except Exception as e:
        print(f"خطأ: {e}")
        return None

if __name__ == "__main__":
    print("=== تحليل بيانات الأدوية ===")
    
    while True:
        print("\nاختر العملية:")
        print("1. تحليل ملف Excel")
        print("2. مقارنة مع قاعدة البيانات")
        print("3. استيراد الأدوية المفقودة")
        print("4. إنشاء قائمة فريدة من Excel")
        print("0. خروج")
        
        choice = input("\nأدخل اختيارك (0-4): ").strip()
        
        if choice == '0':
            break
        elif choice == '1':
            analyze_excel_file()
        elif choice == '2':
            compare_with_database()
        elif choice == '3':
            import_missing_medications()
        elif choice == '4':
            create_unique_medications_list()
        else:
            print("اختيار غير صحيح. حاول مرة أخرى.")
    
    print("تم الانتهاء من التحليل.")