from shared.database import Base, db_session
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Table, select
from sqlalchemy.orm import mapped_column, Mapped, relationship
from typing import List

menus_links = Table(
    'menus_links',
    Base.metadata,
    Column('menu_id', Integer(), ForeignKey('menus.id')),
    Column('link_id', Integer(), ForeignKey('links.id'))
)


class Link(Base):
    __tablename__ = "links"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), unique=True)
    url: Mapped[str] = mapped_column(String(255), unique=True)
    menus: Mapped[List['Menu']] = relationship("Menu", secondary=menus_links, back_populates="links")

    def __repr__(self):
        return f"<Link {self.name}: {self.url}>"


class Menu(Base):
    __tablename__ = "menus"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), unique=True)
    links: Mapped[List[Link]] = relationship("Link", secondary=menus_links, back_populates="menus")

    # String representation
    def __repr__(self):
        return f'<Menu {self.name}>'

    @staticmethod
    def get_all_menus():
        all_menus = db_session.execute(select(Menu)).scalars().all()
        return all_menus
