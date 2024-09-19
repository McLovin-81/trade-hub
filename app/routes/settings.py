from flask import Blueprint, redirect, render_template, request, session, url_for, jsonify
from flask_login import login_required, current_user
from ..database.user_db_requests import set_useraccount_to_reset
from ..database.db import get_db


bp = Blueprint('settings', __name__, url_prefix='/user')


@bp.route('/<username>/settings')
@login_required
def settings(username):
    # Ensure the logged-in user can only view their own settings
    if username != current_user.username:
        return jsonify({'error': 'Unauthorized access'}), 403

    return render_template('settings/settings.html')


# New route for resetting the user account
@bp.route('/<username>/reset-account', methods=['POST'])
@login_required
def reset_account(username):
    if username != current_user.username:
        return jsonify({'error': 'Unauthorized access'}), 403

    db = get_db()
    set_useraccount_to_reset(username, db)
    
    return jsonify({'message': 'Account reset successfully'}), 200