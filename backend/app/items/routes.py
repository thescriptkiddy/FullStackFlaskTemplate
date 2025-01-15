from uuid import UUID

from flask import render_template, url_for, request, redirect, jsonify, flash
from flask_security import login_required
from sqlalchemy import select
from backend.utils.helper import handle_sql_exceptions
from shared.database import db_session
from backend.models.item import Item
from backend.app.items import bp
from backend.app.items.forms import CreateItemForm, UpdateItemForm


@bp.route('/')
@login_required
@handle_sql_exceptions
def items_index():
    result = db_session.execute(select(Item))
    all_items = result.scalars().all()

    message = request.args.get('message')
    category = request.args.get('category', 'info')

    if message:
        flash(message, category)

    return render_template('items/index.html', all_items=all_items)


@bp.route("/read/<string:uuid_str>", methods=["GET"])
@login_required
@handle_sql_exceptions
def read_item_by_id(uuid_str):
    uuid_obj = UUID(uuid_str)
    fetch_item = db_session.query(Item).filter(Item.uuid == uuid_obj).first()
    if not fetch_item:
        flash("Item not found", category='error')
        return jsonify({"status": "error", "message": "Item not found"}), 404
    else:
        return fetch_item


@bp.route('/edit-item/<string:uuid_str>', methods=["GET", "POST"])
@login_required
@handle_sql_exceptions
def update_item(uuid_str):
    uuid_obj = UUID(uuid_str)
    fetch_item = db_session.query(Item).filter(Item.uuid == uuid_obj).first()
    if not fetch_item:
        flash('Item not found', 'error')
        return redirect(url_for('items.items_index'))

    form = UpdateItemForm(obj=fetch_item)

    if form.validate_on_submit():
        if form.title.data != fetch_item.title:
            fetch_item.title = form.title.data
            db_session.commit()
            flash('Item successfully updated', 'success')
        else:
            flash('No changes were made', 'info')
            return redirect(url_for('items.items_index'))
    return render_template("items/edit-item.html", is_edit=True, form=form, item=fetch_item)


@bp.route('/create', methods=["GET", "POST"])
@login_required
@handle_sql_exceptions
def create_item():
    form = CreateItemForm()
    if form.validate_on_submit():
        new_item = Item(
            title=form.title.data
        )
        db_session.add(new_item)
        db_session.commit()
        flash('Item created successfully', 'success')
        return redirect(url_for('items.items_index'))
    return render_template("items/create-item.html", form=form)


@bp.route('/delete/<string:uuid_str>', strict_slashes=False, methods=["DELETE"])
@login_required
@handle_sql_exceptions
def delete_item_by_id(uuid_str):
    uuid_obj = UUID(uuid_str)
    fetch_item_by_id = db_session.query(Item).filter(Item.uuid == uuid_obj).first()
    if fetch_item_by_id:
        db_session.delete(fetch_item_by_id)
        db_session.commit()
        return jsonify({"status": "success", "message": "Item successfully deleted"}), 200
    else:
        return jsonify({"status": "error", "message": "Item not found"}), 404
