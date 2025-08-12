#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
اختبار خاصية البحث التلقائي للمرضى
"""

import requests
import json

# إعدادات الاختبار
BASE_URL = "http://127.0.0.1:5000"
LOGIN_URL = f"{BASE_URL}/auth/login"
SEARCH_API_URL = f"{BASE_URL}/secretary/api/search-patients"
PATIENTS_PAGE_URL = f"{BASE_URL}/secretary/patients"

def login_as_secretary():
    """تسجيل دخول كسكرتير"""
    session = requests.Session()
    
    # الحصول على صفحة تسجيل الدخول للحصول على CSRF token
    login_page = session.get(LOGIN_URL)
    
    # استخراج CSRF token (بسيط)
    csrf_token = None
    if 'csrf_token' in login_page.text:
        import re
        match = re.search(r'name="csrf_token" type="hidden" value="([^"]+)"', login_page.text)
        if match:
            csrf_token = match.group(1)
    
    # تسجيل الدخول
    login_data = {
        'username': 'secretary',
        'password': 'secretary123',
    }
    
    if csrf_token:
        login_data['csrf_token'] = csrf_token
    
    response = session.post(LOGIN_URL, data=login_data)
    
    if response.status_code == 200 and 'dashboard' in response.url:
        print("✅ تم تسجيل الدخول بنجاح كسكرتير")
        return session
    else:
        print(f"❌ فشل في تسجيل الدخول: {response.status_code}")
        return None

def test_search_api(session, search_term):
    """اختبار API البحث"""
    print(f"\n🔍 اختبار البحث عن: '{search_term}'")
    
    try:
        response = session.get(f"{SEARCH_API_URL}?term={search_term}")
        
        if response.status_code == 200:
            results = response.json()
            print(f"✅ البحث نجح، عدد النتائج: {len(results)}")
            
            for i, patient in enumerate(results, 1):
                print(f"  {i}. {patient['full_name']} - {patient['phone']}")
                if patient.get('age'):
                    print(f"     العمر: {patient['age']}, الجنس: {patient['gender']}")
                if patient.get('address') and patient['address'] != 'غير محدد':
                    print(f"     العنوان: {patient['address']}")
            
            return True
        else:
            print(f"❌ فشل البحث: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ خطأ في البحث: {e}")
        return False

def test_patients_page(session):
    """اختبار صفحة المرضى"""
    print(f"\n📄 اختبار صفحة المرضى")
    
    try:
        response = session.get(PATIENTS_PAGE_URL)
        
        if response.status_code == 200:
            print("✅ تم تحميل صفحة المرضى بنجاح")
            
            # فحص وجود عناصر مهمة في الصفحة
            page_content = response.text
            
            if 'patient-search' in page_content:
                print("✅ حقل البحث موجود")
            else:
                print("❌ حقل البحث غير موجود")
                
            if 'search-dropdown' in page_content:
                print("✅ قائمة البحث المنسدلة موجودة")
            else:
                print("❌ قائمة البحث المنسدلة غير موجودة")
                
            if '/secretary/api/search-patients' in page_content:
                print("✅ JavaScript للبحث التلقائي موجود")
            else:
                print("❌ JavaScript للبحث التلقائي غير موجود")
            
            return True
        else:
            print(f"❌ فشل في تحميل صفحة المرضى: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ خطأ في تحميل صفحة المرضى: {e}")
        return False

def main():
    """الاختبار الرئيسي"""
    print("🚀 بدء اختبار خاصية البحث التلقائي للمرضى")
    print("=" * 50)
    
    # تسجيل الدخول
    session = login_as_secretary()
    if not session:
        print("❌ لا يمكن المتابعة بدون تسجيل دخول")
        return
    
    # اختبار صفحة المرضى
    if not test_patients_page(session):
        print("❌ مشكلة في صفحة المرضى")
        return
    
    # اختبار البحث بمصطلحات مختلفة
    search_terms = [
        "Naim",           # بحث بالاسم الأول
        "Younes",         # بحث بالاسم الأخير
        "0778",           # بحث برقم الهاتف
        "أحمد",           # بحث بالعربية
        "xyz123",         # بحث بمصطلح غير موجود
        ""                # بحث فارغ
    ]
    
    success_count = 0
    total_tests = len(search_terms)
    
    for term in search_terms:
        if test_search_api(session, term):
            success_count += 1
    
    print("\n" + "=" * 50)
    print(f"📊 نتائج الاختبار: {success_count}/{total_tests} اختبارات نجحت")
    
    if success_count == total_tests:
        print("🎉 جميع الاختبارات نجحت! خاصية البحث التلقائي تعمل بشكل ممتاز")
    else:
        print("⚠️  بعض الاختبارات فشلت، يرجى مراجعة الأخطاء أعلاه")

if __name__ == "__main__":
    main()