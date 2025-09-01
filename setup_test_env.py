#!/usr/bin/env python3
"""
Setup script for Boat Service test environment
This script helps you create a .env file with test configuration
"""

import os

def create_env_file():
    """Create a .env file with test configuration"""
    
    env_content = """# Test Environment Configuration for Boat Service
FLASK_ENV=development
SECRET_KEY=dev-secret-key-change-in-production

# Razorpay Test API Keys
RAZORPAY_KEY_ID=rzp_test_1DP5mmOlF5G5ag
RAZORPAY_KEY_SECRET=thisisasamplesecretkey

# Email (example: Gmail SMTP - use app password)
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=true
MAIL_USERNAME=owner@example.com
MAIL_PASSWORD=your-app-password
MAIL_DEFAULT_SENDER="Boat Service <owner@example.com>"

# Google Service Account JSON path (mounted securely)
GOOGLE_SERVICE_ACCOUNT=/absolute/path/to/service-account.json
GOOGLE_SHEET_ID=your_google_sheet_id

# Admin auth
ADMIN_USERNAME=admin
ADMIN_PASSWORD=admin123

# Base URL
BASE_URL=http://127.0.0.1:5000
"""
    
    try:
        with open('.env', 'w') as f:
            f.write(env_content)
        print("✅ .env file created successfully!")
        print("📝 You can now edit the .env file with your actual values")
        print("🔑 For Razorpay test mode, the test keys are already set")
        print("🧪 Test card numbers:")
        print("   Success: 4111 1111 1111 1111")
        print("   Failure: 4000 0000 0000 0002")
        print("   CVV: Any 3 digits")
        print("   Expiry: Any future date")
    except Exception as e:
        print(f"❌ Error creating .env file: {e}")

def set_env_variables():
    """Set environment variables directly (alternative method)"""
    print("🔧 Setting environment variables...")
    
    # Set Razorpay test keys
    os.environ['RAZORPAY_KEY_ID'] = 'rzp_test_1DP5mmOlF5G5ag'
    os.environ['RAZORPAY_KEY_SECRET'] = 'thisisasamplesecretkey'
    os.environ['FLASK_ENV'] = 'development'
    os.environ['SECRET_KEY'] = 'dev-secret-key-change-in-production'
    os.environ['ADMIN_USERNAME'] = 'admin'
    os.environ['ADMIN_PASSWORD'] = 'admin123'
    os.environ['BASE_URL'] = 'http://127.0.0.1:5000'
    
    print("✅ Environment variables set successfully!")
    print("🚀 You can now run: python app.py")

if __name__ == "__main__":
    print("🚤 Boat Service Test Environment Setup")
    print("=" * 40)
    
    choice = input("Choose setup method:\n1. Create .env file\n2. Set environment variables directly\nEnter choice (1 or 2): ").strip()
    
    if choice == "1":
        create_env_file()
    elif choice == "2":
        set_env_variables()
    else:
        print("Invalid choice. Please run the script again.")
