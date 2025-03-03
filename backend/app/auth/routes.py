from flask import render_template, redirect, request, flash, url_for, jsonify
from flask_login import current_user
from sqlalchemy import select
from flask_security import logout_user, url_for_security, login_required

from backend.app.auth import bp


@bp.route("/")
def auth_index():
    return render_template("auth/index.html")


@bp.route('/test_auth')
@login_required
def test_auth():
    return jsonify({
        'authenticated': current_user.is_authenticated,
        'email': current_user.email if current_user.is_authenticated else None
    })
