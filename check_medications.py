#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
سكريپت للتحقق من الأدوية المستوردة في قاعدة البيانات
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

def check_medications():
    """التحقق من الأدوية في قاعدة البيانات"""
    
    with app.app_context():
        # إحصائيات عامة
        total_medications = Medication.query.count()
        print(f"=== إحصائيات الأدوية ===")
        print(f"إجمالي عدد الأدوية: {total_medications}")
        
        # عرض أول 20 دواء
        print(f"\n=== أول 20 دواء ===")
        medications = Medication.query.limit(20).all()
        for i, med in enumerate(medications, 1):
            dosage_info = f" - {med.dosage}" if med.dosage else ""
            print(f"{i:2d}. {med.name}{dosage_info}")
        
        # البحث عن أدوية معينة
        print(f"\n=== البحث عن أدوية شائعة ===")
        common_drugs = ['PARACETAMOL', 'IBUPROFEN', 'ASPIRIN', 'AMOXICILLIN']
        
        for drug in common_drugs:
            results = Medication.query.filter(Medication.name.like(f'%{drug}%')).all()
            print(f"{drug}: {len(results)} نتيجة")
            for result in results[:3]:  # عرض أول 3 نتائج فقط
                dosage_info = f" - {result.dosage}" if result.dosage else ""
                print(f"  • {result.name}{dosage_info}")
        
        # الأدوية بدون جرعة
        no_dosage = Medication.query.filter(
            (Medication.dosage == None) | (Medication.dosage == '')
        ).count()
        print(f"\n=== إحصائيات الجرعات ===")
        print(f"أدوية بدون جرعة محددة: {no_dosage}")
        print(f"أدوية بجرعة محددة: {total_medications - no_dosage}")

def search_medication(search_term):
    """البحث عن دواء معين"""
    
    with app.app_context():
        results = Medication.query.filter(
            Medication.name.like(f'%{search_term}%')
        ).all()
        
        print(f"\n=== نتائج البحث عن '{search_term}' ===")
        print(f"تم العثور على {len(results)} نتيجة:")
        
        for i, med in enumerate(results, 1):
            dosage_info = f" - {med.dosage}" if med.dosage else ""
            print(f"{i:2d}. {med.name}{dosage_info}")

if __name__ == "__main__":
    print("=== فحص قاعدة بيانات الأدوية ===")
    
    # فحص عام
    check_medications()
    
    # إمكانية البحث
    print("\n" + "="*50)
    search_term = input("أدخل اسم الدواء للبحث عنه (أو اضغط Enter للتخطي): ").strip()
    
    if search_term:
        search_medication(search_term)
    
    print("\nتم الانتهاء من الفحص.")