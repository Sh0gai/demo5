from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from functools import wraps
from app.db_connect import get_db

auth = Blueprint('auth', __name__)

def login_required(f):
    """Decorator to require login for routes"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session or session.get('user_id') is None:
            session.clear()  # Clear any invalid session data
            flash('Please log in to access this page.', 'warning')
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function

@auth.route('/login')
def login():
    # Redirect to index page (which is now the login page)
    return redirect(url_for('index'))

@auth.route('/logout')
def logout():
    # Clear the session
    username = session.get('fname', 'User')
    session.clear()
    session.modified = True  # Ensure session is marked as modified
    flash(f'Goodbye, {username}! You have been logged out.', 'info')
    response = redirect(url_for('index'))
    # Additional cache control to prevent back button access
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

@auth.route('/register', methods=['GET', 'POST'])
def register():
    """Optional: Allow new employees to register"""
    if request.method == 'POST':
        fname = request.form['fname']
        lname = request.form['lname']
        username = request.form['username']
        password = request.form['password']

        db = get_db()
        cursor = db.cursor()

        # Check if username already exists
        cursor.execute('SELECT user_id FROM employee WHERE username = %s', (username,))
        if cursor.fetchone():
            flash('Username already exists. Please choose another.', 'danger')
            return redirect(url_for('auth.register'))

        # Insert new employee
        # NOTE: In production, hash the password before storing
        cursor.execute('INSERT INTO employee (fname, lname, username, password) VALUES (%s, %s, %s, %s)',
                       (fname, lname, username, password))
        db.commit()

        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('index'))

    return render_template('register.html')
