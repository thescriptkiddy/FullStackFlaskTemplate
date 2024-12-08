from backend.models.role import Role
from backend.models.user import User
from backend.models.item import Item
import click
import os
from flask import Flask, render_template, redirect, url_for
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask.cli import with_appcontext
from flask_bootstrap import Bootstrap5
from flask_security import SQLAlchemySessionUserDatastore, Security
from shared import config
from backend.app.items import bp
from backend.app.database import db_session, Base
from flask_migrate import Migrate
from shared.extensions import LoginManager
from flask_mailman import Mail
from dotenv import load_dotenv

migrate = Migrate()
login_manager = LoginManager()


def create_app(config_class=config.Config):
    """Application-Factory-Pattern"""
    app = Flask(__name__, template_folder=config_class.TEMPLATE_FOLDER, static_folder=config_class.STATIC_FOLDER)
    app.config.from_object(config_class)

    app.teardown_appcontext(lambda exc: db_session.close())

    # Flask-Security
    user_datastore = SQLAlchemySessionUserDatastore(db_session, User, Role)
    security = Security(app, user_datastore)

    # Initialize Flask extensions
    migrate.init_app(app, db_session)
    login_manager.init_app(app)
    Bootstrap5(app)
    mail = Mail(app)

    # Register blueprints here
    from backend.app.items import bp as items_bp
    app.register_blueprint(items_bp, url_prefix="/items")

    from backend.app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix="/auth")

    from backend.app.home import bp as home_bp
    app.register_blueprint(home_bp)

    admin = Admin(app, name="Minimal Flask-Fullstack-Template")
    admin.add_view(ModelView(User, db_session))
    admin.add_view(ModelView(Item, db_session))

    @app.cli.command("init-db")
    def init_db_command():
        """Initialize the database."""
        Base.metadata.create_all(bind=db_session.bind)  # Create tables based on models.
        click.echo('Initialized the database.')

    @app.route('/')
    def default_route():
        return redirect(url_for(app.config['DEFAULT_ROUTE']))

    @app.route('/')
    def test_page():
        return render_template("factory-pattern.html")

    return app


@login_manager.user_loader
def load_user(user_id):
    return db_session.get(User, user_id)
