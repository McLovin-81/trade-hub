from flask import Blueprint, render_template, request, session, jsonify, redirect, url_for
from flask_login import login_required, current_user
from app.database.db import get_db
from app.database.user_db_requests import admin_worklist, reset_account


bp = Blueprint('admin', __name__, url_prefix='/user')


@bp.route('/<username>/admin', methods=['GET', 'POST'] )
@login_required
def admin(username):
    db = get_db()
    admin_table = admin_worklist(db)
    # Ensure the logged-in user can only view their own depot
    if username != current_user.username:
        return jsonify({'error': 'Unauthorized access'}), 403  # Unauthorized access
    
    return render_template('admin/admin.html', admin_table=admin_table)


@bp.route('/reset_account/', methods=['POST'])
@login_required 
def reset_account_route():
    username = request.form.get('username')
    print(username)
    db = get_db()
    reset_account(username, db)  # Aufruf der Funktion zum Zurücksetzen des Kontos
    return redirect(url_for('admin.admin', username=current_user.username))
        