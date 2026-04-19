"""
Verify that CareConnect is ready for deployment
"""
import os
import sys

def check_file(filepath, name, required=True):
    """Check if a file exists"""
    exists = os.path.exists(filepath)
    status = "✓" if exists else ("✗" if required else "⚠")
    print(f"{status} {name}: {'Found' if exists else 'MISSING'}")
    return exists

def check_file_size(filepath, name, max_mb=50):
    """Check file size"""
    if os.path.exists(filepath):
        size_mb = os.path.getsize(filepath) / (1024 * 1024)
        if size_mb > max_mb:
            print(f"  ⚠ Warning: {name} is {size_mb:.1f}MB (may slow deployment)")
            return False
        else:
            print(f"  ✓ Size: {size_mb:.2f}MB")
            return True
    return False

def main():
    print("="*50)
    print("  CARECONNECT DEPLOYMENT READINESS CHECK")
    print("="*50)
    print()
    
    all_good = True
    
    # Critical files
    print("CRITICAL FILES:")
    print("-" * 50)
    all_good &= check_file("app_fixed.py", "Main application")
    all_good &= check_file("requirements.txt", "Dependencies")
    all_good &= check_file("Procfile", "Server config")
    all_good &= check_file("runtime.txt", "Python version")
    all_good &= check_file("model.pkl", "ML model")
    print()
    
    # Check model size
    if os.path.exists("model.pkl"):
        check_file_size("model.pkl", "ML model", max_mb=5)
        print()
    
    # Templates
    print("TEMPLATES:")
    print("-" * 50)
    templates = [
        "templates/base.html",
        "templates/index.html",
        "templates/login.html",
        "templates/register.html",
        "templates/dashboard.html",
        "templates/health_input.html"
    ]
    for t in templates:
        check_file(t, os.path.basename(t))
    print()
    
    # Static files
    print("STATIC FILES:")
    print("-" * 50)
    check_file("static/css/style.css", "CSS")
    print()
    
    # Dataset
    print("DATASET:")
    print("-" * 50)
    if check_file("Dataset/healthcare_dataset.xlsx", "Training data"):
        check_file_size("Dataset/healthcare_dataset.xlsx", "Dataset", max_mb=20)
    print()
    
    # Check Procfile content
    print("CONFIGURATION CHECK:")
    print("-" * 50)
    try:
        with open("Procfile", "r") as f:
            procfile_content = f.read().strip()
            if "app_fixed:app" in procfile_content:
                print("✓ Procfile points to app_fixed:app")
            else:
                print("✗ Procfile should contain: web: gunicorn app_fixed:app")
                all_good = False
    except:
        print("✗ Could not read Procfile")
        all_good = False
    
    # Check requirements
    try:
        with open("requirements.txt", "r") as f:
            reqs = f.read()
            required_packages = ["Flask", "Flask-SQLAlchemy", "gunicorn", "psycopg2-binary"]
            for pkg in required_packages:
                if pkg in reqs:
                    print(f"✓ {pkg} in requirements")
                else:
                    print(f"✗ {pkg} missing from requirements")
                    all_good = False
    except:
        print("✗ Could not read requirements.txt")
        all_good = False
    
    print()
    print("="*50)
    
    if all_good:
        print("✅ ALL CHECKS PASSED!")
        print()
        print("Your app is ready to deploy!")
        print()
        print("Next steps:")
        print("1. git add .")
        print("2. git commit -m 'Ready for deployment'")
        print("3. git push origin main")
        print("4. Follow DEPLOY_NOW.md")
        print()
        print("="*50)
        return 0
    else:
        print("⚠ SOME ISSUES FOUND")
        print()
        print("Please fix the issues above before deploying.")
        print("See DEPLOY_NOW.md for help.")
        print()
        print("="*50)
        return 1

if __name__ == "__main__":
    sys.exit(main())
