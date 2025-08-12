#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
اختبار خاصية البحث التلقائي بالمسارات الصحيحة
"""

import requests
import json

def test_actual_paths():
    """اختبار المسارات الفعلية"""
    
    # المسارات الصحيحة بناء على قائمة المسارات التي حصلنا عليها
    base_url = "http://127.0.0.1:5000"
    
    # المسارات الفعلية للسكرتير
    patients_url = f"{base_url}/secretary/secretary/patients"
    search_api_url = f"{base_url}/secretary/secretary/api/search-patients"
    
    print("🔍 اختبار المسارات الفعلية للسكرتير:")
    print("=" * 50)
    
    # اختبار 1: صفحة المرضى
    try:
        print(f"\n📄 اختبار: {patients_url}")
        response = requests.get(patients_url)
        
        if response.status_code == 200:
            print("✅ صفحة المرضى متاحة!")
        elif response.status_code in [302, 401]:
            print("🔒 صفحة المرضى تتطلب تسجيل دخول (صحيح أمنياً)")
        else:
            print(f"❌ خطأ: {response.status_code}")
            
    except Exception as e:
        print(f"❌ خطأ في الوصول للصفحة: {e}")
    
    # اختبار 2: API البحث
    try:
        print(f"\n🔍 اختبار: {search_api_url}?term=Naim")
        response = requests.get(f"{search_api_url}?term=Naim")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ API البحث يعمل! عدد النتائج: {len(data)}")
        elif response.status_code in [302, 401]:
            print("🔒 API البحث يتطلب تسجيل دخول (صحيح أمنياً)")
        else:
            print(f"❌ خطأ: {response.status_code}")
            
    except Exception as e:
        print(f"❌ خطأ في API البحث: {e}")
    
    print("\n" + "=" * 50)
    print("📝 الملاحظات:")
    print("1. المسارات الصحيحة هي:")
    print(f"   📍 صفحة المرضى: {patients_url}")
    print(f"   📍 API البحث: {search_api_url}")
    print("\n2. كل الاستجابات 401/302 طبيعية لأن التطبيق يتطلب تسجيل دخول")
    print("\n3. لاختبار الخاصية الفعلية:")
    print("   • افتح المتصفح")
    print("   • اذهب إلى http://127.0.0.1:5000/login")
    print("   • سجل دخول كسكرتير (secretary/secretary123)")
    print("   • اذهب إلى /secretary/secretary/patients")
    print("   • جرب البحث التلقائي!")

def test_dashboard_access():
    """اختبار الوصول للوحة التحكم"""
    dashboard_url = "http://127.0.0.1:5000/secretary/dashboard/secretary"
    
    print(f"\n🏠 اختبار لوحة تحكم السكرتير: {dashboard_url}")
    
    try:
        response = requests.get(dashboard_url)
        
        if response.status_code == 200:
            print("✅ لوحة التحكم متاحة!")
        elif response.status_code in [302, 401]:
            print("🔒 لوحة التحكم تتطلب تسجيل دخول")
            
            # محاولة معرفة إلى أين يتم التوجيه
            if response.status_code == 302:
                redirect_location = response.headers.get('Location', 'غير محدد')
                print(f"📍 التوجيه إلى: {redirect_location}")
        else:
            print(f"❌ خطأ: {response.status_code}")
            
    except Exception as e:
        print(f"❌ خطأ: {e}")

if __name__ == "__main__":
    test_actual_paths()
    test_dashboard_access()