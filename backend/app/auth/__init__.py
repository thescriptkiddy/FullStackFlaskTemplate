from flask import Blueprint

bp = Blueprint('auth', __name__)

from backend.app.auth import routes

