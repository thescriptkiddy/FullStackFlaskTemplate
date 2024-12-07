from flask import render_template, redirect
from backend.app.auth import bp


@bp.route("/")
def index():
    return render_template("auth/index.html")


# @bp.route("/register")
# def register_user():
#     render_template("register_user.html")

