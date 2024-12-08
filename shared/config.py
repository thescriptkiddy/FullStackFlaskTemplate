import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    """Default Config Settings with env variables"""
    DEBUG = os.environ.get('DEBUG', 'False') == 'True'
    SECRET_KEY = os.environ.get('FLASK_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DB_URI')
    DEFAULT_ROUTE = 'home.index'
    TEMPLATE_FOLDER = '../frontend/templates'
    STATIC_FOLDER = '../frontend/static'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'csv'}
    # # Flask Security Configuration
    SECURITY_PASSWORD_SALT = os.environ.get("SECURITY_PASSWORD_SALT")
    SECURITY_EMAIL_VALIDATOR_ARGS = {"check_deliverability": False}
    SECURITY_REGISTERABLE = True
    SECURITY_PASSWORD_HASH = 'argon2'

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


class ProductionConfig(Config):
    DEBUG = False


class TestingConfig(Config):
    TESTING = True


