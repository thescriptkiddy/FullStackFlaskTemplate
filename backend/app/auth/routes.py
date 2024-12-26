from flask import render_template, redirect, request, flash, url_for
from sqlalchemy import select
from flask_security import logout_user, url_for_security


from backend.app.auth import bp


@bp.route("/")
def auth_index():
    return render_template("auth/index.html")
