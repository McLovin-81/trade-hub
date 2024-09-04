
"""
This module contains the route handlers for rendering HTML templates.

Routes:
    - GET /: Renders the index.html template.
    - GET /legend: Renders the legend.html template.
"""

from flask import render_template


def index():
    """
    Handle GET requests to / and render the index.html template.

    Returns:
        Response: Rendered HTML template for the index page.
    """
    return render_template('index.html')

def legend():
    """
    Handle GET requests to /legend and render the legend.html template.

    Returns:
        Response: Rendered HTML template for the legend page.
    """
    return render_template('legend.html')

def register():
    return render_template('register.html')
