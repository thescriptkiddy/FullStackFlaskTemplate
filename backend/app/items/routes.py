import os.path
from flask import render_template, url_for, request, redirect, jsonify, flash
from sqlalchemy import select

from backend.app.database import db_session
from backend.models.item import Item
from backend.app.items import bp
from backend.app.items.forms import CreateItemForm


@bp.route('/')
def items_index():
    result = db_session.execute(select(Item))
    all_items = result.scalars().all()
    return render_template('items/index.html', all_items=all_items)


@bp.route('/read/<uuid:item_id>', methods=["GET"])
def read_item_by_id(item_id):
    fetch_item_by_id = db_session.query(Item).filter(Item.uuid == item_id).first()
    print(fetch_item_by_id.title)
    return redirect(url_for('items.items_index'))


@bp.route('/create', methods=["GET"])
def create_item():
    form = CreateItemForm()
    return render_template("items/create-item.html", form=form)


@bp.route('/create', methods=["POST"])
def submit_item():
    form = CreateItemForm()
    if form.validate_on_submit():
        new_item = Item(
            title=form.title.data
        )
        db_session.add(new_item)
        db_session.commit()
        flash('Item created successfully', 'success')
        return redirect(url_for('items.items_index'))
    return render_template("items/create-item.html")


@bp.route('/delete/<uuid:item_id>', methods=["DELETE"])
def delete_item_by_id(item_id):
    fetch_item_by_id = db_session.query(Item).filter(Item.uuid == item_id).first()
    if fetch_item_by_id:
        db_session.delete(fetch_item_by_id)
        db_session.commit()
        return redirect(url_for('items.items_index'))
    else:
        return "Item not found", 404
