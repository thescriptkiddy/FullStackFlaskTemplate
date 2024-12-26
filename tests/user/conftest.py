import pytest
from flask_security.utils import hash_password
from backend.models.user import User
from tests.conftest import db_session
from tests.conftest import init_database


@pytest.fixture
def new_user_in_db(init_database):
    """Fixture to create and add a user to the database"""

    new_user = User(
        firstname="Hans",
        lastname="Peter",
        email="hans.peter@gmail.com",
        active=True,
    )

    new_user.password = hash_password("admin42")

    db_session.add(new_user)
    db_session.commit()
    return new_user
