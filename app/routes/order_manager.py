from flask import Blueprint, g, redirect, render_template, request, session, url_for, jsonify
from flask_login import login_required, current_user
from ..database.db import get_db
from ..database.user_db_requests import get_user_transactions, process_transactions, get_user_balance, get_ranking

bp = Blueprint('ordermanagement', __name__, url_prefix='/user')

@bp.route('/<username>/ordermanagement')
@login_required
def ordermanagement(username):
    # Ensure the logged-in user can only view their own depot
    if username != current_user.username:
        return jsonify({'error': 'Unauthorized access'}), 403  # Unauthorized access
    
    db = get_db()

    # Fetch user's account balance
    account = get_user_balance(current_user.username)

    if account is None:
        return jsonify({'error': 'Account not found'}), 404

    get_ranking(db)
    
    return render_template('depot/depot.html', balance = account)
