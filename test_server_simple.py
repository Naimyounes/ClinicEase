#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
اختبار بسيط للخادم
"""

import requests

def test_server():
    """اختبار الخادم"""
    base_url = "http://127.0.0.1:5000"
    
    print("🔍 اختبار الخادم...")
    print("=" * 50)
    
    try:
        # اختبار الصفحة الرئيسية
        response = requests.get(base_url, timeout=10)
        print(f"📊 حالة الصفحة الرئيسية: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ الخادم يعمل بشكل صحيح")
        else:
            print(f"❌ خطأ في الخادم: {response.status_code}")
            
    except requests.exceptions.ConnectionError:
        print("❌ خطأ في الاتصال - تأكد من تشغيل الخادم على المنفذ 5000")
    except Exception as e:
        print(f"❌ خطأ غير متوقع: {e}")
    
    print("=" * 50)

if __name__ == "__main__":
    test_server()