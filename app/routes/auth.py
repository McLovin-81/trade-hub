
# User authentication routes
# https://flask.palletsprojects.com/en/3.0.x/tutorial/views/

import functools
from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for, jsonify

from werkzeug.security import check_password_hash, generate_password_hash
from ..database.db import get_db
import logging
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

            # Log the user data for confirmation
            print(f"User {username} registered with email {email}")

        except db.IntegrityError as e:
            error = f"User {username} is already registered."
            print(f"Database error: {e}")
            return jsonify({'error': error}), 409
        
        else:
            # Return a success message as JSON
            return jsonify({}), 200

    return render_template('auth/register.html')


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        data = request.get_json()  # Access the JSON payload
        if not data:
            return jsonify({'error': 'Invalid JSON format'}), 400
    
        username = data.get('name')
        password = data.get('password')

        print(username, password)

        db = get_db()
        error = None

        # Query the user from the database by email
        user = db.execute(
            'SELECT * FROM user WHERE username = ?',
            (username,)
        ).fetchone()

        if user is None:
            error = 'User not found'
            return jsonify({'error': error}), 401
        
        # Check if the password is correct
        if not check_password_hash(user['password'], password):
            error = 'Incorrect password'
            return jsonify({'error': error}), 401
        
        # If login is successful, return a success message
        print(f"User {user['username']} logged")
        return jsonify({'message': 'Login successful'}), 200

    return render_template('auth/login.html')


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view
