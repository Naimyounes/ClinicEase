#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
سكريپت شامل لإدارة قاعدة بيانات الأدوية
"""

import sys
import os
import pandas as pd

# إضافة مسار المشروع
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# استيراد التطبيق والنماذج
from clinic_app import create_app, db
from clinic_app.models import Medication

# إنشاء التطبيق
app = create_app()

def add_single_medication():
    """إضافة دواء واحد يدوياً"""
    
    print("\n=== إضافة دواء جديد ===")
    name = input("اسم الدواء: ").strip()
    
    if not name:
        print("اسم الدواء مطلوب!")
        return
    
    dosage = input("الجرعة (اختياري): ").strip()
    if not dosage:
        dosage = None
    
    with app.app_context():
        # التحقق من وجود الدواء
        existing = Medication.query.filter_by(name=name).first()
        if existing:
            print(f"الدواء '{name}' موجود بالفعل!")
            return
        
        # إضافة الدواء الجديد
        new_med = Medication(name=name, dosage=dosage)
        
        try:
            db.session.add(new_med)
            db.session.commit()
            print(f"تم إضافة الدواء '{name}' بنجاح!")
        except Exception as e:
            db.session.rollback()
            print(f"خطأ في إضافة الدواء: {e}")

def search_medications():
    """البحث في الأدوية"""
    
    search_term = input("\nأدخل كلمة البحث: ").strip()
    
    if not search_term:
        print("كلمة البحث مطلوبة!")
        return
    
    with app.app_context():
        results = Medication.query.filter(
            Medication.name.like(f'%{search_term}%')
        ).all()
        
        print(f"\n=== نتائج البحث عن '{search_term}' ===")
        
        if not results:
            print("لم يتم العثور على أي نتائج.")
            return
        
        print(f"تم العثور على {len(results)} نتيجة:")
        
        for i, med in enumerate(results, 1):
            dosage_info = f" - {med.dosage}" if med.dosage else ""
            print(f"{i:3d}. {med.name}{dosage_info}")

def export_medications_to_excel():
    """تصدير الأدوية إلى ملف Excel"""
    
    with app.app_context():
        medications = Medication.query.all()
        
        if not medications:
            print("لا توجد أدوية للتصدير!")
            return
        
        # تحضير البيانات
        data = []
        for med in medications:
            data.append({
                'ID': med.id,
                'اسم الدواء': med.name,
                'الجرعة': med.dosage or ''
            })
        
        # إنشاء DataFrame
        df = pd.DataFrame(data)
        
        # تصدير إلى Excel
        filename = 'medications_export.xlsx'
        try:
            df.to_excel(filename, index=False, engine='openpyxl')
            print(f"تم تصدير {len(medications)} دواء إلى ملف '{filename}' بنجاح!")
        except Exception as e:
            print(f"خطأ في التصدير: {e}")

def delete_medication():
    """حذف دواء"""
    
    search_term = input("\nأدخل اسم الدواء المراد حذفه: ").strip()
    
    if not search_term:
        print("اسم الدواء مطلوب!")
        return
    
    with app.app_context():
        # البحث عن الدواء
        medications = Medication.query.filter(
            Medication.name.like(f'%{search_term}%')
        ).all()
        
        if not medications:
            print("لم يتم العثور على أي دواء بهذا الاسم.")
            return
        
        if len(medications) == 1:
            med = medications[0]
            dosage_info = f" - {med.dosage}" if med.dosage else ""
            
            confirm = input(f"هل أنت متأكد من حذف '{med.name}{dosage_info}'؟ (y/n): ")
            
            if confirm.lower() in ['y', 'yes', 'نعم']:
                try:
                    db.session.delete(med)
                    db.session.commit()
                    print("تم حذف الدواء بنجاح!")
                except Exception as e:
                    db.session.rollback()
                    print(f"خطأ في حذف الدواء: {e}")
            else:
                print("تم إلغاء عملية الحذف.")
        
        else:
            print(f"تم العثور على {len(medications)} دواء:")
            for i, med in enumerate(medications, 1):
                dosage_info = f" - {med.dosage}" if med.dosage else ""
                print(f"{i}. {med.name}{dosage_info}")
            
            try:
                choice = int(input("أدخل رقم الدواء المراد حذفه (0 للإلغاء): "))
                
                if choice == 0:
                    print("تم إلغاء عملية الحذف.")
                    return
                
                if 1 <= choice <= len(medications):
                    med = medications[choice - 1]
                    dosage_info = f" - {med.dosage}" if med.dosage else ""
                    
                    confirm = input(f"هل أنت متأكد من حذف '{med.name}{dosage_info}'؟ (y/n): ")
                    
                    if confirm.lower() in ['y', 'yes', 'نعم']:
                        try:
                            db.session.delete(med)
                            db.session.commit()
                            print("تم حذف الدواء بنجاح!")
                        except Exception as e:
                            db.session.rollback()
                            print(f"خطأ في حذف الدواء: {e}")
                    else:
                        print("تم إلغاء عملية الحذف.")
                else:
                    print("رقم غير صحيح!")
                    
            except ValueError:
                print("يرجى إدخال رقم صحيح!")

def show_database_info():
    """عرض معلومات قاعدة البيانات"""
    
    with app.app_context():
        total = Medication.query.count()
        
        # أدوية بدون جرعة
        no_dosage = Medication.query.filter(
            (Medication.dosage == None) | (Medication.dosage == '')
        ).count()
        
        # آخر 5 أدوية مضافة
        latest = Medication.query.order_by(Medication.id.desc()).limit(5).all()
        
        print(f"\n=== معلومات قاعدة البيانات ===")
        print(f"إجمالي الأدوية: {total}")
        print(f"أدوية بدون جرعة: {no_dosage}")
        print(f"أدوية بجرعة: {total - no_dosage}")
        
        if latest:
            print(f"\nآخر 5 أدوية مضافة:")
            for i, med in enumerate(latest, 1):
                dosage_info = f" - {med.dosage}" if med.dosage else ""
                print(f"{i}. {med.name}{dosage_info}")

def main_menu():
    """القائمة الرئيسية"""
    
    while True:
        print("\n" + "="*50)
        print("إدارة قاعدة بيانات الأدوية")
        print("="*50)
        print("1. عرض معلومات قاعدة البيانات")
        print("2. البحث في الأدوية")
        print("3. إضافة دواء جديد")
        print("4. حذف دواء")
        print("5. تصدير الأدوية إلى Excel")
        print("6. استيراد من ملف Excel")
        print("7. تنظيف قاعدة البيانات")
        print("0. خروج")
        
        choice = input("\nأدخل اختيارك (0-7): ").strip()
        
        if choice == '0':
            print("شكراً لاستخدام نظام إدارة الأدوية!")
            break
        elif choice == '1':
            show_database_info()
        elif choice == '2':
            search_medications()
        elif choice == '3':
            add_single_medication()
        elif choice == '4':
            delete_medication()
        elif choice == '5':
            export_medications_to_excel()
        elif choice == '6':
            print("لاستيراد الأدوية من Excel، استخدم:")
            print("python import_medications_from_excel.py")
        elif choice == '7':
            print("لتنظيف قاعدة البيانات، استخدم:")
            print("python clean_medications.py")
        else:
            print("اختيار غير صحيح. حاول مرة أخرى.")

if __name__ == "__main__":
    print("مرحباً بك في نظام إدارة الأدوية")
    main_menu()