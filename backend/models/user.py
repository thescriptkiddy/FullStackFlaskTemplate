import bcrypt
import uuid
from sqlalchemy.dialects.postgresql import UUID
from flask import current_app
from flask_login import UserMixin
from shared.extensions import db, login_manager
from flask_bcrypt import Bcrypt


class User(db.Model, UserMixin):
    __tablename__ = "user"
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True)
    password_hash = db.Column(db.String(255, ))
    firstname = db.Column(db.String(50))
    lastname = db.Column(db.String(50))
    is_active = db.Column(db.Boolean)

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
@login_manager.user_loader
def load_user(user_id):
    return db.get_or_404(User, user_id)
