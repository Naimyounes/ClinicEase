#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
فحص المسارات المتاحة في التطبيق
"""

from clinic_app import create_app
from flask import url_for

def check_all_routes():
    """فحص جميع المسارات المتاحة"""
    app = create_app()
    
    with app.app_context():
        print("🔍 المسارات المتاحة في التطبيق:")
        print("=" * 60)
        
        rules = []
        for rule in app.url_map.iter_rules():
            if "GET" in rule.methods:
                rules.append({
                    'endpoint': rule.endpoint,
                    'methods': list(rule.methods),
                    'rule': rule.rule
                })
        
        # ترتيب المسارات
        rules.sort(key=lambda x: x['rule'])
        
        for rule_info in rules:
            print(f"📍 {rule_info['rule']}")
            print(f"   Endpoint: {rule_info['endpoint']}")
            print(f"   Methods: {rule_info['methods']}")
            print()
        
        print("=" * 60)
        print(f"📊 إجمالي المسارات: {len(rules)}")
        
        # اختبار مسارات السكرتير
        print("\n🧪 اختبار مسارات السكرتير:")
        secretary_routes = [rule for rule in rules if 'secretary' in rule['rule']]
        for route in secretary_routes:
            print(f"✅ {route['rule']} -> {route['endpoint']}")

if __name__ == "__main__":
    check_all_routes()