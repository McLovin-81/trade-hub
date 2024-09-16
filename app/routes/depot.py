
from flask import Blueprint, g, redirect, render_template, request, session, url_for, jsonify
from flask_login import login_required, current_user
from ..database.db import get_db
from ..database.user_db_requests import get_user_transactions, process_transactions, buy_sell_stock, get_user_balance
from ..graph_utilities.graph_utils import get_stock_info


bp = Blueprint('depot', __name__, url_prefix='/user')


@bp.route('/<username>/depot')
@login_required
def depot(username):
    # Ensure the logged-in user can only view their own depot
    if username != current_user.username:
        return jsonify({'error': 'Unauthorized access'}), 403  # Unauthorized access
    
    db = get_db()

    user_balance = get_user_balance(username, db)
    user_depot = process_transactions(get_user_transactions(username, db))
    buy_sell_stock(current_user.username, "AAPL", 2,"buy", db)
    return render_template('depot/depot.html', depot = user_depot, balance = user_balance)
