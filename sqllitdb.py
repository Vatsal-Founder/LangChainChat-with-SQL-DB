import sqlite3
from datetime import datetime

# Connect to SQLite
connection = sqlite3.connect("sales.db")
cursor = connection.cursor()

# Drop table if exists (optional for testing)
cursor.execute("DROP TABLE IF EXISTS orders")

# Create the orders table
cursor.execute("""
    CREATE TABLE orders (
        order_id INTEGER PRIMARY KEY AUTOINCREMENT,
        customer_name TEXT,
        product TEXT,
        quantity INTEGER,
        price REAL,
        order_date TEXT
    )
""")

# Sample sales records
orders = [
    ('Alice', 'Wireless Mouse', 2, 25.99, '2024-07-01'),
    ('Bob', 'Standing Desk', 1, 399.99, '2024-07-02'),
    ('Clara', 'Office Chair', 1, 149.99, '2024-07-03'),
    ('Alice', 'Laptop Stand', 3, 45.00, '2024-07-04'),
    ('David', 'Monitor', 1, 199.99, '2024-07-05')
]

# Insert orders
cursor.executemany("""
    INSERT INTO orders (customer_name, product, quantity, price, order_date)
    VALUES (?, ?, ?, ?, ?)
""", orders)

# Display all orders
print("📦 Sales Records:")
for row in cursor.execute("SELECT * FROM orders"):
    print(row)

# Commit changes and close connection
connection.commit()
connection.close()
