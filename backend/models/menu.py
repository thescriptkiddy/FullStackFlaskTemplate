import uuid

from flask import jsonify

from shared.database import Base, db_session
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Table, select
from sqlalchemy.orm import mapped_column, Mapped, relationship
from typing import List
from sqlalchemy.dialects.postgresql import UUID
from backend.utils.helper import handle_sql_exceptions

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
    endpoint: Mapped[str] = mapped_column(String(255))
    title: Mapped[str] = mapped_column(String(255))
    order: Mapped[int] = mapped_column(Integer)
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
    @handle_sql_exceptions
    def get_menu_data(**kwargs):
        query = select(Menu)
        if 'menu_id' in kwargs:
            query = query.filter(Menu.id == kwargs['menu_id'])

        menus = db_session.execute(query).scalars().all()

        menu_data = []
        for menu in menus:
            menu_info = {
                'name': menu.name,
                'id': menu.id,
                'links': [{'name': link.name, 'endpoint': link.endpoint, 'title': link.title, 'id': link.id} for link in
                          menu.links]
            }
            menu_data.append(menu_info)

        if 'menu_id' in kwargs and menu_data:
            return menu_data[0]['links']

        return menu_data

    @staticmethod
    @handle_sql_exceptions
    def delete_menu(menu_id):
        menu = db_session.scalars(select(Menu).filter_by(id=menu_id)).first()
        if menu:
            # Clear the relationships
            menu.links = []
            # Delete the menu
            db_session.delete(menu)
            db_session.commit()
            return jsonify({"status": "success", "message": "Menu deleted successfully"}), 200

        else:
            return jsonify({"status": "error", "message": "Item not found"}), 404
