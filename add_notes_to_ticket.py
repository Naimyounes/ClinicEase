#!/usr/bin/env python3
"""
إضافة حقل notes إلى جدول التذاكر الموجود
"""

import sqlite3
import os
from clinic_app import create_app

def add_notes_column():
    """إضافة عمود notes إلى جدول ticket"""
    app = create_app()
    
    with app.app_context():
        # مسار قاعدة البيانات
        db_path = os.path.join(app.instance_path, 'clinic.db')
        
        if not os.path.exists(db_path):
            print("❌ لم يتم العثور على قاعدة البيانات")
            return
        
        try:
            # الاتصال بقاعدة البيانات
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            # التحقق من وجود العمود
            cursor.execute("PRAGMA table_info(ticket)")
            columns = [column[1] for column in cursor.fetchall()]
            
            if 'notes' not in columns:
                # إضافة العمود الجديد
                cursor.execute("ALTER TABLE ticket ADD COLUMN notes TEXT")
                conn.commit()
                print("✅ تم إضافة حقل notes إلى جدول ticket بنجاح")
            else:
                print("ℹ️ حقل notes موجود بالفعل في جدول ticket")
            
            conn.close()
            print("🎉 تم تحديث قاعدة البيانات بنجاح!")
            
        except Exception as e:
            print(f"❌ خطأ في تحديث قاعدة البيانات: {e}")

if __name__ == "__main__":
    add_notes_column()