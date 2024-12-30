from playwright.sync_api import Page, expect


def test_e2e_create_item(authenticated_page: Page):
    """
    GIVEN An authenticated user
    WHEN creates an item
    THEN it should be visible on the items overview page
    """
    authenticated_page.goto("http://127.0.0.1:5000/home/")
    authenticated_page.get_by_role("link", name=" Items").click()
    authenticated_page.get_by_role("button", name="Add an item").click()
    authenticated_page.get_by_label("Create new Item").click()
    authenticated_page.get_by_label("Create new Item").fill("New Item E2E")
    authenticated_page.get_by_role("button", name="Submit Item").click()
    authenticated_page.wait_for_load_state("domcontentloaded")
    expect(authenticated_page).to_have_url("http://127.0.0.1:5000/items/")
    authenticated_page.get_by_text("New Item E2E").click()
