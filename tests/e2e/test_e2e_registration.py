import pytest
from playwright.sync_api import Page, expect
from tests.conftest import flask_server


def test_successful_registration_with_all_attributes(page: Page, flask_server, test_constants,
                                                     generate_test_email, user_exists_in_db,
                                                     remove_user_from_db) -> None:
    """
    GIVEN A visitor wants to create an account
    WHEN the visitor provides a valid email address, password, last- and firstname
    THEN the visitor must be able to create an account and without confirming the email address and
    is automatically authenticated and redirected to the homepage
    """
    test_email = generate_test_email
    page.goto(test_constants["REGISTRATION_URL"])
    page.get_by_label("Email Address").fill(test_email)
    page.get_by_label("Password", exact=True).fill(test_constants["TEST_PASSWORD"])
    page.get_by_label("Retype Password").fill(test_constants["TEST_PASSWORD"])
    page.get_by_label("First Name").fill("Test")
    page.get_by_label("Last Name").fill("User")
    page.get_by_role("button", name="Submit").click()
    page.wait_for_load_state("networkidle")
    expect(
        page.get_by_text("Welcome")).to_be_visible()

    # Verify that user exists in the database
    assert user_exists_in_db(test_email)

    # Remove user
    remove_user_from_db(test_email)


def test_successful_registration_with_email_only(page: Page, flask_server, test_constants, generate_test_email,
                                                 user_exists_in_db, remove_user_from_db) -> None:
    """
    GIVEN A visitor wants to create an account
    WHEN the visitor provides a valid email address, password and nothing else
    THEN the visitor must be able to create an account and without confirming the email address and
    is automatically authenticated and redirected to the homepage
    """
    test_email = generate_test_email
    # Navigate to registration page
    page.goto(test_constants["REGISTRATION_URL"])
    # Fill in registration form
    page.get_by_label("Email Address").fill(test_email)
    page.get_by_label("Password", exact=True).fill(test_constants["TEST_PASSWORD"])
    page.get_by_label("Retype Password").fill(test_constants["TEST_PASSWORD"])

    # Submit registration form
    page.get_by_role("button", name="Submit").click()
    page.wait_for_load_state("networkidle")
    expect(
        page.get_by_text("Welcome")).to_be_visible()

    # Verify that user exists in the database
    assert user_exists_in_db(test_email)

    # Remove user
    remove_user_from_db(test_email)


def test_failed_registration_without_weak_password(page: Page, flask_server, test_constants,
                                                   generate_test_email) -> None:
    """
    GIVEN A user visits the registration page
    WHEN and forgets to repeat the password
    THEN the user should not be able to submit the registration and an error message is visible
    """
    test_email = generate_test_email
    # Navigate to registration page
    page.goto(test_constants["REGISTRATION_URL"])
    # Fill in registration form
    page.get_by_label("Email Address").fill(test_email)
    page.get_by_label("Password", exact=True).fill(test_constants["TEST_PASSWORD_6"])
    page.get_by_label("Retype Password").fill(test_constants["TEST_PASSWORD_6"])
    page.get_by_role("button", name="Submit").click()
    error_message = page.locator("text=Password must be at least 8 characters")
    expect(error_message).to_be_visible()


def test_registration_with_non_matching_passwords(page: Page, flask_server, test_constants, generate_test_email):
    """
    GIVEN A user visits the registration page
    WHEN and does not repeat the same password in the Repeat Password field
    THEN the user should not be able to submit the registration and an error message is visible Passwords do not match
    """
    test_email = generate_test_email
    # Navigate to registration page
    page.goto(test_constants["REGISTRATION_URL"])
    # Fill in registration form
    page.get_by_label("Email Address").fill(test_email)
    page.get_by_label("Password", exact=True).fill(test_constants["TEST_PASSWORD"])

    # Non-matching password
    page.get_by_label("Retype Password").fill("87654321")
    page.get_by_role("button", name="Submit").click()
    error_message = page.locator("text=Passwords do not match")
    expect(error_message).to_be_visible()
