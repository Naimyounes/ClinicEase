#!/usr/bin/env python3
"""
اختبار حالة الخادم ومعلومات routes
"""
import requests

def test_server():
    """اختبار الخادم"""
    base_url = "http://localhost:5000"
    
    try:
        # 1. اختبار الصفحة الرئيسية
        print("🏠 اختبار الصفحة الرئيسية...")
        home_response = requests.get(base_url)
        print(f"   النتيجة: {home_response.status_code}")
        
        # 2. اختبار صفحة تسجيل الدخول
        print("\n🔐 اختبار صفحة تسجيل الدخول...")
        login_response = requests.get(f"{base_url}/login")
        print(f"   النتيجة: {login_response.status_code}")
        
        # 3. محاولة تسجيل دخول real
        print("\n👤 محاولة تسجيل الدخول...")
        session = requests.Session()
        login_data = {
            'username': 'secretary',
            'password': 'secretary123'
        }
        
        login_post = session.post(f"{base_url}/login", data=login_data)
        print(f"   POST login: {login_post.status_code}")
        print(f"   URL بعد login: {login_post.url}")
        
        # 4. اختبار dashboard
        print("\n📊 اختبار dashboard...")
        dash_response = session.get(f"{base_url}/secretary/dashboard")
        print(f"   النتيجة: {dash_response.status_code}")
        
        # 5. اختبار صفحة المرضى
        print("\n👥 اختبار صفحة المرضى...")
        patients_response = session.get(f"{base_url}/secretary/patients")
        print(f"   النتيجة: {patients_response.status_code}")
        
        if patients_response.status_code != 200:
            print(f"   خطأ: {patients_response.text[:200]}")
        
        # 6. اختبار API البحث
        print("\n🔍 اختبار API البحث...")
        api_response = session.get(f"{base_url}/secretary/api/search-patients", params={'term': 'test'})
        print(f"   النتيجة: {api_response.status_code}")
        
        if api_response.status_code == 200:
            try:
                data = api_response.json()
                print(f"   ✅ API يعمل! عدد النتائج: {len(data)}")
            except:
                print(f"   ⚠️ خطأ في JSON")
        elif api_response.status_code != 200:
            print(f"   خطأ API: {api_response.text[:100]}")
            
    except requests.exceptions.ConnectionError:
        print("❌ الخادم لا يعمل")
    except Exception as e:
        print(f"❌ خطأ: {e}")

if __name__ == "__main__":
    test_server()