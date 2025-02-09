import logging
from uuid import UUID

from flask import render_template, url_for, current_app, request, jsonify, flash, redirect
from flask_security import login_required
from backend.app.menu import bp
from backend.app.menu.forms import CreateMenuForm, UpdateMenuForm, UpdateLinkForm
from backend.models.menu import Menu, Link
from backend.utils.route_helpers import get_all_menu_links, generate_route_map
from shared.extensions import db_session
from flask import flash, redirect, url_for, render_template, request
from sqlalchemy.orm.exc import NoResultFound
from backend.utils.route_helpers import nav_item


@bp.route('/')
@nav_item(title="Menu", order=1)
def index():
    menu_data = Menu.get_menu_data()

    return render_template("menu/index.html", menu_data=menu_data)


@bp.route('/edit-menu/<int:menu_id>', methods=["GET", "POST"])
@login_required
def update_menu(menu_id):
    try:
        menu = db_session.query(Menu).filter(Menu.id == menu_id).one()
    except NoResultFound:
        flash('Menu not found', 'error')
        return redirect(url_for('menu.index'))

    all_links = db_session.query(Link).all()
    edit_menu = UpdateMenuForm(obj=menu)
    edit_menu.links.choices = [(str(link.id), link.title) for link in all_links]

    if request.method == "POST" and edit_menu.validate_on_submit():
        try:
            # Update menu name
            menu.name = edit_menu.name.data

            # Get selected link IDs from form data
            selected_link_ids = edit_menu.links.data

            # Fetch Link objects based on selected IDs
            selected_links = db_session.query(Link).filter(Link.id.in_(selected_link_ids)).all()

            # Update menu links
            menu.links = selected_links

            # Commit changes
            db_session.commit()

            flash(f"{menu.name} successfully updated", 'success')
            return redirect(url_for('menu.index'))
        except Exception as e:
            db_session.rollback()
            flash(f"Error updating menu: {str(e)}", 'error')

    # For GET requests or if form validation fails
    edit_menu.links.data = [str(link.id) for link in menu.links]

    return render_template("menu/edit_menu.html", form=edit_menu, menu=menu, is_editable=True)


@bp.route('/create-menu', methods=["GET", "POST"])
@login_required
def create_menu():
    # Load menu links from database
    all_links = get_all_menu_links()
    # Initialize form and prepopulate links
    create_menu_form = CreateMenuForm(all_links=all_links)

    # Submit form data
    if request.method == "POST" and create_menu_form.validate_on_submit():
        print("Form submitted", create_menu_form.data)
        try:
            selected_links = db_session.query(Link).filter(Link.title.in_(create_menu_form.links.data)).all()

            if not selected_links:
                return jsonify({"error": "No valid links found for selection"}, 400)

            new_menu = Menu(
                name=create_menu_form.name.data,
                links=selected_links
            )
            db_session.add(new_menu)
            db_session.commit()

            # return jsonify({"message": "Menu created successfully"}), 200
            return redirect(url_for('menu.index'))

        except Exception as e:
            db_session.rollback()
            logging.error(f"Error creating menu: {e}")
            return jsonify({"error": str(e)}, 500)

    return render_template("menu/create_menu.html", create_menu_form=create_menu_form)


@bp.route('/edit-link/<int:link_id>', methods=["GET", "POST"])
def update_link(link_id):
    link = db_session.query(Link).filter(Link.id == link_id).first()

    if not link:
        flash("Link not found", "error")
        return redirect(url_for("menu.index"))

    form = UpdateLinkForm(obj=link)

    if form.validate_on_submit():
        if form.name.data != link.name:
            link.name = form.name.data
            db_session.commit()
            flash("Link successfully update", 'success')
        else:
            flash("No changes were made", 'info')
            return redirect(url_for('menu.index'))  # for testing

    return render_template("menu/edit_link.html", form=form, link=link, is_editable=True)


# todo Do i need the ui-route?
@bp.route('/delete-menu/<int:menu_id>', methods=["DELETE"])
def delete_menu(menu_id):
    Menu.delete_menu(menu_id)


@bp.route('/all-routes')
def all_routes():
    return generate_route_map()
