#!/usr/bin/env python3
"""
اختبار مباشر لـ API البحث مع تفاصيل أكثر
"""
import requests
import json

def test_search_detailed():
    """اختبار مفصل لـ API البحث"""
    base_url = "http://localhost:5000"
    session = requests.Session()
    
    try:
        print("🔍 اختبار مفصل لـ API البحث...")
        
        # 1. تسجيل الدخول
        print("\n📝 تسجيل الدخول...")
        login_data = {
            'username': 'secretary',
            'password': 'secretary123'
        }
        
        login_response = session.post(f"{base_url}/login", data=login_data)
        print(f"   حالة تسجيل الدخول: {login_response.status_code}")
        
        if login_response.status_code == 200:
            # 2. الذهاب لصفحة المرضى أولاً
            print("\n📋 الذهاب لصفحة المرضى...")
            patients_response = session.get(f"{base_url}/secretary/patients")
            print(f"   حالة صفحة المرضى: {patients_response.status_code}")
            
            if patients_response.status_code == 200:
                # 3. اختبار API البحث
                print("\n🔎 اختبار API البحث...")
                
                # اختبار عدة مسارات ممكنة
                api_paths = [
                    "/secretary/api/search-patients",
                    "/api/search-patients", 
                    "/secretary/search-patients"
                ]
                
                for api_path in api_paths:
                    print(f"\n   تجربة المسار: {api_path}")
                    full_url = f"{base_url}{api_path}"
                    
                    search_response = session.get(full_url, params={'term': 'hola'})
                    print(f"   النتيجة: {search_response.status_code}")
                    
                    if search_response.status_code == 200:
                        try:
                            data = search_response.json()
                            print(f"   ✅ نجح! عدد النتائج: {len(data)}")
                            if data:
                                print(f"   📝 أول نتيجة: {data[0]['full_name']}")
                            break
                        except:
                            print(f"   ⚠️ خطأ في JSON: {search_response.text[:100]}")
                    else:
                        print(f"   ❌ فشل: {search_response.status_code}")
            else:
                print(f"   ❌ فشل في الوصول لصفحة المرضى: {patients_response.status_code}")
        else:
            print(f"   ❌ فشل تسجيل الدخول: {login_response.status_code}")
            
    except requests.exceptions.ConnectionError:
        print("❌ لا يمكن الاتصال بالخادم")
    except Exception as e:
        print(f"❌ خطأ: {e}")

if __name__ == "__main__":
    test_search_detailed()