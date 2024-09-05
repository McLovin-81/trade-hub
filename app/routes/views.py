
"""
This module contains the route handlers for rendering HTML templates.

Routes:
    - GET /: Renders the index.html template.
    - GET /legend: Renders the legend.html template.
"""

from flask import render_template, request, redirect, url_for
from app.graph_utilities.graph_utils import *


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

def main():
    return render_template('main.html')

def detailPage():
    symbol = request.form.get('symbol')
    print(get_stock_info(symbol))
    graph_info = get_graph_info(symbol) 
    graph_html = create_stock_graph(*graph_info)
    
    return render_template('stockWindow.html', symbol=symbol, graph_html=graph_html)