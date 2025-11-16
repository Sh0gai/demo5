from flask import render_template, redirect, url_for, session, request, flash
from . import app
from app.db_connect import get_db
from app.blueprints.auth import login_required

@app.route('/', methods=['GET', 'POST'])
def index():
    # If user is logged in, redirect to dashboard
    if 'user_id' in session:
        return redirect(url_for('dashboard'))

    # Handle login POST request
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        db = get_db()
        cursor = db.cursor()

        # Query employee by username
        cursor.execute('SELECT * FROM employee WHERE username = %s', (username,))
        employee = cursor.fetchone()

        # Check if employee exists and password matches
        if employee and employee['password'] == password:
            # Store user info in session
            session['user_id'] = employee['user_id']
            session['username'] = employee['username']
            session['fname'] = employee['fname']
            session['lname'] = employee['lname']

            flash(f'Welcome back, {employee["fname"]}!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password. Please try again.', 'danger')
            return redirect(url_for('index'))

    # Show login form
    return render_template('index.html')

@app.route('/dashboard')
@login_required
def dashboard():
    db = get_db()
    cursor = db.cursor()

    # Get total counts
    cursor.execute('SELECT COUNT(*) as count FROM pizza')
    total_pizzas = cursor.fetchone()['count']

    cursor.execute('SELECT COUNT(*) as count FROM customer')
    total_customers = cursor.fetchone()['count']

    cursor.execute('SELECT COUNT(*) as count FROM `order`')
    total_orders = cursor.fetchone()['count']

    # Get total revenue for current year (2025)
    cursor.execute('''
        SELECT COALESCE(SUM(od.quantity * p.price), 0) as revenue
        FROM order_detail od
        JOIN pizza p ON od.pizza_id = p.pizza_id
        JOIN `order` o ON od.order_id = o.order_id
        WHERE YEAR(o.date) = 2025
    ''')
    total_revenue_year = cursor.fetchone()['revenue']

    # Get all-time total revenue
    cursor.execute('''
        SELECT COALESCE(SUM(od.quantity * p.price), 0) as revenue
        FROM order_detail od
        JOIN pizza p ON od.pizza_id = p.pizza_id
    ''')
    total_revenue_all_time = cursor.fetchone()['revenue']

    # Get recent orders (last 5)
    cursor.execute('''
        SELECT o.order_id, o.date, c.name as customer_name,
               COALESCE(SUM(od.quantity * p.price), 0) as total
        FROM `order` o
        JOIN customer c ON o.customer_id = c.customer_id
        LEFT JOIN order_detail od ON o.order_id = od.order_id
        LEFT JOIN pizza p ON od.pizza_id = p.pizza_id
        GROUP BY o.order_id, o.date, c.name
        ORDER BY o.date DESC
        LIMIT 5
    ''')
    recent_orders = cursor.fetchall()

    # Get top pizzas
    cursor.execute('''
        SELECT p.name, p.size, COUNT(od.order_detail_id) as order_count
        FROM pizza p
        LEFT JOIN order_detail od ON p.pizza_id = od.pizza_id
        GROUP BY p.pizza_id, p.name, p.size
        HAVING order_count > 0
        ORDER BY order_count DESC
        LIMIT 5
    ''')
    top_pizzas = cursor.fetchall()

    return render_template('dashboard.html',
                         total_pizzas=total_pizzas,
                         total_customers=total_customers,
                         total_orders=total_orders,
                         total_revenue_year=total_revenue_year,
                         total_revenue_all_time=total_revenue_all_time,
                         recent_orders=recent_orders,
                         top_pizzas=top_pizzas)

@app.route('/profile')
@login_required
def profile():
    db = get_db()
    cursor = db.cursor()

    user_id = session.get('user_id')

    # Get employee information
    cursor.execute('SELECT * FROM employee WHERE user_id = %s', (user_id,))
    employee = cursor.fetchone()

    # Get employee's activity stats
    cursor.execute('''
        SELECT COUNT(*) as total_orders_created
        FROM `order`
        WHERE DATE(date) >= DATE_SUB(CURDATE(), INTERVAL 30 DAY)
    ''')
    recent_activity = cursor.fetchone()

    return render_template('profile.html',
                         employee=employee,
                         recent_activity=recent_activity)

@app.route('/about')
def about():
    return render_template('about.html')
