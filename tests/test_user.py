from backend.models.user import User, load_user
from tests.user.conftest import new_user_in_db


def test_user_repr(new_user_in_db):
    """Test string representation of a user"""
    assert repr(new_user_in_db) == '<User hans.peter@gmail.com>'


# TODO Test Password Hashing


# TODO Test Unique Email Constraint

# TODO Test User Activation Status:

# TODO Test Password Change:

# Test Loading Non-Existent User:

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
