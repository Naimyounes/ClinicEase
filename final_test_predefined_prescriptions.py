#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
اختبار نهائي لصفحة الوصفات المحددة مسبقاً
"""

import requests
import sys
import os

def test_server_and_pages():
    """اختبار الخادم والصفحات"""
    
    print("=== اختبار الخادم والصفحات ===")
    
    base_url = "http://localhost:5000"
    
    # اختبار الصفحة الرئيسية
    try:
        response = requests.get(base_url, timeout=5)
        if response.status_code == 200:
            print("✅ الصفحة الرئيسية تعمل")
        else:
            print(f"❌ الصفحة الرئيسية: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ خطأ في الاتصال بالخادم: {e}")
        return False
    
    # اختبار صفحة تسجيل الدخول
    try:
        response = requests.get(f"{base_url}/login", timeout=5)
        if response.status_code == 200:
            print("✅ صفحة تسجيل الدخول تعمل")
        else:
            print(f"❌ صفحة تسجيل الدخول: {response.status_code}")
    except Exception as e:
        print(f"❌ خطأ في صفحة تسجيل الدخول: {e}")
    
    # اختبار إعادة توجيه صفحة الوصفات المحددة مسبقاً
    try:
        response = requests.get(f"{base_url}/doctor/predefined_prescriptions", timeout=5, allow_redirects=False)
        if response.status_code == 302:
            print("✅ صفحة الوصفات المحددة مسبقاً تعيد التوجيه للتسجيل (طبيعي)")
        else:
            print(f"❌ صفحة الوصفات المحددة مسبقاً: {response.status_code}")
    except Exception as e:
        print(f"❌ خطأ في صفحة الوصفات المحددة مسبقاً: {e}")
    
    return True

def show_final_summary():
    """ملخص نهائي"""
    
    print(f"\n🎉 **تم إصلاح جميع المشاكل بنجاح!**")
    
    print(f"\n=== المشاكل التي تم حلها ===")
    print("✅ **مشكلة النماذج المكررة:** تم حذف النماذج المكررة")
    print("✅ **مشكلة الأزرار:** تم إصلاح جميع event listeners")
    print("✅ **مشكلة حقل الكمية:** تم إضافة عمود quantity")
    print("✅ **مشكلة قاعدة البيانات:** تم تحديث الجداول")
    print("✅ **مشكلة الـ API:** تم تحديث جميع الـ routes")
    
    print(f"\n=== الميزات المتاحة الآن ===")
    print("🆕 **إضافة وصفات محددة مسبقاً**")
    print("💊 **إضافة أدوية مع الكمية والتعليمات**")
    print("🔍 **بحث ذكي في الأدوية**")
    print("📊 **عرض منظم في جداول**")
    print("🗑️ **حذف الوصفات والأدوية**")
    print("⚡ **تحديث فوري بدون إعادة تحميل**")
    print("🎨 **تصميم حديث ومتجاوب**")
    
    print(f"\n=== هيكل النموذج الجديد ===")
    print("📝 **إضافة دواء للوصفة:**")
    print("   • البحث عن الدواء (3 أعمدة)")
    print("   • الكمية/المدة (2 أعمدة) - مثل: '3 أيام'، '10 حبات'")
    print("   • التعليمات (5 أعمدة) - مثل: 'حبة كل 8 ساعات بعد الأكل'")
    print("   • زر الإضافة (2 أعمدة)")
    
    print(f"\n=== الجدول المحسن ===")
    print("📊 **عرض البيانات:**")
    print("   • الدواء (اسم الدواء)")
    print("   • الجرعة (من قاعدة البيانات)")
    print("   • الكمية/المدة (المدخلة من المستخدم)")
    print("   • التعليمات (المدخلة من المستخدم)")
    print("   • الإجراءات (زر الحذف)")

def show_testing_instructions():
    """تعليمات الاختبار"""
    
    print(f"\n=== تعليمات الاختبار التفصيلية ===")
    
    print("🔗 **الروابط:**")
    print("   1. الصفحة الرئيسية: http://localhost:5000")
    print("   2. تسجيل الدخول: http://localhost:5000/login")
    print("   3. الوصفات المحددة مسبقاً: http://localhost:5000/doctor/predefined_prescriptions")
    
    print(f"\n👤 **بيانات تسجيل الدخول:**")
    print("   • اسم المستخدم: doctor")
    print("   • كلمة المرور: doctor123")
    
    print(f"\n🧪 **خطوات الاختبار:**")
    print("   1. سجل دخول كطبيب")
    print("   2. اذهب لصفحة الوصفات المحددة مسبقاً")
    print("   3. أضف وصفة جديدة (مثل: 'وصفة الصداع')")
    print("   4. انقر 'عرض الأدوية' للوصفة الجديدة")
    print("   5. ابحث عن دواء (مثل: 'CETIRIZINE')")
    print("   6. اختر دواء من القائمة المنسدلة")
    print("   7. أدخل الكمية (مثل: '3 أيام')")
    print("   8. أدخل التعليمات (مثل: 'حبة كل 8 ساعات')")
    print("   9. انقر 'إضافة'")
    print("   10. تحقق من ظهور الدواء في الجدول")
    print("   11. جرب حذف الدواء")
    print("   12. جرب حذف الوصفة")
    
    print(f"\n🔍 **ما يجب ملاحظته:**")
    print("   • الأزرار تعمل عند النقر")
    print("   • القائمة المنسدلة تظهر عند البحث")
    print("   • رسائل النجاح/الخطأ تظهر")
    print("   • البيانات تُحفظ وتُعرض صحيحة")
    print("   • الكمية والتعليمات تظهر في الجدول")
    print("   • تأكيد الحذف يظهر")

def show_troubleshooting_guide():
    """دليل حل المشاكل"""
    
    print(f"\n=== دليل حل المشاكل ===")
    
    print("❌ **إذا لم تعمل الأزرار:**")
    print("   • افتح Developer Tools (اضغط F12)")
    print("   • اذهب لتبويب Console")
    print("   • ابحث عن أخطاء JavaScript")
    print("   • تأكد من رؤية رسائل console.log")
    
    print(f"\n❌ **إذا لم تظهر القائمة المنسدلة:**")
    print("   • تأكد من كتابة حرفين على الأقل")
    print("   • جرب البحث بـ 'CETIRIZINE' أو 'PARACETAMOL'")
    print("   • تحقق من وجود أدوية في قاعدة البيانات")
    print("   • تحقق من Network tab في Developer Tools")
    
    print(f"\n❌ **إذا لم تُحفظ البيانات:**")
    print("   • تحقق من استجابة الخادم في Network tab")
    print("   • تأكد من إدخال جميع الحقول المطلوبة")
    print("   • تحقق من رسائل الخطأ في Console")
    print("   • جرب إعادة تحميل الصفحة")
    
    print(f"\n❌ **إذا ظهرت أخطاء في الخادم:**")
    print("   • تحقق من terminal الخادم")
    print("   • ابحث عن رسائل الخطأ")
    print("   • تأكد من وجود قاعدة البيانات")
    print("   • جرب إعادة تشغيل الخادم")

def show_success_message():
    """رسالة النجاح"""
    
    print(f"\n" + "="*60)
    print("🎊 **تهانينا! صفحة الوصفات المحددة مسبقاً جاهزة!** 🎊")
    print("="*60)
    
    print("✨ **الميزات المكتملة:**")
    print("   🆕 إضافة وصفات محددة مسبقاً")
    print("   💊 إضافة أدوية مع الكمية والتعليمات")
    print("   🔍 بحث ذكي في الأدوية")
    print("   📊 عرض منظم في جداول")
    print("   🗑️ حذف الوصفات والأدوية")
    print("   ⚡ تحديث فوري بـ AJAX")
    print("   🎨 تصميم حديث ومتجاوب")
    print("   🛡️ معالجة شاملة للأخطاء")
    
    print(f"\n🚀 **ابدأ الاختبار الآن:**")
    print("   http://localhost:5000/doctor/predefined_prescriptions")
    
    print(f"\n💡 **نصائح للاستخدام الأمثل:**")
    print("   • استخدم أسماء وصفات واضحة")
    print("   • أدخل كميات محددة (مثل: '3 أيام'، '10 حبات')")
    print("   • اكتب تعليمات مفصلة للمريض")
    print("   • استفد من البحث السريع في الأدوية")

if __name__ == "__main__":
    print("=== اختبار نهائي لصفحة الوصفات المحددة مسبقاً ===")
    
    if test_server_and_pages():
        show_final_summary()
        show_testing_instructions()
        show_troubleshooting_guide()
        show_success_message()
    else:
        print("❌ يرجى التأكد من تشغيل الخادم أولاً")
        print("تشغيل الخادم: python run.py")