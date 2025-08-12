#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
اختبار وظائف البحث مع تسجيل الدخول
"""

import requests
import json

def test_search_with_login():
    """اختبار وظائف البحث مع تسجيل الدخول"""
    base_url = "http://127.0.0.1:5000"
    
    print("🔍 اختبار وظائف البحث مع تسجيل الدخول...")
    print("=" * 60)
    
    # إنشاء جلسة للحفاظ على الكوكيز
    session = requests.Session()
    
    try:
        # الحصول على صفحة تسجيل الدخول أولاً للحصول على CSRF token
        login_page = session.get(f"{base_url}/login")
        print(f"📊 حالة صفحة تسجيل الدخول: {login_page.status_code}")
        
        if login_page.status_code != 200:
            print("❌ لا يمكن الوصول إلى صفحة تسجيل الدخول")
            return
        
        # محاولة تسجيل الدخول كسكرتير
        login_data = {
            'username': 'secretary',
            'password': 'secretary123'
        }
        
        login_response = session.post(f"{base_url}/login", data=login_data)
        print(f"📊 حالة تسجيل الدخول: {login_response.status_code}")
        
        # التحقق من نجاح تسجيل الدخول
        if login_response.status_code == 200 and 'dashboard' in login_response.url:
            print("✅ تم تسجيل الدخول بنجاح")
        else:
            print("❌ فشل في تسجيل الدخول")
            print(f"📄 الرابط النهائي: {login_response.url}")
            return
        
        # الآن اختبار وظائف البحث
        search_endpoints = [
            "/secretary/api/search-patients",
            "/secretary/api/search-patients-for-ticket"
        ]
        
        test_terms = ["أحمد", "محمد", "test"]
        
        for endpoint in search_endpoints:
            print(f"\n📍 اختبار: {endpoint}")
            print("-" * 40)
            
            for term in test_terms:
                try:
                    url = f"{base_url}{endpoint}?term={term}"
                    response = session.get(url, timeout=10)
                    
                    print(f"🔗 المصطلح: '{term}' - الحالة: {response.status_code}")
                    
                    if response.status_code == 200:
                        try:
                            data = response.json()
                            print(f"✅ النتائج: {len(data)} مريض")
                            if data and len(data) > 0:
                                print(f"📝 أول نتيجة: {data[0].get('full_name', 'غير محدد')}")
                        except json.JSONDecodeError:
                            print("❌ خطأ في تحليل JSON")
                    else:
                        print(f"❌ خطأ HTTP: {response.status_code}")
                        
                except Exception as e:
                    print(f"❌ خطأ: {e}")
                
                print()
        
    except requests.exceptions.ConnectionError:
        print("❌ خطأ في الاتصال - تأكد من تشغيل الخادم")
    except Exception as e:
        print(f"❌ خطأ غير متوقع: {e}")
    
    print("=" * 60)
    print("✅ انتهى الاختبار")

if __name__ == "__main__":
    test_search_with_login()