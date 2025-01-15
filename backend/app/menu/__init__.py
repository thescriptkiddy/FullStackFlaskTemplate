from flask import Blueprint

bp = Blueprint('menu', __name__, template_folder="../frontend/templates/menu", url_prefix="/menu")

from backend.app.menu import routes
