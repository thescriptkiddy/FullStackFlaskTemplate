from flask import jsonify, render_template, current_app
from sqlalchemy.exc import DataError, IntegrityError, OperationalError, SQLAlchemyError
import logging
from functools import wraps


def handle_sql_exceptions(func):
    """Decorator to handle common SQL Exceptions """

    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as err:
            logging.error("Value error: %s", err)
            return jsonify({"status": "error", "message": str(err)}), 400
        except DataError as err:
            logging.error("Incorrect data: %s", err)
            return jsonify({"status": "error", "message": "Incorrect data"}), 400
        except IntegrityError as err:
            logging.error("Duplicate entry: %s", err)
            return jsonify({"status": "error", "message": "Duplicate entry"}), 400
        except OperationalError as err:
            logging.error("Query failed due to lock/dead lock issues: %s", err)
            return jsonify({"status": "error", "message": "Database operation failed"}), 500
        except SQLAlchemyError as err:
            logging.error("Unexpected SQLAlchemy error: %s", err)
            return jsonify({"status": "error", "message": "An unexpected database error occurred"}), 500

    return wrapper


def register_error_handlers(app):
    @app.errorhandler(401)
    def unauthorized_error(error):
        return render_template('401_error.html'), 401

    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('404_error.html'), 404


def load_user(user_id):
    from shared.extensions import user_datastore
    print(f"Attempting to load user with id: {user_id}")
    user = user_datastore.find_user(fs_uniquifier=user_id)
    print(f"User found: {user}")
    return user
