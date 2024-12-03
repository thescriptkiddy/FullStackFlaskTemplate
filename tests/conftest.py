import pytest
from shared.extensions import db
from backend import create_app


@pytest.fixture()
def app():
    app = create_app()
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()


@pytest.fixture()
def init_database(app):
    with app.app_context():
        db.create_all()
        yield db
        db.drop_all()


@pytest.fixture()
def chrome_options(chrome_options):
    chrome_options.binary_location = "/usr/local/bin/chromedriver"
    chrome_options.add_extension('/path/to/extension.crx')
    chrome_options.add_argument('--kiosk')
    return chrome_options
