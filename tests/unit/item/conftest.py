import pytest
from backend.models.item import Item
from backend.app.database import db_session


@pytest.fixture
def new_item_in_db(get_db):
    """Fixture for new item in database"""
    new_item = Item(
        title="New Item in DB",

    )
    db_session.add(new_item)
    db_session.commit()

    return new_item
