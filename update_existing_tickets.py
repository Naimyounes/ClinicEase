#!/usr/bin/env python3
"""
تحديث التذاكر الموجودة لضمان وجود القيم الافتراضية الصحيحة
"""

from clinic_app import create_app, db
from clinic_app.models import Ticket

def update_existing_tickets():
    """تحديث التذاكر الموجودة"""
    app = create_app()
    
    with app.app_context():
        try:
            # الحصول على جميع التذاكر
            tickets = Ticket.query.all()
            updated_count = 0
            
            for ticket in tickets:
                updated = False
                
                # تحديث ticket_type إذا كان فارغاً
                if not ticket.ticket_type:
                    ticket.ticket_type = "regular"
                    updated = True
                
                # تحديث priority إذا كان فارغاً
                if ticket.priority is None:
                    ticket.priority = 0
                    updated = True
                
                if updated:
                    updated_count += 1
            
            # حفظ التغييرات
            if updated_count > 0:
                db.session.commit()
                print(f"✅ تم تحديث {updated_count} تذكرة")
            else:
                print("ℹ️ جميع التذاكر محدثة بالفعل")
            
            print("🎉 تم تحديث التذاكر الموجودة بنجاح!")
            
        except Exception as e:
            print(f"❌ خطأ في تحديث التذاكر: {e}")
            db.session.rollback()

if __name__ == "__main__":
    update_existing_tickets()