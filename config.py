import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    # Security Configuration: Use environment variable in production, fallback for development only
    SECRET_KEY = os.environ.get('SECRET_KEY', 'adopt-n-shop-dev-secret-key-change-in-production')
    
    # Database Configuration: SQLite by default, override via DATABASE_URL
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///' + os.path.join(BASE_DIR, 'adoptnshop.db'))
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # File Upload Configuration
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'static', 'uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB max upload size
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp', 'gif'}
