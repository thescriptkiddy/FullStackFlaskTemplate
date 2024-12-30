from flask_security import RoleMixin
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
import uuid
from shared.database import Base
from sqlalchemy import Column, Integer, String
from backend.models.user import roles_users


# todo Refactor to Annotated Declarative Mapping. Use Mapped, mapped_column instead of Column
class Role(Base, RoleMixin):
    __tablename__ = 'roles'
    id = Column(Integer, primary_key=True, autoincrement=True)
    uuid = Column(UUID(as_uuid=True), unique=True, default=uuid.uuid4)
    description = Column(String, unique=True)
    permissions = Column(String, nullable=True)

    users = relationship('User', secondary=roles_users,
                         back_populates='roles')
