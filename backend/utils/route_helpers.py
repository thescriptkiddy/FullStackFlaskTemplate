from flask import current_app, url_for


def has_no_empty_params(rule):
    """Used my generate_sitemaps to exclude routes with params"""
    defaults = rule.defaults if rule.defaults is not None else ()
    arguments = rule.arguments if rule.arguments is not None else ()

    return len(defaults) >= len(arguments)


# TODO Refactor to allow filtering yes or no
def generate_sitemap():
    """Generates a list of dictionaries with all existing urls and metadata such as url, endpoint, methods and
    defaults"""
    routes = []

    for rule in current_app.url_map.iter_rules():
        if "GET" in rule.methods and has_no_empty_params(rule):
            try:
                url = url_for(rule.endpoint, **(rule.defaults or {}))
                entry = {
                    'url': url,
                    'endpoint': rule.endpoint,
                    'methods': list(rule.methods),
                    'defaults': rule.defaults
                }
                routes.append(entry)
            except Exception as e:
                print("error}")
    return routes
