import pytest
import subprocess
import time
import asyncio
from playwright.sync_api import Playwright, sync_playwright, Page, expect
from sqlalchemy import event
from sqlalchemy.orm import Session
from flask_security.utils import hash_password
from backend import create_app
from shared.config import TestingConfig
from backend.models.user import User
from backend.app.database import db_session


async def close_browser(browser):
    await browser.close()


@pytest.fixture(scope="session", autouse=True)
def setup_flask_server():
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
    print("Closing page...")
    page.close()
    print("Closing context...")
    context.close()
    print("Closing browser...")
    browser.close()
    print("Cleanup complete.")


@pytest.fixture(scope="function")
def auth_context(playwright: Playwright):
    """Fixture to log in a user"""
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()

    # Login
    page.goto("http://127.0.0.1:5000/login")
    page.fill("#floatingEmail", "testuser@testuser.com")
    page.fill("#floatingPassword", "12345678")
    page.click("#submit")

    context.storage_state(path="auth_state.json")

    context.close()
    page.close()
    browser.close()


@pytest.fixture(scope="function")
def authenticated_page(page: Page, auth_context):
    """Fixture to provide a page with auth-context, to access protected pages"""
    new_context = page.context.browser.new_context(storage_state="auth_state.json")
    new_page = new_context.new_page()

    yield new_page

    new_context.close()
