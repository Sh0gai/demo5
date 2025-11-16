from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.db_connect import get_db
from app.blueprints.auth import login_required

orders = Blueprint('orders', __name__)

@orders.route('/', methods=['GET', 'POST'])
@login_required
def show_orders():
    db = get_db()
    cursor = db.cursor()

    # Handle POST request to add a new order
    if request.method == 'POST':
        customer_id = request.form['customer_id']

        # Insert the new order
        cursor.execute('INSERT INTO `order` (customer_id) VALUES (%s)', (customer_id,))
        db.commit()

        flash('New order created successfully!', 'success')
        return redirect(url_for('orders.show_orders'))

    # Get all orders with customer information
    cursor.execute('''
        SELECT o.order_id, o.customer_id, o.date, c.name as customer_name, c.phone, c.email
        FROM `order` o
        JOIN customer c ON o.customer_id = c.customer_id
        ORDER BY o.date DESC
    ''')
    all_orders = cursor.fetchall()

    # Get order details for each order with totals
    order_details = {}
    order_totals = {}
    for order in all_orders:
        cursor.execute('''
            SELECT od.order_detail_id, od.pizza_id, od.quantity,
                   p.name as pizza_name, p.size, p.price,
                   (od.quantity * p.price) as subtotal
            FROM order_detail od
            JOIN pizza p ON od.pizza_id = p.pizza_id
            WHERE od.order_id = %s
        ''', (order['order_id'],))
        order_details[order['order_id']] = cursor.fetchall()

        # Calculate total with tax for this order
        subtotal = sum(detail['subtotal'] for detail in order_details[order['order_id']])
        tax = float(subtotal) * 0.07
        total = float(subtotal) + tax
        order_totals[order['order_id']] = {
            'subtotal': float(subtotal),
            'tax': tax,
            'total': total
        }

    # Get all customers for dropdown
    cursor.execute('SELECT customer_id, name, phone FROM customer ORDER BY name')
    all_customers = cursor.fetchall()

    # Get all pizzas for dropdown
    cursor.execute('SELECT pizza_id, name, size, price FROM pizza ORDER BY name, size')
    all_pizzas = cursor.fetchall()

    return render_template('orders.html',
                         all_orders=all_orders,
                         order_details=order_details,
                         order_totals=order_totals,
                         all_customers=all_customers,
                         all_pizzas=all_pizzas)

@orders.route('/update_order/<int:order_id>', methods=['POST'])
@login_required
def update_order(order_id):
    db = get_db()
    cursor = db.cursor()

    # Update the order's customer
    customer_id = request.form['customer_id']

    cursor.execute('UPDATE `order` SET customer_id = %s WHERE order_id = %s',
                   (customer_id, order_id))
    db.commit()

    flash('Order updated successfully!', 'success')
    return redirect(url_for('orders.show_orders'))

@orders.route('/delete_order/<int:order_id>', methods=['POST'])
@login_required
def delete_order(order_id):
    db = get_db()
    cursor = db.cursor()

    # Delete the order (order_details will be cascade deleted)
    cursor.execute('DELETE FROM `order` WHERE order_id = %s', (order_id,))
    db.commit()

    flash('Order deleted successfully!', 'danger')
    return redirect(url_for('orders.show_orders'))

@orders.route('/add_order_detail/<int:order_id>', methods=['POST'])
@login_required
def add_order_detail(order_id):
    db = get_db()
    cursor = db.cursor()

    pizza_id = request.form['pizza_id']
    quantity = request.form['quantity']

    # Check if this pizza is already in the order
    cursor.execute('SELECT order_detail_id FROM order_detail WHERE order_id = %s AND pizza_id = %s',
                   (order_id, pizza_id))
    existing = cursor.fetchone()

    if existing:
        # Update quantity if already exists
        cursor.execute('UPDATE order_detail SET quantity = quantity + %s WHERE order_detail_id = %s',
                       (quantity, existing['order_detail_id']))
        flash('Updated quantity for existing pizza in order!', 'info')
    else:
        # Insert new order detail
        cursor.execute('INSERT INTO order_detail (order_id, pizza_id, quantity) VALUES (%s, %s, %s)',
                       (order_id, pizza_id, quantity))
        flash('Pizza added to order successfully!', 'success')

    db.commit()
    return redirect(url_for('orders.show_orders'))

@orders.route('/update_order_detail/<int:order_detail_id>', methods=['POST'])
@login_required
def update_order_detail(order_detail_id):
    db = get_db()
    cursor = db.cursor()

    quantity = request.form['quantity']

    cursor.execute('UPDATE order_detail SET quantity = %s WHERE order_detail_id = %s',
                   (quantity, order_detail_id))
    db.commit()

    flash('Order item updated successfully!', 'success')
    return redirect(url_for('orders.show_orders'))

@orders.route('/delete_order_detail/<int:order_detail_id>', methods=['POST'])
@login_required
def delete_order_detail(order_detail_id):
    db = get_db()
    cursor = db.cursor()

    # Delete the order detail
    cursor.execute('DELETE FROM order_detail WHERE order_detail_id = %s', (order_detail_id,))
    db.commit()

    flash('Item removed from order!', 'warning')
    return redirect(url_for('orders.show_orders'))
