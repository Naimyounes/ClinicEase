#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
اختبار وظائف البحث في التطبيق
"""

import requests
import json

def test_search_functions():
    """اختبار جميع وظائف البحث"""
    base_url = "http://127.0.0.1:5000"
    
    # قائمة وظائف البحث للاختبار
    search_endpoints = [
        "/secretary/api/search-patients",
        "/secretary/api/search-patients-for-ticket"
    ]
    
    # مصطلحات البحث للاختبار
    test_terms = ["أحمد", "محمد", "123", ""]
    
    print("🔍 اختبار وظائف البحث...")
    print("=" * 50)
    
    for endpoint in search_endpoints:
        print(f"\n📍 اختبار: {endpoint}")
        print("-" * 30)
        
        for term in test_terms:
            try:
                url = f"{base_url}{endpoint}?term={term}"
                print(f"🔗 الرابط: {url}")
                
                response = requests.get(url, timeout=10)
                
                print(f"📊 الحالة: {response.status_code}")
                
                if response.status_code == 200:
                    try:
                        data = response.json()
                        print(f"✅ النتائج: {len(data)} مريض")
                        if data and len(data) > 0:
                            print(f"📝 أول نتيجة: {data[0].get('full_name', 'غير محدد')}")
                    except json.JSONDecodeError:
                        print("❌ خطأ في تحليل JSON")
                        print(f"📄 المحتوى: {response.text[:100]}...")
                else:
                    print(f"❌ خطأ HTTP: {response.status_code}")
                    print(f"📄 المحتوى: {response.text[:100]}...")
                    
            except requests.exceptions.ConnectionError:
                print("❌ خطأ في الاتصال - تأكد من تشغيل الخادم")
            except requests.exceptions.Timeout:
                print("❌ انتهت مهلة الاتصال")
            except Exception as e:
                print(f"❌ خطأ غير متوقع: {e}")
            
            print()
    
    print("=" * 50)
    print("✅ انتهى الاختبار")

if __name__ == "__main__":
    test_search_functions()