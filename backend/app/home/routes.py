from flask import render_template
from backend.app.home import bp
from backend.utils.route_helpers import nav_item


@bp.route('/')
@nav_item(title="Home", order=0)
def index():
    return render_template("home/index.html")
