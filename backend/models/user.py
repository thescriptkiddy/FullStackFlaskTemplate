import bcrypt
import uuid
from sqlalchemy.dialects.postgresql import UUID
from flask_security import UserMixin
from sqlalchemy.orm import relationship, Mapped, mapped_column
from backend.app.database import Base, db_session
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Table
from pydantic import BaseModel, EmailStr, Field

# todo Refactor to Annotated Declarative Mapping. Use Mapped, mapped_column instead of Column
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
    # Relationships
    roles = relationship('Role', secondary=roles_users,
                         back_populates='users')

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


# DataTransferObject Classes currently not in use!


class UserCreate(BaseModel):
    email: EmailStr = Field(max_length=255)
    password: str = Field(min_length=8)
    firstname: str | None = Field(default=None, max_length=255)
    lastname: str | None = Field(default=None, max_length=255)


class UserRegistration(BaseModel):
    email: EmailStr = Field(max_length=255)
    password: str = Field(min_length=8)
    firstname: str = Field(max_length=255)
    lastname: str = Field(max_length=255)


class UserUpdate(BaseModel):
    firstname: str | None = Field(max_length=255)
    lastname: str | None = Field(max_length=255)
    email: EmailStr | None = Field(max_length=255)


class UserPasswordChange(BaseModel):
    current_password: str = Field(min_length=8)
    new_password: str = Field(min_length=8)


class UserPublic(BaseModel):
    id: int
    email: EmailStr = Field(max_length=255)
    firstname: str = Field(max_length=255)
    lastname: str = Field(max_length=255)
    active: bool


class UserInternal(UserPublic):
    uuid: uuid.UUID
    fs_uniquifier: str
    roles: list[str]


# User-ID needs to be a string

class UserNotFoundError(Exception):
    pass
