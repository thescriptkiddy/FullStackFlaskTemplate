import pytest
from playwright.sync_api import Page, expect
from tests.conftest import flask_server


def test_registration_within_content_area(page: Page, flask_server, test_constants, generate_test_email) -> None:
    """
    GIVEN A visitor wants to create an account
    WHEN the visitor provides a valid email address and password
    THEN the visitor must be able to create an account and without confirming the email address and
    is automatically authenticated and redirected to the homepage
    :param page:
    :param setup_flask_server:
    :return:
    """

    page.goto(test_constants["BASE_URL"])
    page.get_by_role("button", name="Register").click()
    page.get_by_label("Email Address").fill(generate_test_email)
    page.get_by_label("Password", exact=True).fill(test_constants["TEST_PASSWORD"])
    page.get_by_label("Retype Password").fill(test_constants["TEST_PASSWORD"])
    page.get_by_label("First Name").fill("Test")
    page.get_by_label("Last Name").fill("User")
    page.get_by_role("button", name="Submit").click()
    page.wait_for_load_state("networkidle")
    expect(
        page.get_by_text("Welcome")).to_be_visible()


def test_successful_registration_with_email_only(page: Page, flask_server, test_constants, generate_test_email) -> None:
    # Navigate to registration page
    page.goto(test_constants["REGISTRATION_URL"])
    # Fill in registration form
    page.get_by_label("Email Address").fill(generate_test_email)
    page.get_by_label("Password", exact=True).fill(test_constants["TEST_PASSWORD"])
    page.get_by_label("Retype Password").fill(test_constants["TEST_PASSWORD"])

    # Submit registration form
    page.get_by_role("button", name="Submit").click()
    page.wait_for_load_state("networkidle")
    expect(
        page.get_by_text("Welcome")).to_be_visible()

    # Verify that user exists in the database
