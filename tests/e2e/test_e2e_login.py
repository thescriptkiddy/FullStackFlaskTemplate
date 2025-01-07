from playwright.sync_api import Page, expect
from tests.conftest import flask_server


def test_successful_login_via_button(flask_server, page: Page, test_constants) -> None:
    """
    GIVEN An non-authenticated user
    WHEN wants to log in with existing email and password combination
    THEN the user must be authenticated and redirected to the home page
    """
    page.goto(test_constants["BASE_URL"])
    page.get_by_role("button", name="Login").click()
    page.get_by_placeholder("name@example.com").click()
    page.get_by_placeholder("name@example.com").fill("testuser@testuser.com")
    page.get_by_placeholder("Password").fill(test_constants["TEST_PASSWORD"])
    page.get_by_role("button", name="Login").click()
    page.wait_for_load_state("networkidle")
    page.get_by_text("Quickly design and customize").click()


def test_successful_login_via_sidebar(flask_server, page: Page, test_constants, user_exists_in_db) -> None:
    """
    GIVEN An non-authenticated user wants to log in via the Login-Link in the sidebar
    WHEN the user provides valid credentials
    THEN the user must be authenticated and redirected to the home page
    """
    page.goto(test_constants["BASE_URL"])
    page.get_by_test_id("sidebar-login").click()
    page.wait_for_load_state("networkidle")
    page.get_by_placeholder("name@example.com").fill("testuser@testuser.com")
    page.get_by_placeholder("Password").fill(test_constants["TEST_PASSWORD"])
    page.get_by_role("button", name="Login").click()
    page.get_by_role("heading", name="Welcome Test User").click()
    assert user_exists_in_db("testuser@testuser.com")


def test_failed_login_with_email(flask_server, page: Page, test_constants, generate_test_email):
    """
    GIVEN An non-authenticated user wants to log in via the Login-Link in the sidebar
    WHEN the user provides an email address which is not associated with an account
    THEN the user receives an error message
    """
    page.goto(test_constants["BASE_URL"])
    page.get_by_test_id("sidebar-login").click()
    page.wait_for_load_state("networkidle")
    page.get_by_placeholder("name@example.com").fill(generate_test_email)
    page.get_by_placeholder("Password").fill(test_constants["TEST_PASSWORD"])
    page.get_by_role("button", name="Login").click()
    error_message = page.locator("text=Specified user does not exist")
    expect(error_message).to_be_visible()


def test_failed_login_with_wrong_password(flask_server, page: Page, test_constants):
    """
    GIVEN An non-authenticated user wants to log in via the Login-Link in the sidebar
    WHEN the user provides a wrong password
    THEN the user receives an error message
    """
    page.goto(test_constants["BASE_URL"])
    page.get_by_test_id("sidebar-login").click()
    page.wait_for_load_state("networkidle")
    page.get_by_placeholder("name@example.com").fill("testuser@testuser.com")
    page.get_by_placeholder("Password").fill(test_constants["TEST_PASSWORD_6"])
    page.get_by_role("button", name="Login").click()
    error_message = page.locator("text=Invalid password")
    expect(error_message).to_be_visible()

# TODO Add test remember me functionality
