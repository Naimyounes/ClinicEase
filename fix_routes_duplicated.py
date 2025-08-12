#!/usr/bin/env python3
"""
إصلاح المسارات المضاعفة في ملف routes.py
"""

def fix_routes():
    """إصلاح المسارات المضاعفة"""
    routes_file = r"c:\Users\pc cam\Desktop\ClinicEase-main\clinic_app\secretary\routes.py"
    
    try:
        # قراءة الملف
        with open(routes_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        print("🔧 إصلاح المسارات المضاعفة...")
        
        # قائمة الإصلاحات المطلوبة
        replacements = [
            ('@secretary.route("/secretary/api/', '@secretary.route("/api/'),
            ('@secretary.route("/secretary/patient/', '@secretary.route("/patient/'),
            ('@secretary.route("/secretary/patients-french")', '@secretary.route("/patients-french")'),
            ('@secretary.route("/secretary/create-ticket")', '@secretary.route("/create-ticket")'),
            ('@secretary.route("/secretary/emergency-ticket")', '@secretary.route("/emergency-ticket")'),
            ('@secretary.route("/secretary/emergency-ticket/create/', '@secretary.route("/emergency-ticket/create/'),
            ('@secretary.route("/secretary/ticket/', '@secretary.route("/ticket/'),
            ('@secretary.route("/secretary/waiting-list")', '@secretary.route("/waiting-list")'),
            ('@secretary.route("/secretary/visit/', '@secretary.route("/visit/'),
            ('@secretary.route("/secretary/update-payment/', '@secretary.route("/update-payment/'),
        ]
        
        # تطبيق الإصلاحات
        changes_made = 0
        for old_pattern, new_pattern in replacements:
            if old_pattern in content:
                content = content.replace(old_pattern, new_pattern)
                changes_made += 1
                print(f"   ✅ تم إصلاح: {old_pattern} -> {new_pattern}")
        
        # كتابة الملف المحدث
        if changes_made > 0:
            with open(routes_file, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"\n🎯 تم إجراء {changes_made} إصلاحات بنجاح!")
        else:
            print("✅ لا توجد إصلاحات مطلوبة.")
            
    except Exception as e:
        print(f"❌ خطأ: {e}")

if __name__ == "__main__":
    fix_routes()