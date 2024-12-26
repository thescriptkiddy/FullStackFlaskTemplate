import logging

from flask_cors import CORS
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_security import Security, SQLAlchemySessionUserDatastore
from flask_bootstrap import Bootstrap5
from flask_mailman import Mail
from backend.app.database import db_session
from backend.models.user import User
from backend.models.role import Role
from backend.utils.helper import load_user
from backend.app.auth.forms import ExtendedRegisterForm


migrate = Migrate()
security = Security()
bootstrap = Bootstrap5()
mail = Mail()
login_manager = LoginManager()
cors = CORS()
user_datastore = None


def setup_logger(app):
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    # Create a file handler
    file_handler = logging.FileHandler('app.log')
    file_handler.setLevel(logging.DEBUG)

    # Create a console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)

    # Create a formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    # Add the handlers to the logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    app.logger = logger


def init_user_loader(load_user_func):
    login_manager.user_loader(load_user_func)


def init_extensions(app):
    """Handles all flask extensions. Used my the Application Factory Pattern"""
    global user_datastore
    user_datastore = SQLAlchemySessionUserDatastore(db_session, User, Role)
    cors.init_app(app, resources={r"/*": {"origins": app.config.get('CORS_ORIGINS', "*")}},
                  allow_headers=app.config.get('CORS_ALLOW_HEADERS', "*"),
                  methods=app.config.get('CORS_METHODS', "*"),
                  supports_credentials=app.config.get('CORS_SUPPORTS_CREDENTIALS', True))

    migrate.init_app(app, db_session)
    security.init_app(app, user_datastore,
                      register_form=ExtendedRegisterForm)
    bootstrap.init_app(app)
    mail.init_app(app)
    login_manager.init_app(app)

    setup_logger(app)