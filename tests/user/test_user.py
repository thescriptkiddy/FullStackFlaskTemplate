import pytest
from sqlalchemy.exc import IntegrityError
from backend.models.user import User, load_user, UserNotFoundError
from tests.user.conftest import new_user_in_db, db


def test_user_repr(new_user_in_db):
    """Test string representation of a user"""
    assert repr(new_user_in_db) == '<User hans.peter@gmail.com>'


def test_set_password_hashing(new_user_in_db):
    """Set a new password and check whether it is hashed or not"""
    new_user_in_db.set_password("new_password")
    assert new_user_in_db.password_hash != "new_password"
    assert new_user_in_db.check_password("new_password")


def test_unique_email(init_database):
    """Tests that duplicate emails can't be added"""
    new_user1 = User(
        firstname="Hans",
        lastname="Peter",
        email="hans.peter@gmail.com",
        is_active=False,
    )

    new_user2 = User(
        firstname="Hans",
        lastname="Peter",
        email="hans.peter@gmail.com",
        is_active=False,
    )

    init_database.session.add(new_user1)
    init_database.session.commit()

    with pytest.raises(IntegrityError):
        init_database.session.add(new_user2)
        init_database.session.commit()


def test_activation_status_for_new_user(new_user_in_db):
    """Only for new users"""
    assert new_user_in_db.is_active is not True

    new_user_in_db.is_active = True
    assert new_user_in_db.is_active is True


def test_password_change_by_user(new_user_in_db):
    """Testing changing a user's password"""
    assert new_user_in_db.set_password("newpassword")
    assert new_user_in_db.check_password("newpassword")
    assert not new_user_in_db.check_password("admin42")


# TODO UUID Handling issues
# def test_to_load_non_exiting_user(new_user_in_db):
#     with pytest.raises(UserNotFoundError) as info:
#         load_user("23c39cc3-60ef-4cf7-b718-4aa5414c6285")
#     assert str(info.value) == "User with id 23c39cc3-60ef-4cf7-b718-4aa5414c6285 does not exist"


def test_new_user_in_db(new_user_in_db):
    assert new_user_in_db is not None
    assert new_user_in_db.email == "hans.peter@gmail.com"
    assert new_user_in_db.check_password("admin42")


def test_get_user_by_id(new_user_in_db):
    """Test fetching a user by its id"""

    fetched_user = load_user(new_user_in_db.id)

    assert fetched_user.id == new_user_in_db.id
    assert fetched_user.firstname == new_user_in_db.firstname


def test_get_all_users(init_database):
    """Creates 2 new users and fetches them all from the database"""
    user1 = User(
        firstname="Hans",
        lastname="Peter",
        email="hans.peter1@gmail.com",
        is_active=False,
    )

    user2 = User(
        firstname="Marie",
        lastname="Curie",
        email="marie.curie@gmail.com",
        is_active=False,
    )

    init_database.session.add(user1)
    init_database.session.add(user2)
    init_database.session.commit()

    result = init_database.session.execute(init_database.Select(User))
    all_users = result.scalars()

    assert len(list(all_users)) == 2
    assert user1.lastname == "Peter"
    assert user2.lastname == "Curie"
