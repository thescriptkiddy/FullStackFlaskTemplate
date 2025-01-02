import subprocess
import time

import pytest
from flask_security import hash_password
from playwright.sync_api import Playwright, Page, Browser, BrowserContext

from backend import create_app
from backend.models.user import User
from shared.database import db_session, engine, Base
from shared.config import TestingConfig


@pytest.fixture(scope='session')
def app():
    app = create_app()
    app.config.from_object(TestingConfig)
    return app


@pytest.fixture(scope='function')
def get_db(app):
    with app.app_context():
        Base.metadata.create_all(bind=engine)
        yield db_session
        db_session.remove()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def test_user(get_db):
    """Fixture create a test user for unit tests"""
    test_user = User(email="unittest@testuser.com", firstname="Unit", lastname="Test")
    get_db.add(test_user)
    get_db.commit()
    return test_user


@pytest.fixture(scope="session", autouse=True)
def flask_server():
    """App Factory Pattern for Testing"""
    subprocess.run(["flask", "init-db"], check=True)
    server = subprocess.Popen(["flask", "run"])
    time.sleep(5)

    app = create_app(config_class=TestingConfig)
    # Warning does not affect test execution
    with app.app_context():
        existing_user = db_session.query(User).filter_by(email="testuser@testuser.com").first()
        print(f"Before fixture: User exists = {existing_user is not None}")
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

    yield
    print("Ending setup_flask_server fixture")

    server.terminate()
    server.wait()


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
def auth_context(flask_server, page):
    """Fixture to log in a user"""
    # Login
    page.goto("http://127.0.0.1:5000/login")
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


@pytest.fixture(scope='module')
def client(app):
    yield app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()
