import pytest
from backend.models.menu import Menu
from shared.database import db_session
from tests.conftest import test_user
from tests.unit.menu.mock_data import get_mock_menu_data


@pytest.fixture
def new_menu_item(get_db, test_user):
    """Fixture to create a new menu"""
    menu = Menu(
        name="New Menu",
        links=[{'id': 1, 'name': 'Home', 'endpoint': 'home.index', 'title': 'Home'},
               {'id': 2, 'name': 'Menus', 'endpoint': 'menu.index', 'title': 'Menus'},
               {'id': 3, 'name': 'Users', 'endpoint': 'users.users_index', 'title': 'Users'}
               ]
    )

    get_db.add(menu)
    get_db.commit()

    return menu


@pytest.fixture(scope='session')
def mock_menu_data():
    return get_mock_menu_data()
