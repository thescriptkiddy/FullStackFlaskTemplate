import click
from flask import Flask
from flask.cli import with_appcontext
from flask_bootstrap import Bootstrap5
from shared import config
from shared.extensions import db


def create_app(config_class=config.Config):
    """Application-Factory-Pattern"""
    app = Flask(__name__)
    app.config.from_object(config_class)

    @click.command(name='init-db')
    @with_appcontext
    def init_db_command():
        with app.app_context():
            db.create_all()
            click.echo('Initialized the database.')

    # Register the CLI command

    # Initialize Flask extensions here

    # Register blueprints here

    @app.route('/')
    def test_page():
        return '<h1>Testing the Flask Application Factory Pattern</h1>'

    return app
