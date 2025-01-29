from flask import render_template, request, flash, redirect, url_for
from flask_security import login_required, url_for_security
from sqlalchemy import select
from shared.database import db_session
from backend.app.users import bp
from backend.models.user import User
from backend.app.users.forms import UpdateUserForm
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


@bp.route('/edit-user/<string:fs_uniquifier>', methods=["GET", "POST"])
@login_required
def edit_user(fs_uniquifier):
    user = db_session.query(User).filter(User.fs_uniquifier == fs_uniquifier).first()

    if not user:
        flash('User not found', 'error')
        return redirect(url_for('users.user_index'))

    form = UpdateUserForm(obj=user)

    if form.validate_on_submit():
        user.firstname = form.firstname.data
        user.lastname = form.lastname.data

        db_session.commit()
        flash(f'User {user.firstname} {user.lastname} updated successfully', 'success')
        return redirect(url_for('users.users_index'))

    return render_template("users/edit_user.html", user=user, form=form, is_editable=True)


@bp.route('/profile/<string:fs_uniquifier>', methods=["GET"])
@login_required
def load_user_profile_by_id(fs_uniquifier):
    fetch_user_by_id = db_session.query(User).filter(User.fs_uniquifier == fs_uniquifier).first()

    return render_template("users/profile.html", user=fetch_user_by_id)
