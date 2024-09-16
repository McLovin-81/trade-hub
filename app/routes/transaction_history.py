from flask import Blueprint, g, redirect, render_template, request, session, url_for, jsonify
from flask_login import login_required, current_user
from ..database.db import get_db
from ..database.user_db_requests import get_transaction_history



bp = Blueprint('transactions', __name__, url_prefix='/user')


@bp.route('/<username>/transactions')
@login_required
def user_transactions(username):
    # Ensure the logged-in user can only view their own depot
    if username != current_user.username:
        return jsonify({'error': 'Unauthorized access'}), 403  # Unauthorized access
    
    db = get_db()

    transaction_history = get_transaction_history(username, db)
    #NEED RENDER TEMPLATE
    return render_template('', transaction_list = transaction_history)