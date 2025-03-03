import os
import subprocess
import time
import urllib.parse
import uuid
import secrets
import pytest
import socket
from dotenv import load_dotenv
from flask_security import hash_password, login_user, SQLAlchemySessionUserDatastore
from playwright.sync_api import Playwright, Page, Browser, BrowserContext
from sqlalchemy import select

from backend import create_app
from backend.models.role import Role
from backend.models.user import User
from shared.database import db_session, engine, Base
from shared.config import TestingConfig
# from shared.extensions import user_datastore

from tests.unit.menu.mock_data import get_mock_menu_data
import threading
from werkzeug.serving import make_server
from shared.database import init_db, engine

load_dotenv()

# Constants
BASE_URL = os.getenv("BASE_URL")
REGISTRATION_URL = "/register"
LOGIN_URL = "/login"
ITEMS_PAGE = "/items/"
USER_PAGE = "/users"
TEST_PASSWORD = "12345678"
TEST_PASSWORD_6 = "kHud45"
DELETE_BUTTON_SELECTOR = 'button[name="delete-item"] i.bi.bi-trash'
EDIT_BUTTON_SELECTOR = ""
SUCCESS_MESSAGE_SELECTOR = '.alert-success'
ERROR_MESSAGE_SELECTOR = '.alert-error'

test_email = f"registration-test-{uuid.uuid4()}@example.com"

user_datastore = SQLAlchemySessionUserDatastore(db_session, User, Role)


def get_free_port():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('', 0))
        return s.getsockname()[1]


@pytest.fixture(scope="function")
def dynamic_base_url():
    port = get_free_port()
    return f'http://127.0.0.1:{port}'


@pytest.fixture()
def generate_test_email(request):
    """Generates unique email addresses for testing"""
    prefix = getattr(request.node, "prefix", "test")
    return f"{prefix}-{uuid.uuid4()}@example.com"


@pytest.fixture(scope="function")
def test_constants(dynamic_base_url):
    """Testing constants"""

    return {
        "BASE_URL": dynamic_base_url,
        "REGISTRATION_URL": f"{dynamic_base_url}{REGISTRATION_URL}",
        "LOGIN_URL": f"{dynamic_base_url}{LOGIN_URL}",
        "ITEMS_PAGE": f"{dynamic_base_url}{ITEMS_PAGE}",
        "USER_PAGE": f"{dynamic_base_url}{USER_PAGE}",
        "TEST_PASSWORD": TEST_PASSWORD,
        "TEST_PASSWORD_6": TEST_PASSWORD_6,
        "DELETE_BUTTON_SELECTOR": DELETE_BUTTON_SELECTOR,
        "EDIT_BUTTON_SELECTOR": EDIT_BUTTON_SELECTOR,
        "SUCCESS_MESSAGE_SELECTOR": SUCCESS_MESSAGE_SELECTOR,
        "ERROR_MESSAGE_SELECTOR": ERROR_MESSAGE_SELECTOR,
    }


@pytest.fixture(scope="session")
def user_exists_in_db():
    def _user_exists(email):
        return db_session.query(User).filter_by(email=email).first() is not None

    return _user_exists


@pytest.fixture(scope="session")
def remove_user_from_db():
    def _remove_user(email):
        user = db_session.query(User).filter_by(email=email).first()
        if user:
            db_session.delete(user)
            db_session.commit()

    return _remove_user


@pytest.fixture(scope='session')
def mock_context_processors():
    mock_menu_data = get_mock_menu_data()

    def inject_mock_menu_items():
        return dict(menu_items=mock_menu_data)

    def inject_mock_configured_menu_links():
        links = mock_menu_data[0]['links']
        print(f"Injected configured_menu_links: {links}")
        return dict(configured_menu_links=links)

    return [inject_mock_menu_items, inject_mock_configured_menu_links]


@pytest.fixture(scope='session')
def app(mock_context_processors):
    """Testing factory pattern with mocked context processors"""
    from backend import create_app
    from shared.config import TestingConfig, Config

    app = create_app(config_class=TestingConfig, test_context_processors=mock_context_processors)
    with app.app_context():
        yield app


@pytest.fixture(scope='function')
def get_db(app):
    with app.app_context():
        Base.metadata.create_all(bind=engine)
        yield db_session
        db_session.remove()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope='function')
def init_user_datastore(app):
    # Initialize user_datastore
    from shared.extensions import init_extensions
    init_extensions(app)
    yield user_datastore


@pytest.fixture(scope="function")
def test_user(get_db):
    """Fixture loads a test user for unit tests"""

    return get_db.scalars(select(User).filter_by(email='testuser@testuser.com')).first()


@pytest.fixture(scope='function')
def new_user(get_db, init_user_datastore):
    user = user_datastore.create_user(email='test@example.com', password='password')
    get_db.session.commit()
    return user


@pytest.fixture(scope="function", autouse=True)
def flask_server(app, dynamic_base_url):
    """App Factory Pattern for Testing"""

    with app.app_context():
        init_db()

        existing_user = db_session.query(User).filter_by(email="testuser@testuser.com").first()

        if not existing_user:
            test_user = User(
                email="testuser@testuser.com",
                firstname="Test",
                lastname="User",
                active=True
            )
            test_user.password = hash_password("12345678")
            db_session.add(test_user)
            db_session.commit()
            print(f"User added: {test_user.email}")

    # Start server in a separate thread
    parsed_url = urllib.parse.urlparse(dynamic_base_url)
    server = make_server(parsed_url.hostname, parsed_url.port, app)
    thread = threading.Thread(target=server.serve_forever)
    thread.start()

    # Temporarily override the BASE_URL environment variable
    original_base_url = os.environ.get('BASE_URL')
    os.environ['BASE_URL'] = dynamic_base_url

    yield

    # Restore original BASE_URL after testing
    if original_base_url:
        os.environ['BASE_URL'] = original_base_url
    else:
        del os.environ['BASE_URL']

    # Shutdown the server
    server.shutdown()
    thread.join()


@pytest.fixture(scope="function")
def page(playwright: Playwright):
    """Page fixture for non-authentication"""
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    yield page
    page.close()
    context.close()
    browser.close()


@pytest.fixture(scope="function")
def auth_context(flask_server, page, test_constants):
    """Fixture to log in a user"""
    # Login
    page.goto(test_constants["LOGIN_URL"])
    page.fill("#floatingEmail", "testuser@testuser.com")
    page.fill("#floatingPassword", "12345678")
    page.click("#submit")
    page.context.storage_state(path="auth_state.json")
    yield page.context


@pytest.fixture(scope="function")
def authenticated_page(playwright: Playwright, auth_context: BrowserContext) -> Page:
    browser: Browser = playwright.chromium.launch()
    context: BrowserContext = browser.new_context(storage_state="auth_state.json")
    page: Page = context.new_page()

    yield page

    page.close()
    context.close()
    browser.close()


@pytest.fixture(scope='function')
def client(app):
    yield app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()


@pytest.fixture
def authenticated_client(app, get_db, client):
    with app.app_context():
        user = get_db.query(User).filter_by(email="testuser@testuser.com").first()
        if not user:
            user = User(
                email="testuser@testuser.com",
                password="12345789",
                active=True
            )
            get_db.add(user)
            get_db.commit()

    client = app.test_client()
    with client.session_transaction() as session:
        session['user_id'] = user.id
        session['user_firstname'] = user.firstname
        session['user_lastname'] = user.lastname
        session['_fresh'] = True

    return client
