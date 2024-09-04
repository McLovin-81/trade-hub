
"""
This module handles database connections and operations.

Functions:
    - get_db: Retrieves a database connection from the Flask application context.
    - close_db: Closes the database connection.
    - init_db: Initializes the database schema from schema.sql.
    - setup_database: Sets up the database configuration and initializes it if necessary.
"""

import os
import sqlite3
import click
from flask import current_app, g


def get_db():
    """
    Retrieve a database connection from the Flask application context.

    Returns:
        sqlite3.Connection: The database connection object.
    """
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row
    
    return g.db


def close_db(e=None):
    """
    Close the database connection if it exists.
    
    Args:
        e (Exception, optional): Exception instance for handling teardown.
    """
    db = g.pop('db', None)

    if db is not None:
        db.close()


def init_db():
    """
    Initialize the database.
    """
    db = get_db()
    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))


def setup_database(app):
    """
    Set up the database configuration and initialize it if necessary.

    Args:
        app (Flask): The Flask application instance.
    """
    app.config['DATABASE'] = os.path.join(app.instance_path, 'trade_hub_database.sqlite')
    
    # Ensure the instance folder exists
    os.makedirs(app.instance_path, exist_ok=True)
    
    # Initialize the database if it does not exist
    if not os.path.exists(app.config['DATABASE']):
        with app.app_context():
            print("Database does not exist, initializing...")
            init_db()
            print("Database initialized.")
    else:
        print("Database already exists.")
