
"""
This module initializes the Flask application and registers all the routes and APIs.

It contains the factory function `create_app` which sets up the Flask application instance,
configures it, and registers the necessary routes and API endpoints.

The __init__.py serves double duty:
it will contain the application factory, and it tells Python that
the flaskr directory should be treated as a package.
"""
import os
from flask import Flask, g
from flask_login import LoginManager

from .models import User
from .database import db
from .database.db import get_db
from .routes import auth, index, stock_details, depot, order_manager, ranking, transaction_history


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
    app = Flask(__name__, instance_relative_config=True) # -> Flask instance. Thats my WSGI.


    """
    app.config.from_mapping() sets some default configuration that
    the app will use:
        SECRET_KEY is used by Flask and extensions to keep data safe.
        Its set to 'dev' to provide a convenient value during development,
        but it should be overridden with a random value when deploying.
    """
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'trade_hub_database.sqlite'),
        )
    
    if test_config is None:
        # Load the instance config, if it exists, when not testing
        try:
            app.config.from_pyfile('config.py')
        except FileNotFoundError:
            print("Warning: 'config.py' not found. Using default settings.")
    else:
        # Load the test config if passed in
        app.config.from_mapping(test_config)
    
    # Ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

###################################################

    # Initialize Flask-Login
    login_manager = LoginManager()
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        db = get_db()
        user_row = db.execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()
        
        if user_row:
            # Create a User instance with the data from the database
            return User(id=user_row['id'], username=user_row['username'])
        return None


###################################################

    """ Register routes bp's """
    app.register_blueprint(index.bp)
    app.register_blueprint(auth.bp)
    app.register_blueprint(stock_details.bp)
    app.register_blueprint(depot.bp)
    app.register_blueprint(order_manager.bp)
    app.register_blueprint(ranking.bp)
    app.register_blueprint(transaction_history.bp)
    
    """ Call the registration from db.py """
    db.init_app(app)


    return app
