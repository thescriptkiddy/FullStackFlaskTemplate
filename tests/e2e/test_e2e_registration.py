import re
import time
from playwright.sync_api import Page, expect, Playwright
from tests.e2e.conftest import setup_flask_server, page


def test_registration_within_content_area(page: Page, setup_flask_server) -> None:
    """
    GIVEN A visitor wants to create an account
    WHEN the visitor provides a valid email address and password
    THEN the visitor must be able to create an account and without confirming the email address and
    is automatically authenticated and redirected to the homepage
    :param page:
    :param setup_flask_server:
    :return:
    """
    page.goto("http://127.0.0.1:5000/home/")
    page.get_by_role("button", name="Register").click()
    page.get_by_label("Email Address").click()
    page.get_by_label("Email Address").fill("simon333@simon.de")
    page.get_by_label("Email Address").press("Tab")
    page.get_by_label("Password", exact=True).fill("12345678")
    page.get_by_label("Password", exact=True).press("Tab")
    page.get_by_label("Retype Password").fill("12345678")
    page.get_by_label("Retype Password").press("Tab")
    page.get_by_label("First Name").fill("Test")
    page.get_by_label("First Name").press("Tab")
    page.get_by_label("Last Name").fill("User")
    page.get_by_role("button", name="Submit").click()
    page.wait_for_load_state("domcontentloaded")