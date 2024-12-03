import bcrypt
from flask import current_app
from flask_login import UserMixin
from shared.extensions import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_bcrypt import Bcrypt


class User(db.Model, UserMixin):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    password_hash = db.Column(db.String(255, ))
    firstname = db.Column(db.String(100))
    lastname = db.Column(db.String(100))
    is_active = db.Column(db.Boolean)

    def set_password(self, password: str) -> None:
        password_bytes = password.encode('utf-8')
        salt = bcrypt.gensalt()
        self.password_hash = bcrypt.hashpw(password_bytes, salt).decode('utf-8')

    def check_password(self, password: str) -> bool:
        password_bytes = password.encode('utf-8')
        return bcrypt.checkpw(password_bytes, self.password_hash.encode('utf-8'))
