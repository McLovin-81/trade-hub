
"""
This module initializes the Flask application and registers all the routes and APIs.

It contains the factory function `create_app` which sets up the Flask application instance,
configures it, and registers the necessary routes and API endpoints.

The __init__.py serves double duty:
it will contain the application factory, and it tells Python that
the flaskr directory should be treated as a package.
"""
import os
from flask import Flask
from app.routes.views import *
from app.api.endpoints import *
from app.database.db import *
from app.graph_utilities import *

def create_app(test_config=None):
    """
    Factory function to create and configure the Flask application.

    This function initializes a Flask application, registers HTML routes and API endpoints,
    and returns the Flask app instance. It follows the application factory pattern, which
    allows for better organization and flexibility, particularly useful for larger
    applications or when testing.

    Note:
        Any configuration, registration, and other setup the application
        needs will happen inside the function.

    Returns:
        Flask: The Flask application instance configured with routes and APIs.
    """
    app = Flask(__name__) # -> thats my WSGI

    # Register routes for HTML pages
    app.add_url_rule('/', 'index', index)
    app.add_url_rule('/legend', 'legend', legend)
    app.add_url_rule('/register', 'register', register)
    app.add_url_rule('/main', 'main', main)

    # Register API endpoints
    app.add_url_rule('/register/save_name', 'save_name', save_name, methods=['POST'])
    app.add_url_rule('/detailPage', 'details', detailPage, methods = ['GET','POST'])
    # Set up the database
    setup_database(app)

    # Register database functions
    app.teardown_appcontext(close_db)

    return app
