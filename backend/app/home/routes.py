from flask import render_template
from backend.app.home import bp


@bp.route('/')
def index():
    return render_template("home/index.html")


@bp.route('/testing-templates')
def home_testing_templates():
    """Just a route for testing"""
    return render_template("home/bootstrap-table.html")
