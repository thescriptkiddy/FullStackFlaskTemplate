import bcrypt
import uuid
from sqlalchemy.dialects.postgresql import UUID
from flask import current_app
from flask_login import UserMixin
from sqlalchemy.orm import relationship

from shared.extensions import db, login_manager
from flask_bcrypt import Bcrypt


class User(db.Model, UserMixin):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    uuid = db.Column(UUID(as_uuid=True), unique=True, default=uuid.uuid4)
    email = db.Column(db.String, unique=True)
    password_hash = db.Column(db.String(255, ))
    firstname = db.Column(db.String(50))
    lastname = db.Column(db.String(50))
    is_active = db.Column(db.Boolean)

    # Relationships
    items = relationship("Item", back_populates="owner")

    def __repr__(self):
        return f'<User {self.email}>'

    def set_password(self, password: str) -> str:
        password_bytes = password.encode('utf-8')
        salt = bcrypt.gensalt()
        self.password_hash = bcrypt.hashpw(password_bytes, salt).decode('utf-8')
        return self.password_hash

    def check_password(self, password: str) -> bool:
        password_bytes = password.encode('utf-8')
        return bcrypt.checkpw(password_bytes, self.password_hash.encode('utf-8'))


# User-ID needs to be a string

class UserNotFoundError(Exception):
    pass


# TODO UUID Handling issues
@login_manager.user_loader
def load_user(user_id):
    user = db.get_or_404(User, user_id)
    if user is None:
        raise UserNotFoundError(f"User with id {user_id} does not exist")
    return user
