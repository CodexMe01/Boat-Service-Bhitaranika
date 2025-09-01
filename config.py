import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-key")

    RAZORPAY_KEY_ID = os.getenv("RAZORPAY_KEY_ID")
    RAZORPAY_KEY_SECRET = os.getenv("RAZORPAY_KEY_SECRET")

    MAIL_SERVER = os.getenv("MAIL_SERVER", "smtp.gmail.com")
    MAIL_PORT = int(os.getenv("MAIL_PORT", 587))
    MAIL_USE_TLS = os.getenv("MAIL_USE_TLS", "true").lower() == "true"
    MAIL_USERNAME = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
    MAIL_DEFAULT_SENDER = os.getenv("MAIL_DEFAULT_SENDER")

    GOOGLE_SERVICE_ACCOUNT = os.getenv("GOOGLE_SERVICE_ACCOUNT")
    GOOGLE_SHEET_ID = os.getenv("GOOGLE_SHEET_ID")

    ADMIN_USERNAME = os.getenv("ADMIN_USERNAME", "owner")
    ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "change-this")

    BASE_URL = os.getenv("BASE_URL", "http://127.0.0.1:5000")

    # Flask paths
    INSTANCE_PATH = os.path.join(os.getcwd(), 'instance')
    UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads', 'id_proofs')
    MAX_CONTENT_LENGTH = 8 * 1024 * 1024  # 8MB

class Prod(Config):
    pass

class Dev(Config):
    pass
