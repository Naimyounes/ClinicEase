#!/usr/bin/env python3
"""
سكريبت لتحديث قيم payment_status من العربية إلى الفرنسية
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from clinic_app import create_app, db
from clinic_app.models import Visit, Appointment

def update_payment_status():
    """تحديث قيم payment_status من العربية إلى الفرنسية"""
    app = create_app()
    
    with app.app_context():
        print("بدء تحديث قيم payment_status...")
        
        # تحديث الزيارات
        visits = Visit.query.all()
        updated_visits = 0
        
        for visit in visits:
            old_status = visit.payment_status
            
            if visit.payment_status == "مدفوع":
                visit.payment_status = "payé"
                updated_visits += 1
            elif visit.payment_status == "غير مدفوع":
                visit.payment_status = "non_payé"
                updated_visits += 1
            elif visit.payment_status == "مدفوع جزئياً":
                visit.payment_status = "partiellement_payé"
                updated_visits += 1
            
            if old_status != visit.payment_status:
                print(f"تحديث الزيارة {visit.id}: {old_status} -> {visit.payment_status}")
        
        # تحديث المواعيد
        appointments = Appointment.query.all()
        updated_appointments = 0
        
        for appointment in appointments:
            old_status = appointment.status
            
            if appointment.status == "مجدول":
                appointment.status = "Programmé"
                updated_appointments += 1
            elif appointment.status == "مكتمل":
                appointment.status = "Terminé"
                updated_appointments += 1
            elif appointment.status == "ملغي":
                appointment.status = "Annulé"
                updated_appointments += 1
            elif appointment.status == "فائت":
                appointment.status = "Manqué"
                updated_appointments += 1
            
            if old_status != appointment.status:
                print(f"تحديث الموعد {appointment.id}: {old_status} -> {appointment.status}")
        
        # حفظ التغييرات
        try:
            db.session.commit()
            print(f"✅ تم تحديث {updated_visits} زيارة و {updated_appointments} موعد بنجاح!")
        except Exception as e:
            db.session.rollback()
            print(f"❌ خطأ في حفظ التغييرات: {e}")
            return False
        
        return True

if __name__ == "__main__":
    print("🔄 تحديث قيم payment_status...")
    success = update_payment_status()
    
    if success:
        print("✅ تم التحديث بنجاح!")
    else:
        print("❌ فشل في التحديث!")