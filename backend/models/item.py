import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from shared.database import Base
from sqlalchemy import Column, Integer, String, ForeignKey


# todo Refactor to Annotated Declarative Mapping. Use Mapped, mapped_column instead of Column
class Item(Base):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True, autoincrement=True)
    uuid = Column(UUID(as_uuid=True), unique=True, default=uuid.uuid4)
    title = Column(String(255), nullable=False)
    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="items")

    def __repr__(self):
        return f'<Item {self.title}>'
