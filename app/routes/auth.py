
# User authentication routes
# https://flask.palletsprojects.com/en/3.0.x/tutorial/views/

from functools import wraps
from flask import Blueprint, g, redirect, render_template, request, session, url_for, jsonify
from flask_login import LoginManager, login_required, login_user, logout_user, current_user, UserMixin
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

        print(f"User {user['username']} logged in")
        return jsonify({'message': 'Login successful', 'redirect': f'/user/{username}/depot'}), 200

    return render_template('auth/login.html')





@bp.route('/profile')
@login_required
def profile():
    return render_template('profile.html')


@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


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


"""
1. Flask-Login Integration

	•	Flask-Login is used to manage user sessions. This extension provides functions to log users in, track their session, and ensure that only authenticated users can access specific routes.
	•	User Class:
	•	You use a User class (which inherits from UserMixin provided by Flask-Login) that contains the user’s ID and username.
	•	The UserMixin class provides default implementations for methods like is_authenticated and get_id().
	•	Session Tracking:
	•	Flask-Login keeps track of the logged-in user by storing their ID in the session cookie. This cookie is encrypted using the SECRET_KEY in your Flask app configuration.
	•	When the user logs in, their user ID is stored in the session.

2. Login Process

	•	User Login:
	•	In the /login route, you accept the user’s credentials (username and password),
            verify them by querying the database,
            and if the credentials are valid, Flask-Login logs the user in using: login_user(user_obj)
	•	Once logged in, the user ID is stored in the session, allowing Flask-Login
            to recognize the user across different requests.

3. Session Retrieval

	•	Session-Based User Retrieval:
	    •	Each time a user accesses a route, Flask-Login retrieves the user from the session using the user_loader function:
        •	Flask-Login automatically checks the session cookie and loads the corresponding user from the database if the user is logged in.

    •	Current User Context!!!!!!!!:
	    •	Flask provides a global object current_user which gives you access to
            the user currently logged into the session. This is accessible throughout the application:


Summary Flow

	1.	User logs in → Flask-Login verifies credentials, creates a session by storing user ID in a cookie.
	2.	User navigates the app → On each request, Flask-Login retrieves the user from the session cookie and loads the user context.
	3.	User accesses protected routes → Routes requiring authentication are protected with @login_required.
	4.	User logs out → Session is cleared, and the user is redirected to the login page.
"""