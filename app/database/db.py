
"""
This module handles database connections and operations.

Functions:
    - get_db: Retrieves a database connection from the Flask application context.
    - close_db: Closes the database connection.
    - init_db: Initializes the database schema from schema.sql.
    - setup_database: Sets up the database configuration and initializes it if necessary.
"""

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
    Initialize the database by executing the schema file.

    This function retrieves the current database connection using the `get_db()` 
    function, then reads and executes the SQL schema from the file `schema.sql`. 
    The schema file defines the structure of the database, such as tables, 
    indexes, and any initial setup required.

    The SQL schema file is located in the 'database' directory within the 
    current application's context. The file is opened using the `open_resource()` 
    method provided by Flask's `current_app`, ensuring the file is read 
    as part of the application's package.

    The SQL script is executed using `db.executescript()`, which runs multiple 
    SQL commands in a single execution. The contents of the schema file are 
    decoded from UTF-8 to ensure proper handling of special characters.

    This function is typically called when setting up or resetting the 
    application's database.
    """
    db = get_db()
    with current_app.open_resource('database/schema.sql') as f:
        db.executescript(f.read().decode('utf8'))


@click.command('init-db')
def init_db_command():
    #Clear the existing data and create new tables.
    init_db()
    click.echo('Initialized the database.')
