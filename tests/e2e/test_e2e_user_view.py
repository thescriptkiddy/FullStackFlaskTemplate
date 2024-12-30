from tests.conftest import authenticated_page
from playwright.sync_api import Page


def test_e2e_user_overview_page(authenticated_page: Page):
    """
    GIVEN An authenticated user
    WHEN wants to visit the user overview page
    THEN can see a table with all existing users
    :param authenticated_page:
    :return:
    """
    authenticated_page.goto("http://127.0.0.1:5000/users/")
    authenticated_page.wait_for_load_state("domcontentloaded")
    authenticated_page.get_by_text("All users in the Database").click()
