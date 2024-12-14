from flask import Blueprint

bp = Blueprint('api', __name__)

from backend.api.routes import items
