from flask import render_template, url_for, current_app
from backend.app.menu import bp
from backend.utils.route_helpers import generate_sitemap


@bp.route('/')
def index():
    return render_template("menu/index.html")


@bp.route('/sitemap')
def sitemap():
    return render_template("menu/sitemap.html", sitemap=generate_sitemap())
