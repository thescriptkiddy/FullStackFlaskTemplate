from flask import render_template, url_for, current_app
from backend.app.menu import bp
from backend.utils.route_helpers import generate_route_map
from shared.config import TestingConfig


@bp.route('/')
def index():
    return render_template("menu/index.html")


@bp.route('/all-routes')
def get_all_routes():
    all_routes = generate_route_map()
    # Return a list of all urls
    list_of_urls = [url.get("url") for url in all_routes]

    return list_of_urls


@bp.route('/menu-links')
def get_all_menu_links():
    all_routes = generate_route_map()
    # Return a list of all urls
    list_of_menu_links = [f"{current_app.config['BASE_URL']}{url.get("url")}" for url in all_routes]

    return list_of_menu_links
