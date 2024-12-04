import pytest
from shared.extensions import db
from backend.models.user import User
from backend.models.item import Item


@pytest.fixture
def new_item_in_db(init_database):
    """Fixture for new item in database"""

    new_item = Item(
        title="New Item in DB",

    )

    db.session.add(new_item)
    db.session.commit()

    return new_item




