#!/usr/bin/env python3
"""
اختبار المسارات المتاحة في الخادم
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from clinic_app import create_app

def test_routes():
    """عرض جميع المسارات المتاحة"""
    app = create_app()
    
    with app.app_context():
        print("🔗 المسارات المتاحة في التطبيق:")
        print("="*50)
        
        # جمع جميع المسارات
        routes = []
        for rule in app.url_map.iter_rules():
            routes.append({
                'endpoint': rule.endpoint,
                'methods': list(rule.methods),
                'path': str(rule)
            })
        
        # ترتيب المسارات
        routes.sort(key=lambda x: x['path'])
        
        # عرض المسارات
        secretary_routes = []
        api_routes = []
        other_routes = []
        
        for route in routes:
            if '/secretary/' in route['path']:
                secretary_routes.append(route)
            elif '/api/' in route['path']:
                api_routes.append(route)
            else:
                other_routes.append(route)
        
        print("\n📋 مسارات Secretary:")
        for route in secretary_routes:
            methods = [m for m in route['methods'] if m not in ['HEAD', 'OPTIONS']]
            print(f"  {route['path']} -> {route['endpoint']} [{', '.join(methods)}]")
        
        print("\n🔍 مسارات API:")
        for route in api_routes:
            methods = [m for m in route['methods'] if m not in ['HEAD', 'OPTIONS']]
            print(f"  {route['path']} -> {route['endpoint']} [{', '.join(methods)}]")
        
        print("\n📝 مسارات أخرى مهمة:")
        important_routes = [r for r in other_routes if any(keyword in r['path'] for keyword in ['login', 'dashboard', 'patient'])]
        for route in important_routes:
            methods = [m for m in route['methods'] if m not in ['HEAD', 'OPTIONS']]
            print(f"  {route['path']} -> {route['endpoint']} [{', '.join(methods)}]")
        
        print(f"\n📊 إجمالي المسارات: {len(routes)}")
        print(f"   مسارات Secretary: {len(secretary_routes)}")
        print(f"   مسارات API: {len(api_routes)}")

if __name__ == "__main__":
    try:
        test_routes()
    except Exception as e:
        print(f"❌ خطأ: {e}")
        import traceback
        traceback.print_exc()