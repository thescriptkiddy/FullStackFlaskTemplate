from flask import render_template
from flask_security import login_required, url_for_security
from sqlalchemy import select
from shared.database import db_session
from backend.app.users import bp
from backend.models.user import User
from backend.app.auth.forms import ChangePasswordForm


@bp.route('/')
@login_required
def users_index():
    result = db_session.execute(select(User))
    all_users = result.scalars().all()

    return render_template('users/index.html', all_users=all_users)


# Only for testing the change form from flask security
@bp.route('/change-password')
@login_required
def change_password_by_user():
    form = ChangePasswordForm()

    return render_template("security/change_password.html", form=form)


@bp.route('/edit-profile/<string:fs_uniquifier>')
def edit_user_profile(fs_uniquifier):
    return render_template("user/edit_profile.html")


@bp.route('/profile/<string:fs_uniquifier>', methods=["GET"])
@login_required
def load_user_profile_by_id(fs_uniquifier):
    fetch_user_by_id = db_session.query(User).filter(User.fs_uniquifier == fs_uniquifier).first()

    return render_template("users/profile.html", user=fetch_user_by_id)
