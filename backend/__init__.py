import logging

from backend.utils.helper import load_user
# from backend.models.role import Role
from backend.models.user import User
from backend.models.item import Item
from backend.models.menu import Menu
import click
from flask import Flask, render_template, redirect, url_for
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from shared import config
from backend.app.items import bp
from backend.app.users import bp
from backend.app.menu import bp
from shared.database import db_session, Base, init_db
from shared.extensions import init_extensions, login_manager, setup_logger
from backend.utils.helper import register_error_handlers


def create_app(config_class=config.Config, test_context_processors=None):
    """Application-Factory-Pattern"""
    app = Flask(__name__, template_folder=config_class.TEMPLATE_FOLDER, static_folder=config_class.STATIC_FOLDER)
    app.config.from_object(config_class)

    init_extensions(app)

    register_error_handlers(app)

    with app.app_context():
        init_db()

    app.teardown_appcontext(lambda exc: db_session.close())

    from backend.utils.helper import load_user
    login_manager.user_loader(load_user)

    # Register blueprints here
    from backend.app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix="/auth")

    from backend.app.home import bp as home_bp
    app.register_blueprint(home_bp)

    from backend.app.items import bp as items_bp
    app.register_blueprint(items_bp, url_prefix="/items")

    from backend.app.menu import bp as menu_bp
    app.register_blueprint(menu_bp)

    from backend.app.users import bp as user_bp
    app.register_blueprint(user_bp, url_prefix="/users")

    admin = Admin(app, name="Minimal Flask-Fullstack-Template")
    admin.add_view(ModelView(User, db_session))
    admin.add_view(ModelView(Item, db_session))

    from backend.utils.route_helpers import register_links
    with app.app_context():
        register_links(app)

    # Handling context processors

    if test_context_processors:
        for processor in test_context_processors:
            app.context_processor(processor)

    else:
        @app.context_processor
        def inject_menu_items():
            # Fetch menu items from your database
            menu_items = Menu.get_menu_data()
            return dict(menu_items=menu_items)

        @app.context_processor
        def inject_configured_menu_links():
            links = Menu.get_menu_data(menu_id=1)

            return dict(configured_menu_links=links)

    @app.cli.command("init-db")
    def init_db_command():
        """Initialize the database."""
        Base.metadata.create_all(bind=db_session.bind)  # Create tables based on models.
        click.echo('Initialized the database.')

    @app.route('/')
    def default_route():
        return redirect(url_for(app.config['DEFAULT_ROUTE']))

    # @app.route('/')
    # def test_page():
    # return render_template("factory-pattern.html")

    return app
