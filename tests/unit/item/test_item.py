from backend import db_session
from backend.models.item import Item
from tests.conftest import authenticated_page
from tests.conftest import test_user


def test_item_repr(new_item_in_db):
    """Test string representation of an item"""
    assert repr(new_item_in_db) == '<Item New Item in DB>'


def test_create_item(new_item_in_db, test_user):
    """Tests if an item has been added into the database"""
    assert new_item_in_db is not None
    assert new_item_in_db.title == "New Item in DB"
    assert new_item_in_db.owner_id == test_user.id
    assert new_item_in_db.uuid is not None


def test_read_item(new_item_in_db):
    assert new_item_in_db is not None
    fetch_item = db_session.query(Item).filter_by(owner_id=new_item_in_db.owner_id).first()
    assert new_item_in_db.owner_id == fetch_item.owner_id


def test_update_item(new_item_in_db):
    """Tests whether a title can be changed"""
    assert new_item_in_db is not None, "New item should exist in the database"
    original_title = new_item_in_db.title
    new_title = "Updated title"
    new_item_in_db.title = new_title
    db_session.commit()
    db_session.refresh(new_item_in_db)
    assert new_item_in_db.title == new_title, f"Title should be updated to {new_title}"
    assert new_item_in_db.title != original_title, f"New title should be different"


def test_delete_item(new_item_in_db):
    assert new_item_in_db is not None
    item_uuid = new_item_in_db.uuid
    db_session.delete(new_item_in_db)
    db_session.commit()
    deleted_item = db_session.query(Item).filter_by(uuid=item_uuid).first()
    assert deleted_item is None


def test_item_relationship(new_item_in_db, test_user):
    assert new_item_in_db.owner == test_user
    assert new_item_in_db in test_user.items


def tests_items_view(client):
    """Tests that the items route is protected"""
    response_item_route_get = client.get("/items/")
    assert response_item_route_get.status_code == 401
    assert b"401 Unauthorized" in response_item_route_get.data.title()
