"""
This module initializes the Flask application and registers all the routes and APIs.

It contains the factory function `create_app` which sets up the Flask application instance,
configures it, and registers the necessary routes and API endpoints.

Modules:
    routes (module): Contains the route handlers for HTML pages.
    api (module): Contains the API endpoint handlers.
"""

from flask import Flask
from app.routes import *
from app.api import *

def create_app():
    """
    Factory function to create and configure the Flask application.

    This function initializes a Flask application, registers HTML routes and API endpoints,
    and returns the Flask app instance. It follows the application factory pattern, which
    allows for better organization and flexibility, particularly useful for larger
    applications or when testing.

    Returns:
        Flask: The Flask application instance configured with routes and APIs.
    """
    app = Flask(__name__)

    # Register routes for HTML pages
    app.add_url_rule('/', 'index', index)
    app.add_url_rule('/legend', 'legend', legend)

    # Register API endpoints
    app.add_url_rule('/api/data', 'get_data', get_data, methods=['GET'])
    app.add_url_rule('/api/data', 'receive_data', receive_data, methods=['POST'])

    return app
