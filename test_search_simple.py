#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import re

def test_search():
    session = requests.Session()
    
    # تسجيل الدخول
    login_response = session.post('http://127.0.0.1:5000/login', data={
        'username': 'secretary', 
        'password': 'secretary123'
    })
    print('تسجيل الدخول:', login_response.status_code)
    
    # الحصول على الصفحة
    get_response = session.get('http://127.0.0.1:5000/secretary/emergency-ticket')
    print('GET:', get_response.status_code)
    
    # استخراج CSRF token
    csrf_match = re.search(r'name="csrf_token".*?value="([^"]+)"', get_response.text)
    csrf_token = csrf_match.group(1) if csrf_match else None
    print('CSRF token:', csrf_token[:20] if csrf_token else 'لم يتم العثور عليه')
    
    # إرسال البحث
    search_data = {'patient_search': 'Naim', 'csrf_token': csrf_token}
    post_response = session.post('http://127.0.0.1:5000/secretary/emergency-ticket', data=search_data)
    print('POST:', post_response.status_code)
    
    # فحص المحتوى
    if 'Sélectionner le patient' in post_response.text:
        print('✅ تم العثور على صفحة اختيار المرضى')
    elif 'لم يتم العثور' in post_response.text:
        print('❌ لم يتم العثور على مرضى')
    else:
        print('❓ استجابة أخرى')
        # البحث عن أسماء المرضى
        if 'Naim' in post_response.text:
            print('✅ تم العثور على اسم Naim في الاستجابة')
        else:
            print('❌ لم يتم العثور على اسم Naim في الاستجابة')

if __name__ == "__main__":
    test_search()