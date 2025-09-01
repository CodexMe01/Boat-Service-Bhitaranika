#!/usr/bin/env python3
"""
Test Environment Setup for Boat Service
This script sets up a complete test environment with mock services
"""

import os
import sys

def setup_test_environment():
    """Set up complete test environment"""
    
    print("🚤 Setting up Boat Service Test Environment")
    print("=" * 50)
    
    # Set environment variables for testing
    test_config = {
        'FLASK_ENV': 'development',
        'SECRET_KEY': 'test-secret-key-12345',
        'RAZORPAY_KEY_ID': 'rzp_test_1DP5mmOlF5G5ag',
        'RAZORPAY_KEY_SECRET': 'thisisasamplesecretkey',
        'MAIL_SERVER': 'smtp.gmail.com',
        'MAIL_PORT': '587',
        'MAIL_USE_TLS': 'true',
        'MAIL_USERNAME': 'test@example.com',
        'MAIL_PASSWORD': 'test-password',
        'MAIL_DEFAULT_SENDER': 'Boat Service <test@example.com>',
        'GOOGLE_SERVICE_ACCOUNT': '/test/path/service-account.json',
        'GOOGLE_SHEET_ID': 'test_sheet_id',
        'ADMIN_USERNAME': 'admin',
        'ADMIN_PASSWORD': 'admin123',
        'BASE_URL': 'http://127.0.0.1:5000'
    }
    
    # Set each environment variable
    for key, value in test_config.items():
        os.environ[key] = value
        print(f"✅ Set {key} = {value}")
    
    print("\n🔧 Test Environment Configuration Complete!")
    print("\n📋 Test Configuration Summary:")
    print(f"   • Flask Environment: {os.environ.get('FLASK_ENV')}")
    print(f"   • Razorpay Mode: {'Test Mode' if 'test' in os.environ.get('RAZORPAY_KEY_ID', '') else 'Live Mode'}")
    print(f"   • Admin Login: {os.environ.get('ADMIN_USERNAME')} / {os.environ.get('ADMIN_PASSWORD')}")
    print(f"   • Base URL: {os.environ.get('BASE_URL')}")
    
    print("\n🧪 Test Mode Features:")
    print("   • Mock Razorpay client (no real payments)")
    print("   • Test database in instance folder")
    print("   • Mock email service")
    print("   • Mock Google Sheets integration")
    
    print("\n🚀 You can now run: python app.py")
    print("   The app will automatically detect test mode and use mock services.")
    
    return True

def create_test_files():
    """Create necessary test files and directories"""
    
    print("\n📁 Creating test files and directories...")
    
    # Create test directories
    test_dirs = [
        'instance',
        'instance/tickets',
        'uploads',
        'uploads/id_proofs',
        'data'
    ]
    
    for dir_path in test_dirs:
        os.makedirs(dir_path, exist_ok=True)
        print(f"   ✅ Created directory: {dir_path}")
    
    # Create test slots.json if it doesn't exist
    slots_file = 'data/slots.json'
    if not os.path.exists(slots_file):
        test_slots = {
            "2025-09-01": ["09:00", "11:00", "14:00", "16:00"],
            "2025-09-02": ["09:00", "11:00", "14:00"],
            "2025-09-03": ["09:00", "16:00"]
        }
        
        import json
        with open(slots_file, 'w') as f:
            json.dump(test_slots, f, indent=2)
        print(f"   ✅ Created test slots file: {slots_file}")
    
    print("   ✅ All test files created successfully!")

def run_tests():
    """Run basic tests to verify setup"""
    
    print("\n🧪 Running basic tests...")
    
    # Test environment variables
    required_vars = ['FLASK_ENV', 'SECRET_KEY', 'RAZORPAY_KEY_ID', 'ADMIN_USERNAME']
    missing_vars = []
    
    for var in required_vars:
        if not os.environ.get(var):
            missing_vars.append(var)
    
    if missing_vars:
        print(f"   ❌ Missing environment variables: {', '.join(missing_vars)}")
        return False
    else:
        print("   ✅ All required environment variables are set")
    
    # Test file structure
    required_files = ['app.py', 'config.py', 'requirements.txt']
    missing_files = []
    
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        print(f"   ❌ Missing required files: {', '.join(missing_files)}")
        return False
    else:
        print("   ✅ All required files are present")
    
    print("   ✅ Basic tests passed!")
    return True

if __name__ == "__main__":
    try:
        print("🚤 Boat Service Test Environment Setup")
        print("=" * 50)
        
        # Setup environment
        setup_test_environment()
        
        # Create test files
        create_test_files()
        
        # Run tests
        if run_tests():
            print("\n🎉 Test environment setup completed successfully!")
            print("\n📝 Next steps:")
            print("   1. Run: python app.py")
            print("   2. Open: http://127.0.0.1:5000")
            print("   3. Test the booking flow")
            print("   4. Use admin/admin123 to access admin panel")
        else:
            print("\n❌ Test environment setup failed!")
            sys.exit(1)
            
    except Exception as e:
        print(f"\n❌ Error during setup: {e}")
        sys.exit(1)

