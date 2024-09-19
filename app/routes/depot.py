
from flask import Blueprint, g, redirect, render_template, request, session, url_for, jsonify
from flask_login import login_required, current_user
from ..database.db import get_db
from ..database.user_db_requests import get_user_transactions, process_transactions, buy_sell_stock, get_user_balance, get_ranking, calculate_total_profit, get_transaction_history, get_stock_symbols
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
    user_balance = get_user_balance(username, db).format('%.2f')

    # Process user's transactions to get depot data
    depot_data = process_transactions(get_user_transactions(username, db))
    return render_template('depot/depot.html', balance=user_balance, depot = depot_data)


@bp.route('/<username>/transactions')
@login_required
def user_transactions(username):
    # Ensure the logged-in user can only view their own depot
    if username != current_user.username:
        return jsonify({'error': 'Unauthorized access'}), 403  # Unauthorized access
    
    db = get_db()

    transaction_history = get_transaction_history(username, db)
    return render_template('depot/transactions.html', transaction_history = transaction_history)


@bp.route('/<username>/ordermanagement')
@login_required
def ordermanagement(username):
    # Ensure the logged-in user can only view their own depot
    if username != current_user.username:
        return jsonify({'error': 'Unauthorized access'}), 403  # Unauthorized access
    

    db = get_db()
    # Fetch user's account balance
    user_balance = get_user_balance(username, db).format('%.2f')
    # Process user's transactions to get depot data
    depot_data = process_transactions(get_user_transactions(username, db))
    
    return render_template('depot/order-manager.html', balance=user_balance, depot = depot_data)







@bp.route('/api/stocks', methods=['GET'])
def api_get_stocks():
    query = request.args.get('query', '')
    if query:
        db = get_db()
        symbols = get_stock_symbols(query, db)
        return jsonify({'symbols': symbols})
    return jsonify({'symbols': []})



@bp.route('/api/stock-price', methods=['GET'])
def get_stock_price():
    symbol = request.args.get('symbol')
    if symbol:
        stock_info = get_stock_info(symbol)
        return jsonify(stock_info)
    return jsonify({'error': 'Invalid symbol'}), 400


@bp.route('/api/buy-stock', methods=['POST'])  # Ensure 'POST' is included here
@login_required
def api_buy_stock():
    data = request.get_json()
    stock_symbol = data.get("symbol")
    quantity = data.get("quantity")
    order_type = data.get("orderType")

    db = get_db()

    success = buy_sell_stock(current_user.username, stock_symbol, quantity, order_type, db)

    if success:
        return jsonify({'success': True}), 200
    else:
        return jsonify({'success': False, 'message': 'Insufficient balance or stock not available'}), 400