from flask import render_template
from flask_security import login_required
from sqlalchemy import select
from shared.database import db_session
from backend.app.users import bp
from backend.models.user import User


@bp.route('/')
@login_required
def users_index():
    result = db_session.execute(select(User))
    all_users = result.scalars().all()

    return render_template('users/index.html', all_users=all_users)


# Temporary route for testing. It transfers a complete user object

@bp.route('/profile/<string:fs_uniquifier>', methods=["GET"])
@login_required
def load_user_profile_by_id(fs_uniquifier):
    fetch_user_by_id = db_session.query(User).filter(User.fs_uniquifier == fs_uniquifier).first()

    return render_template("users/profile.html", user=fetch_user_by_id)
