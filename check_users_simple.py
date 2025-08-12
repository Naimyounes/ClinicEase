#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
فحص المستخدمين في قاعدة البيانات
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from clinic_app import create_app, db
from clinic_app.models import User, Patient

def check_users():
    """فحص المستخدمين والمرضى"""
    app = create_app()
    
    with app.app_context():
        print("👥 فحص المستخدمين...")
        print("=" * 40)
        
        users = User.query.all()
        print(f"📊 عدد المستخدمين: {len(users)}")
        
        for user in users:
            print(f"👤 المستخدم: {user.username} - الدور: {user.role}")
        
        print("\n🏥 فحص المرضى...")
        print("=" * 40)
        
        patients = Patient.query.all()
        print(f"📊 عدد المرضى: {len(patients)}")
        
        for i, patient in enumerate(patients[:5]):  # أول 5 مرضى فقط
            print(f"🤒 المريض {i+1}: {patient.full_name} - الهاتف: {patient.phone}")
        
        if len(patients) > 5:
            print(f"... و {len(patients) - 5} مريض آخر")

if __name__ == "__main__":
    check_users()