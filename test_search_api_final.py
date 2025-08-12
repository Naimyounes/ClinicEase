#!/usr/bin/env python3
"""
اختبار نهائي لـ API البحث
"""
import requests
import json

def test_api():
    """اختبار API البحث الجديد"""
    base_url = "http://localhost:5000"
    
    print("🧪 اختبار API البحث...")
    
    try:
        # تسجيل دخول
        session = requests.Session()
        login_data = {
            'username': 'secretary',
            'password': 'secretary123'
        }
        
        login_response = session.post(f"{base_url}/login", data=login_data)
        
        if login_response.status_code == 200:
            print("✅ تم تسجيل الدخول بنجاح")
            
            # اختبار API البحث
            search_response = session.get(
                f"{base_url}/secretary/api/search-patients",
                params={'term': 'hola'}
            )
            
            print(f"📊 استجابة API: {search_response.status_code}")
            
            if search_response.status_code == 200:
                try:
                    data = search_response.json()
                    print(f"🎯 عدد النتائج: {len(data)}")
                    
                    if data:
                        print("📋 أول نتيجة:")
                        result = data[0]
                        print(f"   الاسم: {result['full_name']}")
                        print(f"   الهاتف: {result['phone']}")
                        print(f"   الجنس: {result['gender']}")
                        print(f"   العمر: {result['age']}")
                        print("✅ API البحث يعمل بشكل مثالي!")
                    else:
                        print("⚠️ لا توجد نتائج للبحث 'hola'")
                        
                except json.JSONDecodeError as e:
                    print(f"❌ خطأ في JSON: {e}")
                    print(f"Response: {search_response.text[:200]}")
            else:
                print(f"❌ خطأ في API: {search_response.status_code}")
                print(f"Response: {search_response.text[:300]}")
        else:
            print("❌ فشل تسجيل الدخول")
            
    except requests.exceptions.ConnectionError:
        print("❌ الخادم لا يعمل - شغل: python run.py")
    except Exception as e:
        print(f"❌ خطأ: {e}")

if __name__ == "__main__":
    test_api()