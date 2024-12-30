import uuid

from sqlalchemy.dialects.postgresql import UUID
from flask_security import UserMixin
from sqlalchemy.orm import relationship
from shared.database import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Table

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
