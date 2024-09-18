
from flask import Blueprint, g, redirect, render_template, request, session, url_for, jsonify
from flask_login import login_required, current_user
from ..database.db import get_db
from ..database.user_db_requests import get_user_transactions, process_transactions,buy_sell_stock, get_user_balance, get_ranking, calculate_total_profit, get_transaction_history
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
    depot_data = process_transactions(get_user_transactions(username, db))
    #buy_sell_stock(current_user.username, "AIR.DE", 2,"sell", db)
    print(get_ranking(db))
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
    
    #db = get_db()

    # Fetch user's account balance
    #account = get_user_balance(current_user.username, db)

    #if account is None:
    #    return jsonify({'error': 'Account not found'}), 404

    
    
    return render_template('depot/order-manager.html', )
