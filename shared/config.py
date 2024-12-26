import os
from datetime import timedelta

from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv()


class Config:
    """Default Config Settings with env variables"""
    DEBUG = os.environ.get('DEBUG', 'False') == 'True'
    SECRET_KEY = os.environ.get('FLASK_KEY')
    # Database Configurations
    SQLALCHEMY_DATABASE_URI = os.environ.get('DB_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Flask Security Configurations
    SECURITY_REGISTER_URL = '/register'
    SECURITY_PASSWORD_SALT = os.environ.get("SECURITY_PASSWORD_SALT")
    SECURITY_EMAIL_VALIDATOR_ARGS = {"check_deliverability": False}
    SECURITY_REGISTERABLE = True
    SECURITY_PASSWORD_HASH = 'argon2'
    SECURITY_RECOVERABLE = True
    SECURITY_CHANGEABLE = True
    SECURITY_DEFAULT_REMEMBER_ME = True
    SECURITY_REMEMBER_ME = True
    SECURITY_REMEMBER_ME_DURATION = timedelta(days=30)
    SECURITY_CHANGE_URL = '/change'
    SECURITY_POST_CHANGE_VIEW = '/profile'
    SECURITY_POST_LOGIN_VIEW = 'home.index'
    SECURITY_CHANGE_EMAIL = True
    # SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    PERMANENT_SESSION_LIFETIME = timedelta(days=30)
    SECURITY_TOKEN_AUTHENTICATION_HEADER = 'Authentication-Token'
    SECURITY_TOKEN_AUTHENTICATION_KEY = 'auth_token'
    SECURITY_CSRF_PROTECT = True
    SECURITY_USER_IDENTITY_ATTRIBUTES_MAP = {
        'email': 'email',
        'fs_uniquifier': 'fs_uniquifier'
    }

    # CORS_ORIGINS = ["*"]
    # CORS_ALLOW_HEADERS = ["*"]
    # CORS_METHODS = ["*"]
    # CORS_SUPPORTS_CREDENTIALS = True
    #
    DEFAULT_ROUTE = 'home.index'
    TEMPLATE_FOLDER = '../frontend/templates'
    STATIC_FOLDER = '../frontend/static'
    ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'csv'}

    # AUTHENTICATION # TODO Need to check whether this fits for Flask Security
    RESET_PASS_TOKEN_MAX_AGE = os.environ.get("RESET_PASS_TOKEN_MAX_AGE")

    # # Mailman Configuration
    MAIL_SERVER = "smtp.gmail.com"
    MAIL_PORT = 587
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_USE_TLS = True


class DevelopmentConfig(Config):
    """Config for Development"""
    DEBUG = os.environ.get('DEBUG', 'False') == 'True'
    SECRET_KEY = os.environ.get('FLASK_KEY')
    # Database Configurations
    # SQLALCHEMY_DATABASE_URI = os.environ.get('DB_URI')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Flask Security Configurations
    SECURITY_REGISTER_URL = '/register'
    SECURITY_PASSWORD_SALT = os.environ.get("SECURITY_PASSWORD_SALT")
    SECURITY_EMAIL_VALIDATOR_ARGS = {"check_deliverability": False}
    SECURITY_REGISTERABLE = True
    SECURITY_PASSWORD_HASH = 'argon2'
    SECURITY_RECOVERABLE = True
    SECURITY_CHANGEABLE = True
    SECURITY_DEFAULT_REMEMBER_ME = True
    SECURITY_REMEMBER_ME = True
    SECURITY_REMEMBER_ME_DURATION = timedelta(days=30)
    SECURITY_CHANGE_URL = '/change'
    SECURITY_POST_CHANGE_VIEW = '/profile'
    SECURITY_POST_LOGIN_VIEW = 'home.index'
    SECURITY_CHANGE_EMAIL = True
    # SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    PERMANENT_SESSION_LIFETIME = timedelta(days=30)
    SECURITY_TOKEN_AUTHENTICATION_HEADER = 'Authentication-Token'
    SECURITY_TOKEN_AUTHENTICATION_KEY = 'auth_token'
    SECURITY_CSRF_PROTECT = True
    SECURITY_USER_IDENTITY_ATTRIBUTES_MAP = {
        'email': 'email',
        'fs_uniquifier': 'fs_uniquifier'
    }

    DEFAULT_ROUTE = 'home.index'
    TEMPLATE_FOLDER = '../frontend/templates'
    STATIC_FOLDER = '../frontend/static'
    ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'csv'}

    # AUTHENTICATION # TODO Need to check whether this fits for Flask Security
    RESET_PASS_TOKEN_MAX_AGE = os.environ.get("RESET_PASS_TOKEN_MAX_AGE")

    # # Mailman Configuration
    MAIL_SERVER = "smtp.gmail.com"
    MAIL_PORT = 587
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_USE_TLS = True


class ProductionConfig(Config):
    DEBUG = False


class TestingConfig(Config):
    """Config for Testing"""
    TESTING = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    # SECRET_KEY = 'test-secret-key'
    # SECURITY_PASSWORD_SALT = 'test-salt'

    # Disable email sending for tests
    SECURITY_EMAIL_SENDER = 'noreply@example.com'
    MAIL_SUPPRESS_SEND = True

    # Simplify password hashing for faster tests
    # SECURITY_PASSWORD_HASH = 'plaintext'

    # Disable CSRF for testing
    WTF_CSRF_ENABLED = False
    SECURITY_CSRF_PROTECT_MECHANISMS = []

    # Enable registering and other security features for testing
    SECURITY_REGISTERABLE = True
    SECURITY_RECOVERABLE = True
    SECURITY_CHANGEABLE = True
    SECURITY_CONFIRMABLE = False
