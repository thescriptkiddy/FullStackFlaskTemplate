import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    """Default Config Settings with env variables"""
    SECRET_KEY = os.environ.get('FLASK_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DB_URI')
    # static_folder = '../frontend/static/'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'csv'}
    DEBUG = True

    # AUTHENTICATION
    RESET_PASS_TOKEN_MAX_AGE = os.environ.get("RESET_PASS_TOKEN_MAX_AGE")
