import pytest
from backend.models.user import User
from flask_security import login_user
from shared.database import db_session


@pytest.fixture
def authenticated_client(app):
    with app.app_context():
        user = User(email='test@example.com', password='password', active=True)
        db_session(user)
        db_session.commit()

        login_user(user)

    return client
