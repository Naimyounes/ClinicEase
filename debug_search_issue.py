#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
ملف تشخيص مشكلة البحث في قائمة المرضى
"""
import sys
import codecs
import os

# Set UTF-8 encoding for console output
sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer)

# إضافة المسار الجذر للمشروع
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from clinic_app import create_app, db
from clinic_app.models import Patient
from flask import Flask
import traceback

def diagnose_search_issue():
    """تشخيص مشكلة البحث"""
    app = create_app()
    
    with app.app_context():
        print("🔍 تشخيص مشكلة البحث في قائمة المرضى")
        print("=" * 50)
        
        try:
            # 1. التحقق من وجود جدول المرضى
            print("1. التحقق من وجود جدول المرضى...")
            patient_count = Patient.query.count()
            print(f"   ✅ عدد المرضى في قاعدة البيانات: {patient_count}")
            
            # 2. عرض عينة من المرضى
            if patient_count > 0:
                print("\n2. عرض أول 5 مرضى:")
                sample_patients = Patient.query.limit(5).all()
                for i, patient in enumerate(sample_patients, 1):
                    print(f"   {i}. الاسم: {patient.full_name} | الهاتف: {patient.phone}")
            
            # 3. اختبار استعلام البحث
            print("\n3. اختبار استعلام البحث...")
            
            # اختبار بحث فارغ
            term = ""
            empty_results = Patient.query.filter(
                Patient.full_name.ilike(f"%{term}%") | 
                Patient.phone.ilike(f"%{term}%")
            ).limit(10).all()
            print(f"   البحث الفارغ: {len(empty_results)} نتيجة")
            
            # اختبار بحث بحرف واحد
            if patient_count > 0:
                # الحصول على أول حرف من أول مريض للاختبار
                first_patient = Patient.query.first()
                test_char = first_patient.full_name[0] if first_patient and len(first_patient.full_name) > 0 else "ا"
                print(f"   اختبار البحث بالحرف: '{test_char}'")
                
                char_results = Patient.query.filter(
                    Patient.full_name.ilike(f"%{test_char}%") | 
                    Patient.phone.ilike(f"%{test_char}%")
                ).limit(10).all()
                print(f"   نتائج البحث بحرف '{test_char}': {len(char_results)} مريض")
                
                for patient in char_results[:3]:  # عرض أول 3 نتائج
                    print(f"     - {patient.full_name} ({patient.phone})")
            
            # 4. اختبار تحويل النتائج إلى JSON
            print("\n4. اختبار تحويل النتائج إلى JSON...")
            if patient_count > 0:
                sample_patient = Patient.query.first()
                try:
                    from flask import url_for
                    result_dict = {
                        'id': sample_patient.id,
                        'full_name': sample_patient.full_name,
                        'phone': sample_patient.phone or 'غير محدد',
                        'view_url': url_for('secretary.patient_details', patient_id=sample_patient.id)
                    }
                    print(f"   ✅ تم تحويل المريض إلى JSON: {result_dict}")
                except Exception as e:
                    print(f"   ❌ خطأ في تحويل المريض إلى JSON: {str(e)}")
                    print(f"   التفاصيل: {traceback.format_exc()}")
            
            # 5. اختبار دالة البحث نفسها
            print("\n5. اختبار دالة البحث...")
            def simulate_search_api(term):
                """محاكاة دالة البحث API"""
                try:
                    if not term or len(term) < 2:
                        return []
                    
                    patients = Patient.query.filter(
                        Patient.full_name.ilike(f"%{term}%") | 
                        Patient.phone.ilike(f"%{term}%")
                    ).limit(10).all()
                    
                    results = []
                    for patient in patients:
                        results.append({
                            'id': patient.id,
                            'full_name': patient.full_name,
                            'phone': patient.phone or 'غير محدد',
                            'view_url': f'/secretary/patient/{patient.id}'  # رابط مبسط للاختبار
                        })
                    
                    return results
                except Exception as e:
                    print(f"     ❌ خطأ في محاكاة البحث: {str(e)}")
                    return []
            
            # اختبار البحث مع مصطلحات مختلفة
            test_terms = ["ا", "أ", "م", "01"]
            for term in test_terms:
                results = simulate_search_api(term)
                print(f"   البحث عن '{term}': {len(results)} نتيجة")
                
        except Exception as e:
            print(f"❌ حدث خطأ عام في التشخيص: {str(e)}")
            print(f"التفاصيل الكاملة: {traceback.format_exc()}")

if __name__ == "__main__":
    diagnose_search_issue()