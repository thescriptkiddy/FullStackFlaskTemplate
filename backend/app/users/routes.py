import os.path
from flask import render_template, url_for, request, redirect, jsonify, flash
from flask_login import login_required
from sqlalchemy import select
from backend.app.database import db_session
from backend.app.users import bp
from backend.models.user import User
from backend.app.users.forms import CreateUserForm


@bp.route('/')
def users_index():
    result = db_session.execute(select(User))
    all_users = result.scalars().all()

    return render_template('users/index.html', all_users=all_users)


# Temporary route for testing. It transfers a complete user object

@bp.route('/profile/<string:fs_uniquifier>', methods=["GET"])
@login_required
def load_user_profile_by_id(fs_uniquifier):
    fetch_item_by_id = db_session.query(User).filter(User.fs_uniquifier == fs_uniquifier).first()

    return render_template("users/profile.html", user=fetch_item_by_id)


@bp.route('/create', methods=["GET"])
def create_user():
    form = CreateUserForm()

    return render_template('users/create-user.html', form=form)


@bp.route('/create', methods=["POST"])
def submit_user():
    form = CreateUserForm()
    if form.validate_on_submit():
        pass
        return redirect(url_for('users.users_index'))

    return render_template('users/create-user.html')
