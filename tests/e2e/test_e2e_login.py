import re
from flask_security import current_user
from tests.e2e.conftest import setup_flask_server, page
from playwright.sync_api import Page, expect, Playwright


def test_2e2_login(setup_flask_server, page: Page) -> None:
    """
    GIVEN An non-authenticated user
    WHEN wants to log in with existing email and password combination
    THEN the user must be authenticated and redirected to the home page
    :param page:
    :param setup_flask_server:
    :return:
    """
    page.goto("http://127.0.0.1:5000/home/")
    page.get_by_role("button", name="Login").click(timeout=3000)
    page.get_by_placeholder("name@example.com").click()
    page.get_by_placeholder("name@example.com").fill("testuser@testuser.com")
    page.get_by_placeholder("name@example.com").press("Tab")
    page.get_by_placeholder("Password").fill("12345678")
    page.get_by_role("button", name="Login").click()
    page.wait_for_load_state("domcontentloaded")
    page.get_by_text("Quickly design and customize").click()
