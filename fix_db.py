import sqlite3

conn = sqlite3.connect("stock.db")
cursor = conn.cursor()

# Drop old purchases table
cursor.execute("DROP TABLE IF EXISTS purchases")

# Create new purchases table with product_id
cursor.execute("""
CREATE TABLE purchases (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id INTEGER,
    quantity INTEGER,
    date TEXT,
    FOREIGN KEY(product_id) REFERENCES products(id)
)
""")

conn.commit()
conn.close()

print("✅ Database fixed: purchases table recreated with product_id")
