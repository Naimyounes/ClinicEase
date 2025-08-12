#!/usr/bin/env python3
"""
اختبار API البحث في صفحة المرضى
"""
import requests
import json

def test_search_api():
    """اختبار API البحث"""
    base_url = "http://localhost:5000"
    
    # إنشاء جلسة
    session = requests.Session()
    
    try:
        print("=== اختبار حالة الخادم ===")
        response = session.get(base_url)
        print(f"الخادم: {response.status_code} {'✅' if response.status_code == 200 else '❌'}")
        
        print("\n=== اختبار تسجيل الدخول ===")
        # الحصول على صفحة تسجيل الدخول
        login_page = session.get(f"{base_url}/login")
        print(f"صفحة تسجيل الدخول: {login_page.status_code}")
        
        # تسجيل الدخول كسكرتيرة
        login_data = {
            'username': 'secretary',
            'password': 'secretary123'
        }
        
        login_response = session.post(f"{base_url}/login", data=login_data)
        print(f"تسجيل الدخول: {login_response.status_code}")
        
        if 'logout' in login_response.text or 'secretary' in login_response.url:
            print("✅ نجح تسجيل الدخول")
            
            print("\n=== اختبار API البحث ===")
            # اختبار البحث
            search_url = f"{base_url}/secretary/api/search-patients"
            search_params = {'term': 'test'}
            
            search_response = session.get(search_url, params=search_params)
            print(f"API البحث: {search_response.status_code}")
            
            if search_response.status_code == 200:
                try:
                    data = search_response.json()
                    print(f"✅ البحث نجح، عدد النتائج: {len(data)}")
                    if data:
                        print("نتيجة عينة:")
                        print(json.dumps(data[0], indent=2, ensure_ascii=False))
                    else:
                        print("لا توجد نتائج للبحث")
                except json.JSONDecodeError:
                    print("❌ خطأ في تحليل JSON")
                    print(f"Response: {search_response.text[:500]}")
            else:
                print(f"❌ فشل API البحث")
                print(f"Response: {search_response.text[:500]}")
                
        else:
            print("❌ فشل في تسجيل الدخول")
            print(f"Redirected to: {login_response.url}")
            
    except requests.exceptions.ConnectionError:
        print("❌ لا يمكن الاتصال بالخادم")
        print("تأكد من تشغيل الخادم: python run.py")
    except Exception as e:
        print(f"❌ خطأ غير متوقع: {e}")

if __name__ == "__main__":
    test_search_api()