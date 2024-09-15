
from flask import Blueprint, g, redirect, render_template, request, session, url_for, jsonify
from flask_login import login_required, current_user
from ..database.db import get_db
from ..database.user_db_requests import get_user_transactions, process_transactions, buy_sell_stock
from ..graph_utilities.graph_utils import get_stock_info


bp = Blueprint('depot', __name__, url_prefix='/user')


@bp.route('/<username>/depot')
@login_required
def depot(username):
    # Ensure the logged-in user can only view their own depot
    if username != current_user.username:
        return jsonify({'error': 'Unauthorized access'}), 403  # Unauthorized access
    
    db = get_db()

    # Fetch user's account balance
    account = db.execute(
        'SELECT balance FROM account WHERE user_id = ?',
        (current_user.id,)
    ).fetchone()

    if account is None:
        return jsonify({'error': 'Account not found'}), 404

    # Fetch user's stocks/transaction history
    transactions = db.execute(
        '''
        SELECT th.symbol, p.name, SUM(th.quantity) AS total_quantity, th.price
        FROM transactionHistory th
        JOIN product p ON th.symbol = p.symbol
        WHERE th.user_id = ?
        GROUP BY th.symbol, p.name, th.price
        ''', 
        (current_user.id,)
    ).fetchall()

    # Prepare response data
    user_depot = {
        'balance': account['balance'],
        'stocks': [{'symbol': row['symbol'], 'name': row['name'], 'quantity': row['total_quantity'], 'price': row['price']} for row in transactions]
    }
    depot_data = process_transactions(get_user_transactions(username, db))
    buy_sell_stock(current_user.username, "AAPL", 2,"sell", db)
    return render_template('depot/depot.html', depot=user_depot, depot_data = depot_data)
