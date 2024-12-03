import pytest
from shared.extensions import db
from backend.models.user import User


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

    db.session.add(new_user)
    db.session.commit()

    return new_user
