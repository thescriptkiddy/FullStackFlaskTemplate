from flask import render_template, redirect, request, flash, url_for
from sqlalchemy import select

from backend import User
from backend.app.auth import bp
from backend.app.auth.forms import ExtendedRegisterForm
from backend.app.database import db_session


@bp.route("/")
def index():

    return render_template("auth/index.html")




