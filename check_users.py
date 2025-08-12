#!/usr/bin/env python3
"""
سكريبت للتحقق من المستخدمين في قاعدة البيانات
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from clinic_app import create_app, db
from clinic_app.models import User

def check_users():
    """التحقق من المستخدمين الموجودين"""
    app = create_app()
    
    with app.app_context():
        print("🔍 التحقق من المستخدمين...")
        
        users = User.query.all()
        
        if not users:
            print("❌ لا يوجد مستخدمين في قاعدة البيانات!")
            return
        
        print(f"📊 عدد المستخدمين: {len(users)}")
        print("-" * 50)
        
        for user in users:
            print(f"ID: {user.id}")
            print(f"اسم المستخدم: {user.username}")
            print(f"الدور: {user.role}")
            print(f"كلمة المرور (مشفرة): {user.password[:20]}...")
            print("-" * 30)

if __name__ == "__main__":
    check_users()