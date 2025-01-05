from playwright.sync_api import Page
from tests.conftest import flask_server


def test_2e2_login(flask_server, page: Page, test_constants) -> None:
    """
    GIVEN An non-authenticated user
    WHEN wants to log in with existing email and password combination
    THEN the user must be authenticated and redirected to the home page
    """
    page.goto(test_constants["BASE_URL"])
    page.get_by_role("button", name="Login").click()
    page.get_by_placeholder("name@example.com").click()
    page.get_by_placeholder("name@example.com").fill("testuser@testuser.com")
    page.get_by_placeholder("name@example.com").press("Tab")
    page.get_by_placeholder("Password").fill("12345678")
    page.get_by_role("button", name="Login").click()
    page.wait_for_load_state("domcontentloaded")
    page.get_by_text("Quickly design and customize").click()
