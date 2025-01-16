from pprint import pprint

from flask import current_app, url_for
from werkzeug.routing import BuildError
from urllib.parse import unquote


def has_no_empty_params(rule):
    """Used my generate_sitemaps to exclude routes with params"""
    defaults = rule.defaults if rule.defaults is not None else ()
    arguments = rule.arguments if rule.arguments is not None else ()

    return len(defaults) >= len(arguments)


# TODO Refactor to allow filtering yes or no
def generate_route_map(include_params=True):
    """Generates a list of dictionaries with all existing urls and metadata such as url, endpoint, methods and
    defaults"""
    routes = []

    for rule in current_app.url_map.iter_rules():
        if "GET" in rule.methods and (include_params or has_no_empty_params(rule)):
            try:
                url = url_for(rule.endpoint, **{arg: f"<{arg}>" for arg in rule.arguments})
                entry = {
                    'url': unquote(url),
                    'endpoint': rule.endpoint,
                    'methods': list(rule.methods),
                    'defaults': rule.defaults
                }
                routes.append(entry)
            except BuildError as e:
                print(f"Could not build URL for {rule.endpoint}: {str(e)}")
    
    return routes
