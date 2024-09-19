
"""
This module contains the route handlers for rendering HTML templates.
"""

from flask import (
    Blueprint, redirect, render_template,
    request, url_for
)
from app.utilities.news_utils import get_products, get_stock_news
from app.database.db import get_db
from app.database.user_db_requests import get_ranking


bp = Blueprint('home_page', __name__)


@bp.route('/', endpoint='index')
def index():
    """
    Handle GET requests to / and render the index.html template.

    Returns:
        Response: Rendered HTML template for the index page.
    """
    db = get_db()
    ranking_list = get_ranking(db)
    
    return render_template('index.html', ranking_list=ranking_list)




@bp.route('/legend')
def legend():
    return render_template('legend.html')


@bp.route('/news', endpoint='news')
def news():
    news_data = get_stock_news(get_products())
    
    return render_template('news.html', news_data=news_data)

@bp.route('/wiki', endpoint='wiki')
def wiki():
    
    
    return render_template('wiki.html')
