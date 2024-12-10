import pytest
from backend import create_app
from backend.app.database import db_session, Session, engine, Base
from shared.config import Config


@pytest.fixture(scope='session')
def app():
    app = create_app()
    app.config.from_object(Config)  # Load config from your Config class
    app.config.update({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:'  # Override for testing
    })
    return app


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()


@pytest.fixture(scope='function')
def db(app):
    with app.app_context():
        Base.metadata.create_all(bind=engine)
        yield db_session
        db_session.remove()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture()
def init_database(db):

    yield db



@pytest.fixture()
def chrome_options(chrome_options):
    chrome_options.binary_location = "/usr/local/bin/chromedriver"
    chrome_options.add_extension('/path/to/extension.crx')
    chrome_options.add_argument('--kiosk')
    return chrome_options
