#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
اختبار سريع لصفحة الأدوية بعد إصلاح خطأ Jinja2
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

def test_template_rendering():
    """اختبار عرض القالب"""
    
    with app.app_context():
        from flask import render_template
        from clinic_app.doctor.forms import MedicationForm
        
        try:
            # محاولة عرض القالب
            form = MedicationForm()
            medications = Medication.query.limit(5).all()  # أول 5 أدوية للاختبار
            
            # محاولة عرض القالب
            rendered = render_template(
                'doctor/medications.html', 
                title='Gestion des médicaments', 
                form=form, 
                medications=medications
            )
            
            print("✅ تم عرض القالب بنجاح!")
            print(f"✅ تم عرض {len(medications)} دواء في القالب")
            
            # التحقق من وجود العناصر المهمة
            if 'delete-form' in rendered:
                print("✅ نماذج الحذف موجودة")
            
            if 'csrf_token' in rendered:
                print("✅ CSRF tokens موجودة")
                
            if 'searchMedication' in rendered:
                print("✅ بار البحث موجود")
                
            return True
            
        except Exception as e:
            print(f"❌ خطأ في عرض القالب: {e}")
            return False

def show_medications_sample():
    """عرض عينة من الأدوية"""
    
    with app.app_context():
        print(f"\n=== عينة من الأدوية ===")
        medications = Medication.query.limit(10).all()
        
        for i, med in enumerate(medications, 1):
            dosage_info = f" - {med.dosage}" if med.dosage else " - بدون جرعة"
            print(f"{i:2d}. {med.name}{dosage_info}")
        
        total = Medication.query.count()
        print(f"\nإجمالي الأدوية: {total}")

if __name__ == "__main__":
    print("=== اختبار إصلاح قالب الأدوية ===")
    
    if test_template_rendering():
        show_medications_sample()
        
        print(f"\n=== النتيجة ===")
        print("✅ تم إصلاح خطأ Jinja2 بنجاح!")
        print("✅ القالب يعمل بشكل صحيح")
        print("✅ زر الحذف يجب أن يعمل الآن")
        
        print(f"\n=== للاختبار ===")
        print("1. شغل التطبيق: python run.py")
        print("2. اذهب إلى: http://localhost:5000/doctor/medications")
        print("3. سجل دخول كطبيب: doctor / doctor123")
        print("4. اختبر إضافة وحذف الأدوية")
    else:
        print("❌ لا يزال هناك خطأ في القالب")