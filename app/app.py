"""
This module serves as the entry point for running the Flask application.

It imports the `create_app` function from the `app` package's `__init__.py` file, 
initializes the Flask application, and starts the development server if the script 
is executed directly.

Modules:
    app (module): Contains the `create_app` function used to create the Flask app instance.
"""

from app import create_app

app = create_app()

if __name__ == '__main__':
    """
    If this script is executed directly, this block will run the Flask application.
    
    The app will be started in debug mode, which is useful for development, as it provides 
    interactive debugging and reloading on code changes.
    """
    app.run(debug=True)