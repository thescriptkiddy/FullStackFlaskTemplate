import pytest
from backend import create_app
from backend.app.database import db_session, Session, engine, Base


@pytest.fixture()
def app():
    app = create_app()
    with app.app_context():
        Base.metadata.create_all(bind=db_session.bind)
        yield app
    with app.app_context():
        Base.metadata.drop_all(bind=db_session.bind)


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()


@pytest.fixture()
def init_database(app):
    with app.app_context():
        Base.metadata.create_all(bind=db_session.bind)
        yield app
        Base.metadata.drop_all(bind=db_session.bind)


@pytest.fixture()
def chrome_options(chrome_options):
    chrome_options.binary_location = "/usr/local/bin/chromedriver"
    chrome_options.add_extension('/path/to/extension.crx')
    chrome_options.add_argument('--kiosk')
    return chrome_options
