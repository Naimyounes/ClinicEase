#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
اختبار بسيط للـ API
"""

import sys
import os

# إضافة مسار المشروع
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from clinic_app import create_app, db
from clinic_app.models import PredefinedPrescription, User

def test_database_directly():
    """اختبار قاعدة البيانات مباشرة"""
    
    print("=== اختبار قاعدة البيانات مباشرة ===")
    
    app = create_app()
    
    with app.app_context():
        try:
            # 1. اختبار الاتصال بقاعدة البيانات
            print("1. اختبار الاتصال بقاعدة البيانات...")
            users_count = User.query.count()
            print(f"   ✅ عدد المستخدمين: {users_count}")
            
            # 2. اختبار جدول الوصفات المحددة مسبقاً
            print("\n2. اختبار جدول الوصفات المحددة مسبقاً...")
            prescriptions_count = PredefinedPrescription.query.count()
            print(f"   ✅ عدد الوصفات الحالية: {prescriptions_count}")
            
            # 3. اختبار إضافة وصفة جديدة
            print("\n3. اختبار إضافة وصفة جديدة...")
            from datetime import datetime
            test_name = f"وصفة اختبار {datetime.now().strftime('%H:%M:%S')}"
            
            # التحقق من عدم وجود وصفة بنفس الاسم
            existing = PredefinedPrescription.query.filter_by(name=test_name).first()
            if existing:
                print(f"   ⚠️ وصفة بهذا الاسم موجودة مسبقاً: {test_name}")
                return
            
            # إضافة الوصفة
            new_prescription = PredefinedPrescription(name=test_name)
            db.session.add(new_prescription)
            db.session.commit()
            
            print(f"   ✅ تم إضافة الوصفة: {test_name}")
            print(f"   ✅ ID الوصفة الجديدة: {new_prescription.id}")
            
            # 4. التحقق من الإضافة
            print("\n4. التحقق من الإضافة...")
            updated_count = PredefinedPrescription.query.count()
            print(f"   ✅ عدد الوصفات بعد الإضافة: {updated_count}")
            
            # 5. عرض جميع الوصفات
            print("\n5. عرض جميع الوصفات:")
            all_prescriptions = PredefinedPrescription.query.all()
            for prescription in all_prescriptions:
                meds_count = len(prescription.medications)
                print(f"   • {prescription.name} (ID: {prescription.id}, أدوية: {meds_count})")
            
            print(f"\n✅ قاعدة البيانات تعمل بشكل صحيح!")
            
        except Exception as e:
            print(f"❌ خطأ في قاعدة البيانات: {e}")
            db.session.rollback()

def test_user_authentication():
    """اختبار المستخدمين"""
    
    print(f"\n=== اختبار المستخدمين ===")
    
    app = create_app()
    
    with app.app_context():
        try:
            # البحث عن مستخدم doctor
            doctor_user = User.query.filter_by(username='doctor').first()
            if doctor_user:
                print(f"✅ مستخدم doctor موجود:")
                print(f"   • الاسم: {doctor_user.username}")
                print(f"   • الدور: {doctor_user.role}")
                print(f"   • نشط: {doctor_user.is_active}")
            else:
                print("❌ مستخدم doctor غير موجود")
                
                # عرض جميع المستخدمين
                all_users = User.query.all()
                print(f"المستخدمون الموجودون ({len(all_users)}):")
                for user in all_users:
                    print(f"   • {user.username} ({user.role})")
            
        except Exception as e:
            print(f"❌ خطأ في فحص المستخدمين: {e}")

def test_api_route_manually():
    """اختبار route الـ API يدوياً"""
    
    print(f"\n=== اختبار API Route يدوياً ===")
    
    app = create_app()
    
    with app.test_client() as client:
        try:
            # محاولة الوصول للـ API بدون تسجيل دخول
            print("1. اختبار GET بدون تسجيل دخول...")
            response = client.get('/doctor/api/predefined_prescriptions')
            print(f"   الاستجابة: {response.status_code}")
            
            if response.status_code == 302:
                print("   ✅ إعادة توجيه للتسجيل (طبيعي)")
            elif response.status_code == 200:
                print("   ⚠️ وصول بدون تسجيل دخول!")
            else:
                print(f"   ❌ خطأ غير متوقع: {response.status_code}")
            
            # محاولة POST بدون تسجيل دخول
            print("\n2. اختبار POST بدون تسجيل دخول...")
            test_data = {'name': 'وصفة اختبار API'}
            response = client.post('/doctor/api/predefined_prescriptions', 
                                 json=test_data,
                                 content_type='application/json')
            print(f"   الاستجابة: {response.status_code}")
            
            if response.status_code == 302:
                print("   ✅ إعادة توجيه للتسجيل (طبيعي)")
            elif response.status_code == 200:
                print("   ⚠️ وصول بدون تسجيل دخول!")
            else:
                print(f"   ❌ خطأ غير متوقع: {response.status_code}")
                
        except Exception as e:
            print(f"❌ خطأ في اختبار API: {e}")

def show_javascript_debugging():
    """نصائح تشخيص JavaScript"""
    
    print(f"\n=== تشخيص JavaScript ===")
    
    print("🔍 **خطوات التشخيص:**")
    print("1. افتح الصفحة: http://localhost:5000/doctor/predefined_prescriptions")
    print("2. سجل دخول: doctor / doctor123")
    print("3. افتح Developer Tools (F12)")
    print("4. اذهب لتبويب Console")
    print("5. أدخل اسم وصفة وانقر 'Ajouter l'ordonnance'")
    print("6. راقب الرسائل في Console")
    
    print(f"\n🔍 **ما يجب أن تراه:**")
    print("   • '📝 إرسال نموذج إضافة الوصفة'")
    print("   • '➕ إضافة وصفة جديدة: [الاسم]'")
    print("   • '📥 استجابة إضافة الوصفة: {...}'")
    
    print(f"\n🔍 **إذا لم تر الرسائل:**")
    print("   • المشكلة في event listener")
    print("   • تحقق من أخطاء JavaScript")
    print("   • جرب إعادة تحميل الصفحة")
    
    print(f"\n🔍 **إذا رأيت خطأ في Network:**")
    print("   • اذهب لتبويب Network")
    print("   • ابحث عن طلب POST للـ API")
    print("   • تحقق من status code والاستجابة")
    print("   • تحقق من بيانات الطلب")

if __name__ == "__main__":
    print("=== اختبار شامل للوصفات المحددة مسبقاً ===")
    
    test_database_directly()
    test_user_authentication()
    test_api_route_manually()
    show_javascript_debugging()
    
    print(f"\n=== الخلاصة ===")
    print("✅ إذا نجحت الاختبارات أعلاه:")
    print("   • قاعدة البيانات تعمل")
    print("   • النماذج صحيحة")
    print("   • API routes موجودة")
    print("   • المشكلة في JavaScript أو المتصفح")
    
    print(f"\n❌ إذا فشلت الاختبارات:")
    print("   • هناك مشكلة في الخادم")
    print("   • تحقق من رسائل الخطأ أعلاه")
    print("   • راجع logs الخادم")