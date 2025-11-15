import mysql.connector
import re

config = {
    'host': 'd6q8diwwdmy5c9k9.cbetxkdyhwsb.us-east-1.rds.amazonaws.com',
    'user': 'r9bv9jybh4nyuy74',
    'password': 'nmeu7f3vr3cs2rz3',
    'database': 'mcc9bzsbx4u6p0gz',
    'port': 3306
}

try:
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()

    # Read seed_data.sql
    with open('database/seed_data.sql', 'r', encoding='utf-8') as f:
        seed_sql = f.read()

    # Remove comments
    seed_sql = re.sub(r'--.*$', '', seed_sql, flags=re.MULTILINE)

    # Split statements more carefully
    statements = []
    current = ''
    for line in seed_sql.split('\n'):
        line = line.strip()
        if line:
            current += ' ' + line
            if line.endswith(';'):
                statements.append(current.strip())
                current = ''

    print(f'Found {len(statements)} SQL statements')

    for i, statement in enumerate(statements, 1):
        if statement and len(statement) > 5:
            print(f'Executing statement {i}...')
            cursor.execute(statement)

    conn.commit()

    # Show counts
    print('\nRecord counts:')
    cursor.execute('SELECT COUNT(*) FROM customer')
    print(f'  Customers: {cursor.fetchone()[0]}')

    cursor.execute('SELECT COUNT(*) FROM pizza')
    print(f'  Pizzas: {cursor.fetchone()[0]}')

    cursor.execute('SELECT COUNT(*) FROM employee')
    print(f'  Employees: {cursor.fetchone()[0]}')

    cursor.execute("SELECT COUNT(*) FROM `order`")
    print(f'  Orders: {cursor.fetchone()[0]}')

    cursor.execute('SELECT COUNT(*) FROM order_detail')
    print(f'  Order Details: {cursor.fetchone()[0]}')

    print('\nDatabase populated successfully!')

    cursor.close()
    conn.close()

except Exception as e:
    print(f'Error: {e}')
    import traceback
    traceback.print_exc()
