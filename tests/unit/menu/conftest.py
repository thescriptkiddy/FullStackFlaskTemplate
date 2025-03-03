import pytest
from sqlalchemy import select

from backend.models.menu import Menu, Link
from shared.database import db_session
from tests.conftest import test_user
from tests.unit.menu.mock_data import get_mock_menu_data


@pytest.fixture
def new_menu_in_db(get_db, test_user):
    """Fixture to create a new menu"""
    link_1 = Link(
        name="Home",
        endpoint="home.index",
        title="Go Home",
        order=0,
    )

    link_2 = Link(
        name="Items",
        endpoint="items.index_items",
        title="Items",
        order=0,
    )

    menu = Menu(
        name="Main Menu in DB",
        links=[link_1, link_2]
    )

    get_db.add(menu)
    get_db.add(link_1, link_2)

    get_db.commit()
    get_db.refresh(menu)

    return menu


@pytest.fixture(scope='session')
def mock_menu_data():
    return get_mock_menu_data()
