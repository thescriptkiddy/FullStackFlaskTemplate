from playwright.sync_api import Page, expect
import asyncio


def test_e2e_create_item(authenticated_page: Page, test_constants):
    """
    GIVEN An authenticated user
    WHEN creates an item
    THEN it should be visible on the items overview page
    """
    authenticated_page.goto(test_constants["BASE_URL"])
    authenticated_page.get_by_role("link", name=" Items").click()
    authenticated_page.get_by_role("button", name="Add an item").click()
    authenticated_page.get_by_label("Create new Item").click()
    authenticated_page.get_by_label("Create new Item").fill("New Item E2E")
    authenticated_page.get_by_role("button", name="Submit Item").click()
    authenticated_page.wait_for_load_state("domcontentloaded")
    expect(authenticated_page).to_have_url(test_constants["ITEMS_PAGE"])
    authenticated_page.get_by_text("New Item E2E").click()


def test_item_overview_with_authentication(authenticated_page: Page, test_constants):
    """
    GIVEN An authenticated user
    WHEN views the items overview page
    THEN can the table view
    """
    authenticated_page.goto(test_constants["ITEMS_PAGE"])
    authenticated_page.get_by_text("All items in the Database").click()


def test_e2e_delete_item(authenticated_page: Page, test_constants):
    """
    GIVEN An authenticated user
    WHEN deletes an item
    THEN it should not be visible anymore
    """
    authenticated_page.goto(test_constants["ITEMS_PAGE"])
    authenticated_page.wait_for_selector(test_constants["DELETE_BUTTON_SELECTOR"])
    authenticated_page.on("dialog", lambda dialog: dialog.accept())

    # initial_item_count = authenticated_page.locator('button[name="delete-item"]').count()
    initial_item_count = authenticated_page.locator(test_constants["DELETE_BUTTON_SELECTOR"]).count()

    authenticated_page.locator(test_constants["DELETE_BUTTON_SELECTOR"]).first.click()
    authenticated_page.wait_for_load_state('networkidle')

    success_message = authenticated_page.locator(test_constants["SUCCESS_MESSAGE_SELECTOR"])
    expect(success_message).to_be_visible()
    expect(success_message).to_contain_text("Item successfully deleted")

    expect(authenticated_page.locator('button[name="delete-item"]')).to_have_count(initial_item_count - 1)
