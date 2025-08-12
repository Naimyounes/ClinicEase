#!/usr/bin/env python3
"""
تحديث جدول إعدادات الطبيب لإضافة الحقول الجديدة
"""

import sqlite3
import os
from datetime import datetime

def update_doctor_settings_table():
    """إضافة الحقول الجديدة لجدول إعدادات الطبيب"""
    
    # مسار قاعدة البيانات
    db_paths = [
        'instance/clinic.db',
        'clinic_app/clinic.db'
    ]
    
    # البحث عن قاعدة البيانات
    db_path = None
    for path in db_paths:
        if os.path.exists(path):
            db_path = path
            break
    
    if not db_path:
        print("❌ لم يتم العثور على قاعدة البيانات")
        return False
    
    print(f"📁 استخدام قاعدة البيانات: {db_path}")
    
    try:
        # الاتصال بقاعدة البيانات
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # التحقق من وجود الجدول
        cursor.execute("""
            SELECT name FROM sqlite_master 
            WHERE type='table' AND name='doctor_settings'
        """)
        
        if not cursor.fetchone():
            print("❌ جدول doctor_settings غير موجود")
            return False
        
        # التحقق من الأعمدة الموجودة
        cursor.execute("PRAGMA table_info(doctor_settings)")
        existing_columns = [column[1] for column in cursor.fetchall()]
        print(f"📋 الأعمدة الموجودة: {existing_columns}")
        
        # الأعمدة الجديدة المطلوب إضافتها
        new_columns = [
            ('doctor_name_arabic', 'VARCHAR(100)'),
            ('doctor_name_latin', 'VARCHAR(100)'),
            ('clinic_name', 'VARCHAR(100)'),
            ('doctor_specialty', 'VARCHAR(100)')
        ]
        
        # إضافة الأعمدة الجديدة إذا لم تكن موجودة
        for column_name, column_type in new_columns:
            if column_name not in existing_columns:
                try:
                    cursor.execute(f"ALTER TABLE doctor_settings ADD COLUMN {column_name} {column_type}")
                    print(f"✅ تم إضافة العمود: {column_name}")
                except sqlite3.Error as e:
                    print(f"❌ خطأ في إضافة العمود {column_name}: {e}")
            else:
                print(f"ℹ️  العمود {column_name} موجود مسبقاً")
        
        # حفظ التغييرات
        conn.commit()
        print("✅ تم تحديث قاعدة البيانات بنجاح!")
        
        # عرض هيكل الجدول المحدث
        cursor.execute("PRAGMA table_info(doctor_settings)")
        columns = cursor.fetchall()
        print("\n📊 هيكل جدول doctor_settings المحدث:")
        for column in columns:
            print(f"   - {column[1]} ({column[2]})")
        
        return True
        
    except sqlite3.Error as e:
        print(f"❌ خطأ في قاعدة البيانات: {e}")
        return False
    
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    print("🔄 بدء تحديث جدول إعدادات الطبيب...")
    success = update_doctor_settings_table()
    
    if success:
        print("\n🎉 تم التحديث بنجاح! يمكنك الآن استخدام الإعدادات الجديدة.")
    else:
        print("\n❌ فشل في التحديث. يرجى المحاولة مرة أخرى.")