from uuid import UUID

from flask import render_template, url_for, request, redirect, jsonify, flash
from flask_security import login_required
from sqlalchemy import select
from backend.utils.helper import handle_sql_exceptions
from shared.database import db_session
from backend.models.item import Item
from backend.app.items import bp
from backend.app.items.forms import CreateItemForm, UpdateItemForm
from backend.utils.route_helpers import nav_item
from backend.utils.database_helper import create_record, read_records, update_record, delete_record


@bp.route('/')
@login_required
@handle_sql_exceptions
@nav_item(title="Items", order=2)
def items_index():
    message = request.args.get('message')
    category = request.args.get('category', 'info')

    if message:
        flash(message, category)

    return render_template('items/index.html', all_items=read_records(Item))


@bp.route("/read/<string:uuid_str>", methods=["GET"])
@login_required
@handle_sql_exceptions
def read_item_by_id(uuid_str):
    uuid_obj = UUID(uuid_str)
    fetch_item = read_records(Item, uuid_obj)

    # Convert the item to a dictionary
    item_dict = {
        'id': str(fetch_item.id),
        'title': fetch_item.title,
        # Add other fields as needed
    }

    return jsonify(item_dict), 200


@bp.route('/edit-item/<string:uuid_str>', methods=["GET", "POST"])
@login_required
@handle_sql_exceptions
def update_item(uuid_str):
    uuid_obj = UUID(uuid_str)
    fetch_item = read_records(Item, uuid_obj)
    if not fetch_item:
        flash('Item not found', 'error')
        return redirect(url_for('items.items_index'))

    form = UpdateItemForm(obj=fetch_item)

    if form.validate_on_submit():
        if form.title.data != fetch_item.title:
            update_record(Item, uuid_obj,
                          title=form.title.data
                          )

            flash('Item successfully updated', 'success')
            return redirect(url_for('items.items_index'))
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
        create_record(Item,
                      title=form.title.data
                      )
        flash('Item created successfully', 'success')
        return redirect(url_for('items.items_index'))
    return render_template("items/create-item.html", form=form)


@bp.route('/delete/<string:uuid_str>', strict_slashes=False, methods=["DELETE"])
@login_required
@handle_sql_exceptions
def delete_item_by_id(uuid_str):
    uuid_obj = UUID(uuid_str)
    if delete_record(Item, uuid_obj):
        return jsonify({"status": "success", "message": "Item successfully deleted"}), 200
    else:
        return jsonify({"status": "error", "message": "Item not found"}), 404
