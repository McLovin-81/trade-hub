from flask import Blueprint, redirect, render_template, request, session, url_for, jsonify
from flask_login import login_required, current_user


bp = Blueprint('settings', __name__, url_prefix='/user')


@bp.route('/<username>/settings')
@login_required
def settings(username):
    # Ensure the logged-in user can only view their own depot
    if username != current_user.username:
        return jsonify({'error': 'Unauthorized access'}), 403  # Unauthorized access

    return render_template('settings/settings.html')