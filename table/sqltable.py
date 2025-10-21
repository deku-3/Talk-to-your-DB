import sqlite3
from faker import Faker
import random

# Optional: seed for reproducible fake data
SEED = 42
random.seed(SEED)
fake = Faker()
Faker.seed(SEED)

DB = "sales.db"

# Connect
conn = sqlite3.connect(DB)
cur = conn.cursor()

# Recreate schema
cur.executescript("""
DROP TABLE IF EXISTS sales;
DROP TABLE IF EXISTS customer;
DROP TABLE IF EXISTS product;
""")

cur.execute("""
CREATE TABLE customer (
    customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    email TEXT,
    join_date TEXT,
    city TEXT,
    loyalty_points INTEGER
);
""")

cur.execute("""
CREATE TABLE product (
    product_id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_name TEXT,
    category TEXT,
    unit_cost REAL,
    unit_price REAL
);
""")

cur.execute("""
CREATE TABLE sales (
    sale_id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id INTEGER,
    product_id INTEGER,
    quantity_sold INTEGER,
    sale_date TEXT,
    FOREIGN KEY (customer_id) REFERENCES customer(customer_id),
    FOREIGN KEY (product_id) REFERENCES product(product_id)
);
""")

# Insert 20 customers
customers = []
for _ in range(20):
    customers.append((
        fake.name(),  # <-- human-readable name
        fake.email(),
        fake.date_between(start_date='-2y', end_date='today').isoformat(),
        fake.city(),
        random.randint(0, 1000)
    ))

cur.executemany(
    "INSERT INTO customer (name, email, join_date, city, loyalty_points) VALUES (?, ?, ?, ?, ?)",
    customers
)
conn.commit()

# Debug: print the customers we will find in DB (verify insertion)
print("=== customers (INSERT preview) ===")
for c in customers[:5]:
    print(c)

# Build products and insert (5 per category)
category_map = {
    'Electronics': ['Smartphone', 'Laptop', 'Headphones', 'Smartwatch', 'Bluetooth Speaker'],
    'Books': ['Fiction Novel', 'Science Textbook', 'Cooking Guide', 'Self-Help Book', 'Travel Journal'],
    'Clothing': ['T-Shirt', 'Jeans', 'Jacket', 'Sneakers', 'Formal Shirt'],
    'Grocery': ['Rice Bag', 'Cooking Oil', 'Pasta Pack', 'Breakfast Cereal', 'Coffee Powder'],
    'Toys': ['Building Blocks', 'Action Figure', 'Puzzle Set', 'Remote Car', 'Stuffed Animal']
}

products = []
for category, items in category_map.items():
    for product_name in items:
        cost = round(random.uniform(10, 100), 2)
        price = round(cost + random.uniform(5, 50), 2)
        products.append((product_name, category, cost, price))

cur.executemany(
    "INSERT INTO product (product_name, category, unit_cost, unit_price) VALUES (?, ?, ?, ?)",
    products
)
conn.commit()

# Verify products inserted (first 8)
print("\n=== products (first 8) ===")
for row in cur.execute("SELECT product_id, product_name, category FROM product LIMIT 8"):
    print(row)

# Fetch IDs for sales
customer_ids = [r[0] for r in cur.execute("SELECT customer_id FROM customer").fetchall()]
product_ids = [r[0] for r in cur.execute("SELECT product_id FROM product").fetchall()]

# Insert 50 sales
sales = []
for _ in range(50):
    sales.append((
        random.choice(customer_ids),
        random.choice(product_ids),
        random.randint(1, 10),
        fake.date_between(start_date='-1y', end_date='today').isoformat()
    ))

cur.executemany(
    "INSERT INTO sales (customer_id, product_id, quantity_sold, sale_date) VALUES (?, ?, ?, ?)",
    sales
)
conn.commit()

# Final verification queries
print("\n=== customers table (first 10 rows from DB) ===")
for row in cur.execute("SELECT customer_id, name, email, join_date, city, loyalty_points FROM customer LIMIT 10"):
    print(row)

print("\n=== sample sales join (first 10) ===")
for row in cur.execute("""
SELECT s.sale_id, c.name, p.product_name, s.quantity_sold, s.sale_date
FROM sales s
JOIN customer c ON s.customer_id = c.customer_id
JOIN product p ON s.product_id = p.product_id
LIMIT 10
"""):
    print(row)

conn.close()

print("\n✅ Enhanced sales.db created with customers, products, and sales.")
