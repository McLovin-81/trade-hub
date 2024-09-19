from flask import Blueprint, redirect, render_template, request, session, url_for, jsonify
from flask_login import login_required, current_user
from ..database.user_db_requests import set_useraccount_to_reset, delete_account
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
@bp.route('/api/reset-account', methods=['POST'])
@login_required
def reset_account():
    username = current_user.username  # Use the current_user to get the logged-in user's username

    db = get_db()
    set_useraccount_to_reset(username, db)
    
    return jsonify({'message': 'Account reset successfully. The admin has received your reset request.'}), 200


@bp.route('/api/delete-account', methods=['POST'])
@login_required
def delete_account_route():
    username = current_user.username  # Get the logged-in user's username

    try:
        db = get_db()
        delete_account(username, db)  # Delete the account from the database

        # Log the user out after account deletion
        session.clear()  # Clear the session (Flask-Login handles this)
        return jsonify({'message': 'Account deleted successfully.'}), 200
    except Exception as e:
        print(f"Error deleting account: {e}")
        return jsonify({'error': 'Failed to delete account.'}), 500