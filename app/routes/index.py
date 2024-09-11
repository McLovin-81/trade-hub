
"""
This module contains the route handlers for rendering HTML templates.
"""

from flask import (
    Blueprint, redirect, render_template,
    request, url_for
)


bp = Blueprint('home_page', __name__)


@bp.route('/', endpoint='index')
def index():
    """
    Handle GET requests to / and render the index.html template.

    Returns:
        Response: Rendered HTML template for the index page.
    """
    return render_template('index.html')




@bp.route('/legend')
def legend():
    return render_template('legend.html')




