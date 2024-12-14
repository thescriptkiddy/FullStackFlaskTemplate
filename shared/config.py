import os
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
    SECURITY_CHANGE_URL = '/change'
    SECURITY_POST_CHANGE_VIEW = '/profile'
    SECURITY_CHANGE_EMAIL = True

    CORS_ORIGINS = ["*"]
    CORS_ALLOW_HEADERS = ["*"]
    CORS_METHODS = ["*"]
    CORS_SUPPORTS_CREDENTIALS = True

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
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DB_URI')


class ProductionConfig(Config):
    DEBUG = False


class TestingConfig(Config):
    TESTING = True
