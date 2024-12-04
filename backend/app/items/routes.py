import os.path
from flask import render_template, url_for, request, redirect
from backend.models.item import Item
from backend.app.items import bp


@bp.route('/')
def items_index():
    return render_template('items/index.html')


