
# User authentication routes
# https://flask.palletsprojects.com/en/3.0.x/tutorial/views/

import functools
from flask import (
    Blueprint, flash, g, redirect, render_template,
    request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
from ..database.db import get_db


bp = Blueprint('auth', __name__, url_prefix='/auth')

"""
@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        db = get_db()
        error = None

        # Make checks

        if error is None:
            try:
                db.execute(
                    "INSERT INTO user (username, email,  password) VALUES (?, ?, ?)",
                    (username, email, generate_password_hash(password)),
                )
                db.commit()
            except db.IntegrityError:
                error = f"User {username} is already registered."
            else:
                return redirect(url_for('auth.login'))
        
        flash(error)
            
    return render_template('auth/register.html')
"""
@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        data = request.json  # Access the JSON payload
        print(f"Received data: {data}")  # Debugging
        username = data.get('name')
        email = data.get('email')
        password = data.get('password')

        db = get_db()
        error = None

        # Perform checks
        if not username or not email or not password:
            error = 'All fields are required.'

        if error is None:
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
            else:
                # send ok before redirect
                return redirect(url_for('auth.login'))
        
        flash(error)

    return render_template('auth/register.html')


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None

        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone()

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('index'))

        flash(error)

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
