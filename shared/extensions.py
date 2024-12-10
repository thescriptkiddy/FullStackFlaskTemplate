from flask_login import LoginManager
from flask_migrate import Migrate
from flask_security import Security, SQLAlchemySessionUserDatastore
from flask_bootstrap import Bootstrap5
from flask_mailman import Mail
from backend.app.database import db_session
from backend.models.user import User
from backend.models.role import Role
from backend.app.auth.service import load_user

migrate = Migrate()
security = Security()
bootstrap = Bootstrap5()
mail = Mail()
login_manager = LoginManager()

user_datastore = None


def init_extensions(app):
    """Handles all flask extensions. Used my the Application Factory Pattern"""
    global user_datastore
    user_datastore = SQLAlchemySessionUserDatastore(db_session, User, Role)

    migrate.init_app(app, db_session)
    security.init_app(app, user_datastore)
    bootstrap.init_app(app)
    mail.init_app(app)
    login_manager.init_app(app)
    login_manager.user_loader(load_user)
