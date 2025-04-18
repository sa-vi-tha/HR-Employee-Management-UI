
import os
from cryptography.fernet import Fernet

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or os.urandom(24)
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///hr_management.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    EXTERNAL_HRMS_API_KEY = os.environ.get('EXTERNAL_HRMS_API_KEY', '')
    ENCRYPTION_KEY = Fernet.generate_key()
    