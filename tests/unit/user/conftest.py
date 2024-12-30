import uuid

import pytest
from flask_security.utils import hash_password
from sqlalchemy.exc import IntegrityError

from backend.models.user import User
from tests.conftest import db_session


@pytest.fixture(scope="function")
def get_test_user(get_db):
    """Fixture to create and add a test user"""
    unique_email = f"hans.peter_{uuid.uuid4()}@gmail.com"
    new_user = User(
        firstname="Hans",
        lastname="Peter",
        email=unique_email,
        active=True,
    )

    new_user.password = hash_password("admin42")

    db_session.add(new_user)

    try:
        db_session.commit()
        yield new_user
    except IntegrityError:
        db_session.rollback()
        print("A user with this email already exists")
        raise
