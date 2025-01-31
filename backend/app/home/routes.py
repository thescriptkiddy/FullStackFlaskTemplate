from flask import render_template
from sqlalchemy import select

from backend.app.home import bp
from backend.models.item import Item
from shared.database import db_session


@bp.route('/')
def index():
    return render_template("home/index.html")


@bp.route('/testing-templates')
def home_testing_templates():
    """Just a route for testing"""
    result = db_session.execute(select(Item))
    items = result.scalars().all()
    return render_template("components/card_competition.html", items=items)
