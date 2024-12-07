import pytest

from backend.models.user import User
from backend.models.item import Item
from backend.app.database import db_session, Session, engine, Base


@pytest.fixture
def new_item_in_db(init_database):
    """Fixture for new item in database"""

    new_item = Item(
        title="New Item in DB",

    )

    db_session.add(new_item)
    db_session.commit()

    return new_item




