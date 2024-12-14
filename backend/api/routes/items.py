import json
import os.path
from flask import render_template, url_for, request, redirect, jsonify
from sqlalchemy import select
from werkzeug.exceptions import HTTPException

from backend.app.database import db_session
from backend.models.item import Item
from backend.api import bp
from backend.utils.helper import AlchemyEncoder


# All API Routes for Items

# Maybe I will implement Flask-Marshmallow
@bp.route('/', methods=["GET"])
def read_all_items():
    items = db_session.query(Item).all()
    items_json = json.dumps(items, cls=AlchemyEncoder)
    print(items_json)
    return items_json


@bp.route('/items', methods=["POST"])
def create_item():
    if request.method == "POST":
        new_item = Item(
            title=request.data.title()
        )
        db_session.add(new_item)
        db_session.commit()
        db_session.refresh(new_item)
        return new_item


@bp.route('/items/<int:item_id>', methods=["PUT"])
def update_item_by_id(item_id):
    raise HTTPException("404")


@bp.route('/items/<int:item_id>', methods=["DELETE"])
def delete_item_by_id(item_id):
    db_session.delete(item_id)
    db_session.commit()

    return item_id
