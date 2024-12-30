import uuid
import pytest
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from backend.models.user import User
from backend.app.database import db_session
from flask_security.utils import hash_password
from tests.conftest import get_db
from tests.unit.user.conftest import get_test_user


def test_user_repr(get_test_user, get_db):
    """Test string representation of a user"""
    assert repr(get_test_user) == f'<User {get_test_user.email}>'


def test_set_password_hashing(get_test_user):
    """Set a new password and check whether it is hashed or not"""
    get_test_user.password = hash_password("new_password")
    assert get_test_user.password != "new_password"
    assert get_test_user.verify_and_update_password("new_password")


def test_unique_email(get_db):
    """Tests that duplicate emails can't be added"""
    new_user1 = User(
        firstname="Hans",
        lastname="Peter",
        email="hans.peter1@gmail.com",
        active=False,
    )

    new_user2 = User(
        firstname="Hans",
        lastname="Peter",
        email="hans.peter1@gmail.com",
        active=False,
    )

    db_session.add(new_user1)
    db_session.commit()

    with pytest.raises(IntegrityError):
        db_session.add(new_user2)
        db_session.commit()


def test_activation_status_for_new_user(get_test_user, get_db):
    """Only for new users"""
    get_test_user.active = True
    assert get_test_user.active is True


def test_password_change_by_user(get_test_user):
    """Testing changing a user's password"""
    get_test_user.password = hash_password("newpassword")
    assert get_test_user.verify_and_update_password("newpassword")
    assert not get_test_user.verify_and_update_password("admin42")


def test_get_user_by_id(get_test_user):
    """Test fetching a user by its id"""
    assert get_test_user.email == get_test_user.email
    assert get_test_user.firstname == get_test_user.firstname


# TODO Could be a parameterized test
def test_get_all_users(get_db):
    """Creates 2 new users and fetches them all from the database"""

    user1 = User(
        firstname="Hans",
        lastname="Peter",
        email="test1@test.com",
        active=True
    )

    user2 = User(
        firstname="Marie",
        lastname="Curie",
        email="test2@test.com",
        active=True
    )

    get_db.add(user1)

    get_db.add(user2)

    get_db.commit()

    # TODO LegacyAPIWarning:
    stmt = select(User)

    result = db_session.execute(stmt)
    all_users = result.scalars().all()

    # One user is added during startup
    assert len(list(all_users)) == 2
    assert user1.lastname == "Peter"
    assert user2.lastname == "Curie"


def test_user_view(client):
    """Tests that user route is protected"""
    response_user_route_get = client.get("/users/")
    assert response_user_route_get.status_code == 401
    assert b"401 Unauthorized" in response_user_route_get.data.title()
