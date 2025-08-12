#!/usr/bin/env python3
"""
تحديث جدول إعدادات الطبيب لإضافة حقل شعار العيادة (النسخة الثالثة)
إضافة: clinic_logo
"""

import sqlite3
import os
from datetime import datetime

def update_doctor_settings_table_v3():
    """إضافة حقل شعار العيادة لجدول إعدادات الطبيب - النسخة الثالثة"""
    
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
        
        # العمود الجديد المطلوب إضافته في النسخة الثالثة
        new_columns_v3 = [
            ('clinic_logo', 'VARCHAR(200)')
        ]
        
        # إضافة العمود الجديد إذا لم يكن موجوداً
        for column_name, column_type in new_columns_v3:
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
    print("🔄 بدء تحديث جدول إعدادات الطبيب (النسخة الثالثة)...")
    print("📝 إضافة: حقل شعار العيادة (clinic_logo)")
    success = update_doctor_settings_table_v3()
    
    if success:
        print("\n🎉 تم التحديث بنجاح! يمكنك الآن رفع شعار العيادة.")
        print("📋 الحقل الجديد المضاف:")
        print("   - clinic_logo: مسار شعار العيادة")
        print("\n💡 ملاحظات:")
        print("   - يُسمح بملفات الصور (JPG, PNG, GIF)")
        print("   - سيتم تحسين الصورة تلقائياً")
        print("   - الحد الأقصى المُوصى به: 300x300 بكسل")
    else:
        print("\n❌ فشل في التحديث. يرجى المحاولة مرة أخرى.")