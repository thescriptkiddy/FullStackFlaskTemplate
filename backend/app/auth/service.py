from backend.app.database import db_session
from backend.models.user import User


def load_user(user_id):
    return db_session.get(User, user_id)
