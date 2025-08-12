#!/usr/bin/env python3
"""
تنظيف ملف routes.py من الدوال المكررة
"""

def clean_routes_file():
    """حذف الدوال المكررة من ملف routes.py"""
    
    routes_file = r"c:\Users\pc cam\Desktop\ClinicEase-main\clinic_app\secretary\routes.py"
    
    try:
        with open(routes_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # العد الكلي للسطور
        lines = content.split('\n')
        print(f"عدد السطور: {len(lines)}")
        
        # البحث عن الدوال المكررة
        api_functions = []
        for i, line in enumerate(lines):
            if 'def search_patients_api' in line or '@secretary.route("/secretary/api/' in line:
                api_functions.append((i+1, line.strip()))
        
        print(f"دوال API موجودة:")
        for line_num, line_content in api_functions:
            print(f"  السطر {line_num}: {line_content}")
            
        # البحث عن أسماء الدوال
        function_names = []
        for i, line in enumerate(lines):
            if line.strip().startswith('def ') and 'search' in line:
                function_names.append((i+1, line.strip()))
                
        print(f"\nدوال البحث:")
        for line_num, line_content in function_names:
            print(f"  السطر {line_num}: {line_content}")
        
    except Exception as e:
        print(f"خطأ: {e}")

if __name__ == "__main__":
    clean_routes_file()