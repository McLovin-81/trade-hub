
# User authentication routes
# https://flask.palletsprojects.com/en/3.0.x/tutorial/views/

from functools import wraps
from flask import Blueprint, g, redirect, render_template, request, url_for, jsonify, flash
from flask_login import login_required, login_user, logout_user, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from ..database.db import get_db
from ..models import User
import re


bp = Blueprint('auth', __name__, url_prefix='/auth')


def validate_user_registration_input(username, email, password):
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    if not re.match(email_regex, email):
        return 'Invalid email format'
    if len(password) < 8:
        return 'Password must be at least 8 characters long'
    return None


@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        data = request.get_json()  # Access the JSON payload
        if not data:
            return jsonify({'error: Invalid JSON format'}, 400)
        
        username = data.get('name')
        email = data.get('email')
        password = data.get('password')

        db = get_db()
        error = None

        # Validate user input
        error = validate_user_registration_input(username, email, password)
        if error:
            return jsonify({'error': error}), 400

        try:
            db.execute(
                "INSERT INTO user (username, email, password) VALUES (?, ?, ?)",
                (username, email, generate_password_hash(password)),
            )
            db.commit()

            user_id = db.execute('SELECT id FROM user WHERE username = ?', (username,)).fetchone()['id']
            # Create an account with an initial balance
            db.execute(
                "INSERT INTO account (user_id, balance) VALUES (?, ?)",
                (user_id, 1000.0)  # You can set an initial balance of 0 or any other value
            )
            db.commit()

        except db.IntegrityError as e:
            error = f"User {username} is already registered."
            print(f"Database error: {e}")
            return jsonify({'error': error}), 409
        
        else:
            # Return a success message as JSON
            return jsonify({'message': 'Registration successful', 'redirect': '/auth/login'}), 200

    return render_template('auth/register.html')


@bp.route('/login', methods=('GET', 'POST'))
def login():
    
    if request.method == 'POST':
        data = request.get_json()  # Access the JSON payload
        if not data:
            return jsonify({'error': 'Invalid JSON format'}), 400
    
        username = data.get('name')
        password = data.get('password')

        db = get_db()
        error = None

        # Query the user from the database by email
        user = db.execute(
            'SELECT * FROM user WHERE username = ?',
            (username,)
        ).fetchone()

        # Check if user exists
        if user is None:
            error = 'User not found'
            return jsonify({'error': error}), 401
        
        # Check if the password is correct
        if not check_password_hash(user['password'], password):
            error = 'Incorrect password'
            return jsonify({'error': error}), 401
        

        user_obj = User(user['id'], user['username'])
        login_user(user_obj)

        if user['isAdmin'] == True:
            return jsonify({'message': 'Login successful', 'redirect': f'/user/{username}/admin'}), 200

        print(f"User {user['username']} logged in")
        return jsonify({'message': 'Login successful', 'redirect': f'/user/{username}/depot'}), 200

    return render_template('auth/login.html')


@bp.route('/logout')
@login_required
def logout():
    logout_user()  # Logs out the current user
    return redirect(url_for('home_page.index'))


@bp.route('/profile')
@login_required
def profile():
    return render_template('profile.html')


@bp.before_app_request
def load_logged_in_user():
    if current_user.is_authenticated:
        g.user = current_user
    else:
        g.user = None








# Not needed
def login_required(view):
    @wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        return view(**kwargs)
    return wrapped_view
