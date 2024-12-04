import click
from flask import Flask
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask.cli import with_appcontext
from flask_bootstrap import Bootstrap5
from shared import config
from shared.extensions import db, migrate
from backend.models.user import User
from backend.models.item import Item


def create_app(config_class=config.Config):
    """Application-Factory-Pattern"""
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize Flask extensions here
    db.init_app(app)
    migrate.init_app(app)
    Bootstrap5(app)

    admin = Admin(app, name="Minimal Flask-Fullstack-Template")
    admin.add_view(ModelView(User, db.session))
    admin.add_view(ModelView(Item, db.session))

    @app.cli.command("init-db")
    def init_db_command():
        """Initialize the database."""
        db.create_all()
        click.echo('Initialized the database.')


    # Register blueprints here

    @app.route('/')
    def test_page():
        return '<h1>Testing the Flask Application Factory Pattern</h1>'

    return app
