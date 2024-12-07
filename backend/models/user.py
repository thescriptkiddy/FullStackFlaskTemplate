import bcrypt
import uuid
from sqlalchemy.dialects.postgresql import UUID
from flask_login import UserMixin
from flask_security.models import sqla as sqla
from flask_security import UserMixin
from sqlalchemy.orm import relationship
from backend.app.database import Base, db_session
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Table
from shared.extensions import LoginManager, login_manager
from flask_bcrypt import Bcrypt

# roles_users = Table('roles_users', Base.metadata,
#                     Column('user_id', Integer(), ForeignKey('users.id'), primary_key=True),
#                     Column('role_id', Integer(), ForeignKey('roles.id'), primary_key=True)
#                     )

roles_users = Table('roles_users', Base.metadata,
                    Column('user_id', Integer(), ForeignKey('users.id')),
                    Column('role_id', Integer(), ForeignKey('roles.id'))
                    )


class User(Base, UserMixin):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    uuid = Column(UUID(as_uuid=True), unique=True, default=uuid.uuid4)
    fs_uniquifier = Column(String(255), unique=True, nullable=False, default=lambda: str(uuid.uuid4()))
    email = Column(String, unique=True)
    password = Column(String(255, ), nullable=False, server_default='')
    firstname = Column(String(50))
    lastname = Column(String(50))
    active = Column(Boolean)
    # roles_id = Column(Integer, ForeignKey('roles.id'))
    roles = relationship('Role', secondary=roles_users,
                         back_populates='users')

    # Relationships
    items = relationship("Item", back_populates="owner")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.fs_uniquifier:
            self.fs_uniquifier = uuid.uuid4().hex

    def __repr__(self):
        return f'<User {self.email}>'

    def set_password(self, password: str) -> str:
        password_bytes = password.encode('utf-8')
        salt = bcrypt.gensalt()
        self.password = bcrypt.hashpw(password_bytes, salt).decode('utf-8')
        return self.password

    def check_password(self, password: str) -> bool:
        password_bytes = password.encode('utf-8')
        return bcrypt.checkpw(password_bytes, self.password.encode('utf-8'))


# User-ID needs to be a string

class UserNotFoundError(Exception):
    pass


@login_manager.user_loader
def load_user(user_id):
    return db_session.get(User, user_id)
