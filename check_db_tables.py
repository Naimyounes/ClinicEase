#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
فحص جداول قاعدة البيانات
"""

import sqlite3
import os

def check_database_tables():
    """فحص جداول قاعدة البيانات"""
    
    db_path = os.path.join(os.path.dirname(__file__), 'instance', 'clinic.db')
    
    if not os.path.exists(db_path):
        print("❌ ملف قاعدة البيانات غير موجود")
        return
    
    print(f"=== فحص قاعدة البيانات ===")
    print(f"مسار قاعدة البيانات: {db_path}")
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # الحصول على قائمة الجداول
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        
        print(f"\nالجداول الموجودة ({len(tables)}):")
        for table in sorted(tables):
            print(f"  • {table[0]}")
        
        # فحص جدول predefined_prescription
        if ('predefined_prescription',) in tables:
            print(f"\n=== جدول predefined_prescription ===")
            cursor.execute("PRAGMA table_info(predefined_prescription);")
            columns = cursor.fetchall()
            print("الأعمدة:")
            for col in columns:
                print(f"  • {col[1]} ({col[2]})")
            
            cursor.execute("SELECT COUNT(*) FROM predefined_prescription;")
            count = cursor.fetchone()[0]
            print(f"عدد السجلات: {count}")
        else:
            print("\n❌ جدول predefined_prescription غير موجود")
        
        # فحص جدول predefined_prescription_medication
        if ('predefined_prescription_medication',) in tables:
            print(f"\n=== جدول predefined_prescription_medication ===")
            cursor.execute("PRAGMA table_info(predefined_prescription_medication);")
            columns = cursor.fetchall()
            print("الأعمدة:")
            for col in columns:
                print(f"  • {col[1]} ({col[2]})")
            
            cursor.execute("SELECT COUNT(*) FROM predefined_prescription_medication;")
            count = cursor.fetchone()[0]
            print(f"عدد السجلات: {count}")
        else:
            print("\n❌ جدول predefined_prescription_medication غير موجود")
        
        # فحص جدول medication
        if ('medication',) in tables:
            print(f"\n=== جدول medication ===")
            cursor.execute("SELECT COUNT(*) FROM medication;")
            count = cursor.fetchone()[0]
            print(f"عدد الأدوية: {count}")
            
            if count > 0:
                cursor.execute("SELECT name, dosage FROM medication LIMIT 5;")
                medications = cursor.fetchall()
                print("أمثلة على الأدوية:")
                for med in medications:
                    print(f"  • {med[0]} ({med[1] or 'بدون جرعة'})")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ خطأ في فحص قاعدة البيانات: {e}")

def add_quantity_column():
    """إضافة عمود الكمية إذا لم يكن موجوداً"""
    
    db_path = os.path.join(os.path.dirname(__file__), 'instance', 'clinic.db')
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # فحص وجود عمود quantity
        cursor.execute("PRAGMA table_info(predefined_prescription_medication);")
        columns = cursor.fetchall()
        column_names = [col[1] for col in columns]
        
        if 'quantity' not in column_names:
            print("إضافة عمود quantity...")
            cursor.execute("ALTER TABLE predefined_prescription_medication ADD COLUMN quantity TEXT;")
            conn.commit()
            print("✅ تم إضافة عمود quantity بنجاح")
        else:
            print("✅ عمود quantity موجود مسبقاً")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ خطأ في إضافة عمود quantity: {e}")

if __name__ == "__main__":
    check_database_tables()
    add_quantity_column()
    print("\n" + "="*50)
    check_database_tables()