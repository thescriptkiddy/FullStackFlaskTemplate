from flask import render_template
from backend.app.home import bp


@bp.route('/')
def index():
    return render_template("home/index.html")
