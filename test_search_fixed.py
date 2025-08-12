#!/usr/bin/env python3
"""
اختبار البحث بعد الإصلاح
"""
import requests
import json

def test_search_fixed():
    """اختبار سريع للبحث"""
    
    try:
        # اختبار الاتصال بالخادم
        response = requests.get("http://localhost:5000")
        if response.status_code != 200:
            print("❌ الخادم لا يعمل")
            return
            
        print("✅ الخادم يعمل")
        
        # اختبار API البحث مباشرة (بدون تسجيل دخول للاختبار السريع)
        session = requests.Session()
        
        # محاولة تسجيل دخول سريع
        login_data = {
            'username': 'secretary',
            'password': 'secretary123'
        }
        login_response = session.post("http://localhost:5000/login", data=login_data)
        
        if login_response.status_code == 200:
            # اختبار API البحث
            search_response = session.get(
                "http://localhost:5000/secretary/api/search-patients",
                params={'term': 'hola'}
            )
            
            print(f"🔍 استجابة البحث: {search_response.status_code}")
            
            if search_response.status_code == 200:
                try:
                    data = search_response.json()
                    print(f"📊 عدد النتائج: {len(data)}")
                    
                    if data:
                        print("✅ البحث يعمل! عينة من النتائج:")
                        for result in data[:2]:
                            print(f"  - {result['full_name']} ({result['gender']}, {result['age']})")
                    else:
                        print("⚠️ لا توجد نتائج للبحث")
                        
                except json.JSONDecodeError:
                    print("❌ خطأ في تحليل JSON")
                    print(search_response.text[:200])
            else:
                print(f"❌ خطأ في API البحث: {search_response.status_code}")
                print(search_response.text[:200])
        else:
            print("❌ فشل تسجيل الدخول")
            
    except requests.exceptions.ConnectionError:
        print("❌ لا يمكن الاتصال بالخادم - تأكد من تشغيل: python run.py")
    except Exception as e:
        print(f"❌ خطأ: {e}")

if __name__ == "__main__":
    test_search_fixed()