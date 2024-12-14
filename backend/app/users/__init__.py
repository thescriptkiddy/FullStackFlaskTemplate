from flask import Blueprint

bp = Blueprint('users', __name__, template_folder="../frontend/templates/hans", url_prefix="/users")

from backend.app.users import routes

