#!/usr/bin/env python3
"""
سكريبت لاختبار الوصول إلى صفحة payments
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from clinic_app import create_app
from flask import url_for

def test_payments_access():
    """اختبار الوصول إلى صفحة payments"""
    app = create_app()
    
    with app.app_context():
        print("🔍 اختبار routes المتاحة...")
        
        # طباعة جميع الـ routes
        for rule in app.url_map.iter_rules():
            if 'secretary' in rule.endpoint:
                print(f"Route: {rule.rule} -> {rule.endpoint}")
        
        print("\n" + "="*50)
        
        # اختبار URL للـ payments
        try:
            payments_url = url_for('secretary.payments')
            print(f"✅ URL للـ payments: {payments_url}")
        except Exception as e:
            print(f"❌ خطأ في إنشاء URL للـ payments: {e}")
        
        # اختبار URL للـ dashboard
        try:
            dashboard_url = url_for('secretary.dashboard')
            print(f"✅ URL للـ dashboard: {dashboard_url}")
        except Exception as e:
            print(f"❌ خطأ في إنشاء URL للـ dashboard: {e}")

if __name__ == "__main__":
    test_payments_access()