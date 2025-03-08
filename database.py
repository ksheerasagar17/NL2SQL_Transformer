import sqlite3
import os

DATABASE_PATH = "ecommerce.db"

def get_db_connection():
    """Create a database connection"""
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialize the database with tables and sample data"""
    if os.path.exists(DATABASE_PATH):
        os.remove(DATABASE_PATH)
    
    conn = get_db_connection()
    cursor = conn.cursor()

    # Create tables
    cursor.executescript('''
        -- First create tables in correct order
        CREATE TABLE products (
            product_id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            description TEXT,
            price DECIMAL(10, 2) NOT NULL,
            category TEXT,
            stock_quantity INTEGER NOT NULL
        );

        CREATE TABLE customers (
            customer_id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            join_date DATE NOT NULL,
            total_orders INTEGER DEFAULT 0
        );

        CREATE TABLE orders (
            order_id INTEGER PRIMARY KEY,
            customer_id INTEGER,
            order_date DATETIME NOT NULL,
            total_amount DECIMAL(10, 2) NOT NULL,
            status TEXT NOT NULL,
            FOREIGN KEY (customer_id) REFERENCES customers (customer_id)
        );

        CREATE TABLE order_items (
            order_item_id INTEGER PRIMARY KEY,
            order_id INTEGER,
            product_id INTEGER,
            quantity INTEGER NOT NULL,
            price_at_time DECIMAL(10, 2) NOT NULL,
            FOREIGN KEY (order_id) REFERENCES orders (order_id),
            FOREIGN KEY (product_id) REFERENCES products (product_id)
        );
    ''')

    # Insert sample data
    sample_products = [
        (1, 'Laptop Pro X', 'High-performance laptop with 16GB RAM', 1299.99, 'Electronics', 50),
        (2, 'Wireless Earbuds', 'Noise-cancelling wireless earbuds', 149.99, 'Electronics', 200),
        (3, 'Running Shoes', 'Comfortable running shoes for athletes', 79.99, 'Sports', 150),
        (4, 'Coffee Maker', 'Automatic drip coffee maker', 49.99, 'Home & Kitchen', 100),
        (5, 'Backpack', 'Water-resistant laptop backpack', 39.99, 'Accessories', 300)
    ]

    sample_customers = [
        (1, 'John Doe', 'john@example.com', '2024-01-01', 3),
        (2, 'Jane Smith', 'jane@example.com', '2024-01-15', 2),
        (3, 'Bob Wilson', 'bob@example.com', '2024-02-01', 1),
        (4, 'Alice Brown', 'alice@example.com', '2024-02-15', 4),
        (5, 'Charlie Davis', 'charlie@example.com', '2024-03-01', 0)
    ]

    sample_orders = [
        (1, 1, '2024-02-01 10:00:00', 1299.99, 'Delivered'),
        (2, 1, '2024-02-15 14:30:00', 149.99, 'Delivered'),
        (3, 2, '2024-02-20 09:15:00', 119.98, 'Shipped'),
        (4, 4, '2024-03-01 16:45:00', 89.98, 'Processing'),
        (5, 3, '2024-03-05 11:20:00', 49.99, 'Delivered')
    ]

    sample_order_items = [
        (1, 1, 1, 1, 1299.99),  # Laptop Pro X
        (2, 2, 2, 1, 149.99),   # Wireless Earbuds
        (3, 3, 3, 1, 79.99),    # Running Shoes
        (4, 3, 4, 1, 39.99),    # Coffee Maker
        (5, 4, 5, 2, 44.99),    # Backpack
        (6, 5, 4, 1, 49.99)     # Coffee Maker
    ]

    cursor.executemany('INSERT INTO products VALUES (?, ?, ?, ?, ?, ?)', sample_products)
    cursor.executemany('INSERT INTO customers VALUES (?, ?, ?, ?, ?)', sample_customers)
    cursor.executemany('INSERT INTO orders VALUES (?, ?, ?, ?, ?)', sample_orders)
    cursor.executemany('INSERT INTO order_items VALUES (?, ?, ?, ?, ?)', sample_order_items)

    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()
