from flask import Blueprint

bp = Blueprint('home', __name__, url_prefix="/home", template_folder="../frontend/templates/home")

from backend.app.home import routes
