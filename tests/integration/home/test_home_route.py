import flask_security
import pytest

from flask_security import current_user
from sqlalchemy import select
from backend.models.user import User


def test_home_route(client):
    response = client.get('/home/')
    assert response.status_code == 200
    assert b"Home" in response.data
