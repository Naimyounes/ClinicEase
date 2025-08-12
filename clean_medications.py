#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
سكريپت لتنظيف وتحسين بيانات الأدوية
"""

import sys
import os
import re

# إضافة مسار المشروع
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# استيراد التطبيق والنماذج
from clinic_app import create_app, db
from clinic_app.models import Medication

# إنشاء التطبيق
app = create_app()

def clean_medication_name(name):
    """تنظيف اسم الدواء"""
    if not name:
        return name
    
    # إزالة المسافات الزائدة
    name = name.strip()
    
    # إزالة المسافات المتعددة
    name = re.sub(r'\s+', ' ', name)
    
    return name

def clean_dosage(dosage):
    """تنظيف الجرعة"""
    if not dosage:
        return dosage
    
    # إزالة المسافات الزائدة
    dosage = dosage.strip()
    
    # إزالة المسافات المتعددة
    dosage = re.sub(r'\s+', ' ', dosage)
    
    return dosage

def find_duplicates():
    """البحث عن الأدوية المكررة"""
    
    with app.app_context():
        print("=== البحث عن الأدوية المكررة ===")
        
        # الحصول على جميع الأدوية
        medications = Medication.query.all()
        
        # تجميع الأدوية حسب الاسم (بعد التنظيف)
        name_groups = {}
        
        for med in medications:
            clean_name = clean_medication_name(med.name).upper()
            
            if clean_name not in name_groups:
                name_groups[clean_name] = []
            
            name_groups[clean_name].append(med)
        
        # العثور على المجموعات التي تحتوي على أكثر من دواء واحد
        duplicates = {name: meds for name, meds in name_groups.items() if len(meds) > 1}
        
        print(f"تم العثور على {len(duplicates)} مجموعة من الأدوية المكررة:")
        
        for name, meds in list(duplicates.items())[:10]:  # عرض أول 10 مجموعات
            print(f"\n'{name}' ({len(meds)} نسخة):")
            for med in meds:
                dosage_info = f" - {med.dosage}" if med.dosage else ""
                print(f"  • ID: {med.id} | {med.name}{dosage_info}")
        
        return duplicates

def clean_all_medications():
    """تنظيف جميع أسماء الأدوية والجرعات"""
    
    with app.app_context():
        print("=== تنظيف أسماء الأدوية والجرعات ===")
        
        medications = Medication.query.all()
        updated_count = 0
        
        for med in medications:
            original_name = med.name
            original_dosage = med.dosage
            
            # تنظيف الاسم
            clean_name = clean_medication_name(med.name)
            clean_dos = clean_dosage(med.dosage)
            
            # التحقق من وجود تغييرات
            if clean_name != original_name or clean_dos != original_dosage:
                med.name = clean_name
                med.dosage = clean_dos
                updated_count += 1
                
                print(f"تم تحديث: '{original_name}' -> '{clean_name}'")
                if original_dosage != clean_dos:
                    print(f"  الجرعة: '{original_dosage}' -> '{clean_dos}'")
        
        if updated_count > 0:
            try:
                db.session.commit()
                print(f"\nتم تحديث {updated_count} دواء بنجاح.")
            except Exception as e:
                db.session.rollback()
                print(f"خطأ في حفظ التحديثات: {e}")
        else:
            print("لا توجد تحديثات مطلوبة.")

def remove_exact_duplicates():
    """إزالة الأدوية المكررة تماماً (نفس الاسم والجرعة)"""
    
    with app.app_context():
        print("=== إزالة الأدوية المكررة تماماً ===")
        
        # البحث عن الأدوية المكررة
        duplicates_query = db.session.query(
            Medication.name, 
            Medication.dosage, 
            db.func.count(Medication.id).label('count'),
            db.func.min(Medication.id).label('keep_id')
        ).group_by(
            Medication.name, 
            Medication.dosage
        ).having(
            db.func.count(Medication.id) > 1
        )
        
        duplicates = duplicates_query.all()
        
        if not duplicates:
            print("لا توجد أدوية مكررة تماماً.")
            return
        
        print(f"تم العثور على {len(duplicates)} مجموعة من الأدوية المكررة تماماً:")
        
        total_removed = 0
        
        for dup in duplicates:
            name, dosage, count, keep_id = dup
            dosage_info = f" - {dosage}" if dosage else ""
            print(f"'{name}{dosage_info}' ({count} نسخة)")
            
            # حذف جميع النسخ عدا الأولى
            deleted = Medication.query.filter(
                Medication.name == name,
                Medication.dosage == dosage,
                Medication.id != keep_id
            ).delete()
            
            total_removed += deleted
            print(f"  تم حذف {deleted} نسخة مكررة")
        
        try:
            db.session.commit()
            print(f"\nتم حذف {total_removed} دواء مكرر بنجاح.")
            print(f"العدد الحالي للأدوية: {Medication.query.count()}")
        except Exception as e:
            db.session.rollback()
            print(f"خطأ في حذف الأدوية المكررة: {e}")

def show_statistics():
    """عرض إحصائيات مفصلة"""
    
    with app.app_context():
        total = Medication.query.count()
        
        # أدوية بدون جرعة
        no_dosage = Medication.query.filter(
            (Medication.dosage == None) | (Medication.dosage == '')
        ).count()
        
        # أطول أسماء الأدوية
        longest_names = Medication.query.order_by(
            db.func.length(Medication.name).desc()
        ).limit(5).all()
        
        print(f"\n=== إحصائيات مفصلة ===")
        print(f"إجمالي الأدوية: {total}")
        print(f"أدوية بدون جرعة: {no_dosage}")
        print(f"أدوية بجرعة: {total - no_dosage}")
        
        print(f"\nأطول أسماء الأدوية:")
        for i, med in enumerate(longest_names, 1):
            dosage_info = f" - {med.dosage}" if med.dosage else ""
            print(f"{i}. {med.name}{dosage_info} ({len(med.name)} حرف)")

if __name__ == "__main__":
    print("=== تنظيف قاعدة بيانات الأدوية ===")
    
    while True:
        print("\nاختر العملية:")
        print("1. عرض الإحصائيات")
        print("2. البحث عن الأدوية المكررة")
        print("3. تنظيف أسماء الأدوية والجرعات")
        print("4. إزالة الأدوية المكررة تماماً")
        print("5. تنفيذ جميع عمليات التنظيف")
        print("0. خروج")
        
        choice = input("\nأدخل اختيارك (0-5): ").strip()
        
        if choice == '0':
            break
        elif choice == '1':
            show_statistics()
        elif choice == '2':
            find_duplicates()
        elif choice == '3':
            clean_all_medications()
        elif choice == '4':
            remove_exact_duplicates()
        elif choice == '5':
            print("تنفيذ جميع عمليات التنظيف...")
            clean_all_medications()
            remove_exact_duplicates()
            show_statistics()
        else:
            print("اختيار غير صحيح. حاول مرة أخرى.")
    
    print("تم الانتهاء من تنظيف قاعدة البيانات.")