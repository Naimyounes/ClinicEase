#!/usr/bin/env python3
"""
اختبار مباشر لـ API مع تفاصيل أكثر
"""
import requests
import json

def test_api_detailed():
    """اختبار مفصل لـ API"""
    base_url = "http://localhost:5000"
    session = requests.Session()
    
    try:
        print("🔍 اختبار API مفصل...")
        
        # 1. تسجيل الدخول بتفاصيل أكثر
        print("\n🔐 تسجيل الدخول...")
        login_data = {
            'username': 'secretary',
            'password': 'secretary123'
        }
        
        login_response = session.post(f"{base_url}/login", data=login_data, allow_redirects=False)
        print(f"   حالة تسجيل الدخول: {login_response.status_code}")
        print(f"   Headers: {dict(login_response.headers)}")
        
        if 'Location' in login_response.headers:
            print(f"   إعادة توجيه إلى: {login_response.headers['Location']}")
        
        # 2. اتباع إعادة التوجيه
        if login_response.status_code in [302, 301]:
            redirect_response = session.get(login_response.headers['Location'])
            print(f"   حالة بعد إعادة التوجيه: {redirect_response.status_code}")
        
        # 3. اختبار dashboard للتأكد من تسجيل الدخول
        print("\n📊 اختبار dashboard...")
        dashboard_response = session.get(f"{base_url}/secretary/dashboard")
        print(f"   حالة dashboard: {dashboard_response.status_code}")
        
        if dashboard_response.status_code == 200:
            print("✅ تم تسجيل الدخول بنجاح")
            
            # 4. اختبار API مع headers مفصلة
            print("\n🔍 اختبار API البحث...")
            api_url = f"{base_url}/secretary/api/search-patients"
            
            # إضافة headers مفيدة
            headers = {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
                'X-Requested-With': 'XMLHttpRequest'
            }
            
            api_response = session.get(
                api_url, 
                params={'term': 'ali'}, 
                headers=headers,
                allow_redirects=False
            )
            
            print(f"   حالة API: {api_response.status_code}")
            print(f"   Content-Type: {api_response.headers.get('Content-Type', 'غير محدد')}")
            print(f"   Response headers: {dict(api_response.headers)}")
            
            if api_response.status_code == 200:
                print(f"   Response text (أول 200 حرف): {api_response.text[:200]}")
                
                try:
                    data = api_response.json()
                    print(f"   ✅ JSON صحيح! عدد النتائج: {len(data)}")
                except:
                    print("   ❌ ليس JSON - يبدو أنه HTML")
                    
            elif api_response.status_code in [302, 301]:
                print(f"   ⚠️ إعادة توجيه إلى: {api_response.headers.get('Location', 'غير محدد')}")
            else:
                print(f"   ❌ خطأ: {api_response.status_code}")
                print(f"   Response: {api_response.text[:200]}")
                
        else:
            print(f"❌ فشل في الوصول لdashboard: {dashboard_response.status_code}")
            print(f"Response: {dashboard_response.text[:200]}")
            
    except Exception as e:
        print(f"❌ خطأ: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_api_detailed()