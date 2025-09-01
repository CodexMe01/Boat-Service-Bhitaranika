# Test Configuration for Boat Service
# Copy these values to your .env file or set as environment variables

# Razorpay Test API Keys (for development/testing only)
RAZORPAY_KEY_ID = "rzp_test_1DP5mmOlF5G5ag"
RAZORPAY_KEY_SECRET = "thisisasamplesecretkey"

# Other test configuration
SECRET_KEY = "dev-secret-key-change-in-production"
FLASK_ENV = "development"

# Admin credentials for testing
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"

# Base URL for testing
BASE_URL = "http://127.0.0.1:5000"

# Test card numbers for Razorpay:
# Success: 4111 1111 1111 1111
# Failure: 4000 0000 0000 0002
# CVV: Any 3 digits
# Expiry: Any future date
