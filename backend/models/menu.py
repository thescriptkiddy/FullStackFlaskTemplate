import uuid
from shared.database import Base, db_session
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Table, select
from sqlalchemy.orm import mapped_column, Mapped, relationship
from typing import List
from sqlalchemy.dialects.postgresql import UUID

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
    endpoint: Mapped[str] = mapped_column(String(255), unique=True)
    menus: Mapped[List['Menu']] = relationship("Menu", secondary=menus_links, back_populates="links")

    def __repr__(self):
        return f"<Link {self.name}: {self.endpoint}>"


class Menu(Base):
    __tablename__ = "menus"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), unique=True)
    links: Mapped[List[Link]] = relationship("Link", secondary=menus_links, back_populates="menus")

    # String representation
    def __repr__(self):
        return f'<Menu {self.name}>'

    @staticmethod
    def get_menu_data():
        all_menus = db_session.execute(select(Menu)).scalars().all()

        menu_data = []
        for menu in all_menus:
            menu_info = {
                'name': menu.name,
                'id': menu.id,
                # Dict comprehension
                'links': [{'name': link.name, 'url': link.endpoint} for link in menu.links]
            }
            menu_data.append(menu_info)

        return menu_data
