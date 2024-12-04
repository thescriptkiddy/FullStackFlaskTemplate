from flask import Blueprint

bp = Blueprint('items', __name__, template_folder="frontend/templates/items")

from backend.app.items import routes


