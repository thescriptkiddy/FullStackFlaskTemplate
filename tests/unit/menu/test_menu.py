import pytest
from sqlalchemy import select, func

from backend.models.menu import Menu, Link, menus_links
from tests.conftest import get_db
from tests.unit.menu.conftest import new_menu_in_db


def test_menu_repr(new_menu_in_db):
    """Tests string representation of a menu"""
    assert repr(new_menu_in_db) == '<Menu Main Menu in DB>'


def test_create_menu_with_links(new_menu_in_db):
    """
    GIVEN An authenticated user
    WHEN wants to create a new menu with available links (aka ui-routes)
    THEN a new menu model with relations to available links models have been saved to the database
    :return:
    """
    assert new_menu_in_db.name == "Main Menu in DB"
    assert len(new_menu_in_db.links) == 2
    assert all([link.name in ["Home", "Items"] for link in new_menu_in_db.links])
    assert all([link.endpoint in ["home.index", "items.index_items"] for link in new_menu_in_db.links])

    assert all(new_menu_in_db in link.menus for link in new_menu_in_db.links)


def test_delete_existing_menu(new_menu_in_db, get_db):
    """
    GIVEN a menu with links in the database
    WHEN the delete_menu method is called
    THEN the menu should be deleted, but the links should remain, with relationships removed
    """
    menu_id = new_menu_in_db.id
    link_ids = [link.id for link in new_menu_in_db.links]

    assert get_db.scalars(select(Menu).filter_by(id=menu_id)).first()
    assert all(get_db.scalars(select(Link).filter_by(id=link_id)) is not None for link_id in link_ids)

    result, status_code = Menu.delete_menu(menu_id)

    assert status_code == 200
    assert result.json['status'] == 'success'
    assert result.json['message'] == 'Menu deleted successfully'

    count_query = select(func.count()).select_from(menus_links).where(menus_links.c.menu_id == menu_id)
    remaining_relationships = get_db.execute(count_query).scalar()
    assert remaining_relationships == 0


def test_get_menu_data(new_menu_in_db, get_db):
    """Tests the get_menu_data function without any optional kwargs"""
    # assert get_db.execute(select(Menu)).scalars().all() == Menu.get_menu_data()
    menu_id = new_menu_in_db.id

    result = Menu.get_menu_data()

    # Checks that the result is a list
    assert isinstance(result, list)
    assert len(result) == 1

    menu_data = result[0]

    assert menu_data['name'] == 'Main Menu in DB'
    assert menu_data['id'] == menu_id

    assert 'links' in menu_data
    assert isinstance(menu_data['links'], list)
    assert len(menu_data['links']) == len(new_menu_in_db.links)

    # Tests the get_menu_data function with a kwarg
    links_only = Menu.get_menu_data(menu_id=menu_id)
    assert isinstance(links_only, list)
    assert len(links_only) == len(new_menu_in_db.links)
    for link_data, original_link in zip(links_only, new_menu_in_db.links):
        assert link_data['name'] == original_link.name
        assert link_data['endpoint'] == original_link.endpoint
        assert link_data['title'] == original_link.title
        assert link_data['id'] == original_link.id
