#!/usr/bin/env python3
"""
Test script to verify the boating service setup
Run this after installing dependencies to check if everything is working
"""

import sys
import os
import importlib

def test_imports():
    """Test if all required packages can be imported"""
    print("Testing package imports...")
    
    required_packages = [
        'flask',
        'dotenv',
        'razorpay',
        'requests',
        'gspread',
        'google.auth',
        'reportlab',
        'flask_mail',
        'werkzeug'
    ]
    
    failed_imports = []
    
    for package in required_packages:
        try:
            importlib.import_module(package)
            print(f"✓ {package}")
        except ImportError as e:
            print(f"✗ {package}: {e}")
            failed_imports.append(package)
    
    if failed_imports:
        print(f"\nFailed to import: {', '.join(failed_imports)}")
        print("Please install missing packages: pip install -r requirements.txt")
        return False
    
    print("✓ All packages imported successfully")
    return True

def test_config():
    """Test configuration loading"""
    print("\nTesting configuration...")
    
    try:
        from config import Dev
        config = Dev()
        
        # Check if required configs exist
        required_configs = [
            'SECRET_KEY',
            'RAZORPAY_KEY_ID',
            'RAZORPAY_KEY_SECRET',
            'MAIL_SERVER',
            'MAIL_USERNAME',
            'MAIL_PASSWORD',
            'GOOGLE_SERVICE_ACCOUNT',
            'GOOGLE_SHEET_ID',
            'ADMIN_USERNAME',
            'ADMIN_PASSWORD'
        ]
        
        missing_configs = []
        for config_name in required_configs:
            if not getattr(config, config_name, None):
                missing_configs.append(config_name)
        
        if missing_configs:
            print(f"⚠ Missing environment variables: {', '.join(missing_configs)}")
            print("Please set these in your .env file")
        else:
            print("✓ All configuration variables found")
        
        return True
        
    except Exception as e:
        print(f"✗ Configuration error: {e}")
        return False

def test_file_structure():
    """Test if all required files and directories exist"""
    print("\nTesting file structure...")
    
    required_files = [
        'app.py',
        'config.py',
        'requirements.txt',
        'templates/base.html',
        'templates/index.html',
        'templates/customer.html',
        'templates/pay.html',
        'templates/success.html',
        'templates/admin.html',
        'static/css/styles.css',
        'static/js/main.js',
        'static/js/admin.js',
        'services/gsheet.py',
        'services/emailer.py',
        'services/pdf_ticket.py',
        'services/storage.py',
        'data/slots.json'
    ]
    
    missing_files = []
    
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"✓ {file_path}")
        else:
            print(f"✗ {file_path}")
            missing_files.append(file_path)
    
    if missing_files:
        print(f"\nMissing files: {', '.join(missing_files)}")
        return False
    
    print("✓ All required files found")
    return True

def test_flask_app():
    """Test if Flask app can be created"""
    print("\nTesting Flask application...")
    
    try:
        from app import app
        print("✓ Flask app created successfully")
        
        # Test basic route
        with app.test_client() as client:
            response = client.get('/')
            if response.status_code == 200:
                print("✓ Home route working")
            else:
                print(f"✗ Home route returned status {response.status_code}")
                return False
        
        return True
        
    except Exception as e:
        print(f"✗ Flask app error: {e}")
        return False

def main():
    """Run all tests"""
    print("Boating Service Setup Test")
    print("=" * 40)
    
    tests = [
        test_imports,
        test_config,
        test_file_structure,
        test_flask_app
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"✗ Test failed with exception: {e}")
    
    print("\n" + "=" * 40)
    print(f"Tests passed: {passed}/{total}")
    
    if passed == total:
        print("🎉 All tests passed! Your setup is ready.")
        print("\nNext steps:")
        print("1. Configure your .env file with actual values")
        print("2. Set up Google Sheets integration")
        print("3. Configure Razorpay keys")
        print("4. Set up email settings")
        print("5. Run: python app.py")
    else:
        print("❌ Some tests failed. Please fix the issues above.")
        sys.exit(1)

if __name__ == "__main__":
    main()
