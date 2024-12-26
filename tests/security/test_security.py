from flask import session

from backend import db_session
from backend.models.user import User
from tests.user.conftest import new_user_in_db


def test_login_view(client):
    """Tests that login is available"""
    response = client.get('/login')
    assert b"Login" in response.data


def test_register_view(client):
    """Test that registration is available"""
    response = client.get('/register')
    assert b"Register" in response.data


def test_admin_view(client):
    """Test that the admin view is protected and user gets redirected"""
    response = client.get('/admin')
    assert response.status_code == 308


# todo seems to be a False-Positive case, I guess due to WTF-Forms enabled
def test_user_login(client, app, db, new_user_in_db):
    user = db_session.query(User).filter_by(email="hans.peter@gmail.com").first()
    if user:
        print(user)
        response = client.post("/login", data={
            "email": "hans.peter@gmail.com",
            "password": "admin42"
        }, follow_redirects=True)

        assert response.status_code == 200, f"Login failed: {response.data.decode()}"
        print(response.headers.get("Set-Cookie"))

        # print(f"Login Response: {response.status_code}, Data: {response.data.decode()}")

    else:
        print("User not found")
