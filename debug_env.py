
import os
import django
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hospital_management.settings')
django.setup()

def check_env():
    print("--- Checking Template Settings ---")
    for t in settings.TEMPLATES:
        print(f"BACKEND: {t['BACKEND']}")
        print(f"DIRS: {t['DIRS']}")
        print(f"APP_DIRS: {t['APP_DIRS']}")

    print("\n--- Reading Global Template File ---")
    path = os.path.join(settings.BASE_DIR, 'templates', 'doctors', 'doctor_list.html')
    print(f"Path: {path}")
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
            if "{% if selected_city == city %}" in content:
                print("SUCCESS: Found correct spacing in 'selected_city == city'")
            elif "{% if selected_city==city %}" in content:
                print("FAIL: Found BAD spacing 'selected_city==city'")
            else:
                print("FAIL: Could not find the IF tag at all.")
                # Print around the area
                idx = content.find("selected_city")
                if idx != -1:
                    print(f"Context: {content[idx-10:idx+20]}")
    else:
        print("FAIL: File not found at expected path.")

if __name__ == '__main__':
    check_env()
