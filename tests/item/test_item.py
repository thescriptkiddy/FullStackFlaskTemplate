from backend.models.item import Item
from tests.item.conftest import new_item_in_db
from shared.extensions import db

def test_item_repr(new_item_in_db):
    """Test string representation of an item"""
    assert repr(new_item_in_db) == '<Item New Item in DB>'


def test_new_item_in_db(new_item_in_db):
    """Tests if an item has been added into the database"""
    assert new_item_in_db is not None
    assert new_item_in_db.title == "New Item in DB"


def test_change_title(new_item_in_db):
    """Tests whether a title can be changed"""
    assert new_item_in_db is not None
    original_title = new_item_in_db.title

    new_title = "Updated title"
    new_item_in_db.title = new_title

    db.session.commit()

    db.session.refresh(new_item_in_db)

    assert new_item_in_db.title == new_title
    assert new_item_in_db.title != original_title

