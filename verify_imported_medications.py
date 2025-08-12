#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
سكريپت للتحقق من الأدوية المستوردة
"""

import sys
import os

# إضافة مسار المشروع
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# استيراد التطبيق والنماذج
from clinic_app import create_app, db
from clinic_app.models import Medication

# إنشاء التطبيق
app = create_app()

def show_medication_statistics():
    """عرض إحصائيات مفصلة عن الأدوية"""
    
    with app.app_context():
        total = Medication.query.count()
        
        print(f"=== إحصائيات الأدوية ===")
        print(f"إجمالي الأدوية: {total}")
        
        # أدوية بدون جرعة
        no_dosage = Medication.query.filter(
            (Medication.dosage == None) | (Medication.dosage == '')
        ).count()
        print(f"أدوية بدون جرعة: {no_dosage}")
        print(f"أدوية بجرعة: {total - no_dosage}")

def search_specific_medications():
    """البحث عن أدوية معينة"""
    
    with app.app_context():
        print(f"\n=== البحث عن أدوية شائعة ===")
        
        # قائمة الأدوية الشائعة للبحث عنها
        common_drugs = [
            'PARACETAMOL',
            'IBUPROFEN', 
            'AMOXICILLIN',
            'CETIRIZINE',
            'OMEPRAZOLE',
            'METFORMIN'
        ]
        
        for drug in common_drugs:
            results = Medication.query.filter(
                Medication.name.like(f'%{drug}%')
            ).all()
            
            print(f"\n{drug}: {len(results)} نتيجة")
            
            # عرض أول 5 نتائج
            for i, med in enumerate(results[:5], 1):
                dosage_info = f" - {med.dosage}" if med.dosage else " - بدون جرعة"
                print(f"  {i}. {med.name}{dosage_info}")
            
            if len(results) > 5:
                print(f"  ... و {len(results) - 5} نتيجة أخرى")

def show_random_sample():
    """عرض عينة عشوائية من الأدوية"""
    
    with app.app_context():
        print(f"\n=== عينة عشوائية من الأدوية ===")
        
        # الحصول على عينة عشوائية
        import random
        total_count = Medication.query.count()
        
        # اختيار 20 رقم عشوائي
        random_ids = random.sample(range(1, total_count + 1), min(20, total_count))
        
        for i, med_id in enumerate(random_ids, 1):
            med = Medication.query.get(med_id)
            if med:
                dosage_info = f" - {med.dosage}" if med.dosage else " - بدون جرعة"
                print(f"{i:2d}. ID:{med.id} | {med.name}{dosage_info}")

def interactive_search():
    """بحث تفاعلي"""
    
    with app.app_context():
        while True:
            print(f"\n=== البحث التفاعلي ===")
            search_term = input("أدخل اسم الدواء للبحث عنه (أو 'خروج' للإنهاء): ").strip()
            
            if search_term.lower() in ['خروج', 'exit', 'quit', '']:
                break
            
            results = Medication.query.filter(
                Medication.name.like(f'%{search_term}%')
            ).all()
            
            print(f"\nتم العثور على {len(results)} نتيجة:")
            
            if not results:
                print("لا توجد نتائج.")
                continue
            
            # عرض النتائج مع ترقيم
            for i, med in enumerate(results, 1):
                dosage_info = f" - {med.dosage}" if med.dosage else " - بدون جرعة"
                print(f"{i:3d}. ID:{med.id} | {med.name}{dosage_info}")
            
            if len(results) > 50:
                print(f"\n(عرض أول 50 نتيجة من أصل {len(results)})")

def check_duplicates():
    """فحص الأدوية المكررة"""
    
    with app.app_context():
        print(f"\n=== فحص الأدوية المكررة ===")
        
        # البحث عن الأدوية المكررة (نفس الاسم والجرعة)
        duplicates = db.session.query(
            Medication.name,
            Medication.dosage,
            db.func.count(Medication.id).label('count')
        ).group_by(
            Medication.name,
            Medication.dosage
        ).having(
            db.func.count(Medication.id) > 1
        ).order_by(
            db.func.count(Medication.id).desc()
        ).limit(10).all()
        
        if duplicates:
            print(f"أكثر 10 أدوية تكراراً:")
            for name, dosage, count in duplicates:
                dosage_info = f" - {dosage}" if dosage else " - بدون جرعة"
                print(f"  '{name}{dosage_info}' ({count} مرة)")
        else:
            print("لا توجد أدوية مكررة.")

def main_menu():
    """القائمة الرئيسية"""
    
    while True:
        print("\n" + "="*50)
        print("فحص الأدوية المستوردة")
        print("="*50)
        print("1. عرض الإحصائيات")
        print("2. البحث عن أدوية شائعة")
        print("3. عرض عينة عشوائية")
        print("4. البحث التفاعلي")
        print("5. فحص الأدوية المكررة")
        print("0. خروج")
        
        choice = input("\nأدخل اختيارك (0-5): ").strip()
        
        if choice == '0':
            print("شكراً لاستخدام نظام فحص الأدوية!")
            break
        elif choice == '1':
            show_medication_statistics()
        elif choice == '2':
            search_specific_medications()
        elif choice == '3':
            show_random_sample()
        elif choice == '4':
            interactive_search()
        elif choice == '5':
            check_duplicates()
        else:
            print("اختيار غير صحيح. حاول مرة أخرى.")

if __name__ == "__main__":
    print("=== فحص الأدوية المستوردة ===")
    main_menu()