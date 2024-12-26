import pytest
from flask_security import login_user

from backend import create_app, User
from backend.app.database import db_session, engine, Base
from shared.config import Config


@pytest.fixture(scope='session')
def app():
    app = create_app()
    app.config.from_object(Config)  # Load config from your Config class
    app.config.update({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
        'WTF_CSRF_ENABLED': False,
        'SECURITY_CSRF_PROTECT': False,
    })

    return app


@pytest.fixture(scope='function')
def db(app):
    with app.app_context():
        Base.metadata.create_all(bind=engine)
        yield db_session
        db_session.remove()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope='module')
def client(app):
    yield app.test_client()


@pytest.fixture()
def init_database(db):
    yield db


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()
