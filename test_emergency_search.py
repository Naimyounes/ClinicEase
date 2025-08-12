#!/usr/bin/env python3
"""
اختبار البحث التلقائي في صفحة emergency ticket
"""
import requests
import json

def test_emergency_search():
    """اختبار شامل للبحث في صفحة emergency ticket"""
    base_url = "http://localhost:5000"
    session = requests.Session()
    
    try:
        print("🚨 اختبار البحث في صفحة emergency ticket...")
        
        # 1. تسجيل الدخول
        print("\n🔐 تسجيل الدخول...")
        login_data = {
            'username': 'secretary',
            'password': 'secretary123'
        }
        
        login_response = session.post(f"{base_url}/login", data=login_data)
        
        if login_response.status_code == 200:
            print("✅ تم تسجيل الدخول بنجاح")
            
            # 2. اختبار صفحة emergency ticket
            print("\n📋 اختبار صفحة emergency ticket...")
            emergency_response = session.get(f"{base_url}/secretary/emergency-ticket")
            print(f"   حالة الصفحة: {emergency_response.status_code}")
            
            if emergency_response.status_code == 200:
                print("✅ صفحة emergency ticket تعمل")
                
                # 3. اختبار API البحث المحدث
                print("\n🔍 اختبار API البحث...")
                
                # اختبار مع مصطلحات مختلفة
                search_terms = ['ali', 'mohamed', 'sara', 'test', 'hola']
                
                for term in search_terms:
                    print(f"\n   البحث عن: '{term}'")
                    api_response = session.get(
                        f"{base_url}/secretary/api/search-patients",
                        params={'term': term}
                    )
                    
                    print(f"   حالة API: {api_response.status_code}")
                    
                    if api_response.status_code == 200:
                        try:
                            data = api_response.json()
                            print(f"   ✅ النتائج: {len(data)} مريض")
                            
                            if data:
                                # عرض أول نتيجة
                                patient = data[0]
                                print(f"   👤 أول نتيجة: {patient.get('full_name', 'غير محدد')}")
                                print(f"   📞 الهاتف: {patient.get('phone', 'غير محدد')}")
                            else:
                                print("   ℹ️ لا توجد نتائج")
                        except json.JSONDecodeError as e:
                            print(f"   ❌ خطأ في JSON: {e}")
                            print(f"   Response: {api_response.text[:100]}")
                    else:
                        print(f"   ❌ فشل API: {api_response.status_code}")
                        print(f"   خطأ: {api_response.text[:100]}")
                        
                # 4. اختبار مع اسم غير موجود
                print(f"\n   البحث عن اسم غير موجود: 'xyz123'")
                empty_response = session.get(
                    f"{base_url}/secretary/api/search-patients",
                    params={'term': 'xyz123'}
                )
                
                if empty_response.status_code == 200:
                    empty_data = empty_response.json()
                    print(f"   ✅ النتائج للاسم غير الموجود: {len(empty_data)} مريض")
                
            else:
                print(f"❌ فشل في الوصول لصفحة emergency ticket: {emergency_response.status_code}")
                print(f"خطأ: {emergency_response.text[:200]}")
        else:
            print(f"❌ فشل تسجيل الدخول: {login_response.status_code}")
            
    except requests.exceptions.ConnectionError:
        print("❌ لا يمكن الاتصال بالخادم - تأكد من تشغيل: python run.py")
    except Exception as e:
        print(f"❌ خطأ غير متوقع: {e}")

if __name__ == "__main__":
    test_emergency_search()