import pytest
from backend.models.item import Item
from shared.database import db_session
from tests.conftest import test_user


@pytest.fixture
def new_item_in_db(get_db, test_user):
    """Fixture for new item in database"""
    new_item = Item(
        title="New Item in DB",
        owner_id=test_user.id,
    )
    get_db.add(new_item)
    get_db.commit()

    return new_item
