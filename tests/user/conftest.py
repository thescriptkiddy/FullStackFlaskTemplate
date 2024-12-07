import pytest

from backend.models.user import User
from backend.app.database import db_session


@pytest.fixture
def new_user_in_db(init_database):
    """Fixture to create and add a user to the database"""

    new_user = User(
        firstname="Hans",
        lastname="Peter",
        email="hans.peter@gmail.com",
        is_active=False,
    )

    new_user.set_password(password="admin42")

    db_session.add(new_user)
    db_session.commit()
    return new_user
