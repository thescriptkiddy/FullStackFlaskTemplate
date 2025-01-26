from flask import current_app, url_for, jsonify
from sqlalchemy import select
from werkzeug.routing import BuildError
from urllib.parse import unquote
import os
from bs4 import BeautifulSoup
from backend.models.menu import Link
from shared.database import db_session
from backend.utils.helper import handle_sql_exceptions


def get_template_title(template_name):
    template_folder = current_app.config['TEMPLATE_FOLDER']

    for root, dirs, files in os.walk(template_folder):
        if template_name in files:
            template_path = os.path.join(root, template_name)
            with open(template_path, 'r') as file:
                content = file.read()
                soup = BeautifulSoup(content, 'html.parser')
                h1_tag = soup.find('h1')
                return h1_tag.text if h1_tag else None

    return None


def generate_route_map(include_params=False):
    routes = []
    for rule in current_app.url_map.iter_rules():
        if "GET" in rule.methods and (include_params or len(rule.defaults or ()) >= len(rule.arguments or ())):
            try:
                url = url_for(rule.endpoint, **{arg: f"<{arg}>" for arg in rule.arguments})
                template_name = f"{rule.endpoint}.html"
                title = get_template_title(template_name)
                routes.append({
                    'url': unquote(url),
                    'endpoint': rule.endpoint,
                    'methods': list(rule.methods),
                    'defaults': rule.defaults,
                    'title': title
                })
            except BuildError as e:
                current_app.logger.warning(f"Could not build URL for {rule.endpoint}: {str(e)}")
    return routes


def get_all_menu_links():
    """Endpoint offers a list of url-links registered in the app"""
    return [url for url in db_session.execute(select(Link.url)).scalars().all()]


@handle_sql_exceptions
def save_all_menu_links_to_database():
    """Persists urls to the database based on flasks routing information"""
    # Generate a list of links based on flasks routing
    links_based_on_routing = set([f"{current_app.config['BASE_URL']}{route['url']}" for route in generate_route_map()])
    # Verifies that routing information (link strings) are available
    if not links_based_on_routing:
        return jsonify({"error": "Cannot compare due to missing routing information"}), 400
    # Fetch all links from database
    persisted_links = set([url for url in db_session.execute(select(Link.url)).scalars().all()])
    # Create a list of missing links
    missing_links = list({url for url in links_based_on_routing if url not in persisted_links})
    # Save missing links to database
    if missing_links:
        for new_link in missing_links:
            new_link = Link(
                name=new_link,
                url=new_link
            )
            db_session.add(new_link)
        db_session.commit()
        return jsonify({
            "message": f"{len(missing_links)} new links saved successfully",
            "new_links": missing_links,
            "all_links": list(links_based_on_routing)
        }), 200

    return jsonify({"message": "No new links found", "all_links": list(links_based_on_routing)}), 200
