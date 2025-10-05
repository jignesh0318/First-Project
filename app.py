from flask import Flask, request, jsonify, render_template
import sqlite3
from datetime import datetime

app = Flask(__name__)

# -------------------- DB INITIALIZATION --------------------
def init_db():
    conn = sqlite3.connect('stock.db')
    c = conn.cursor()
    
    # Products table (unique product name)
    c.execute('''CREATE TABLE IF NOT EXISTS products
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  name TEXT UNIQUE,
                  quantity INTEGER,
                  threshold INTEGER)''')
    
    # Purchases table (with product_id foreign key)
    c.execute('''CREATE TABLE IF NOT EXISTS purchases
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  product_id INTEGER,
                  quantity INTEGER,
                  date TEXT,
                  FOREIGN KEY(product_id) REFERENCES products(id))''')
    
    conn.commit()
    conn.close()

init_db()

# -------------------- HOME --------------------
@app.route('/')
def index():
    return render_template('index.html')

# -------------------- PRODUCTS --------------------
@app.route('/products', methods=['GET'])
def get_products():
    conn = sqlite3.connect('stock.db')
    c = conn.cursor()
    c.execute("SELECT * FROM products")
    rows = c.fetchall()
    conn.close()

    products = []
    for row in rows:
        products.append({
            "id": row[0],
            "name": row[1],
            "quantity": row[2],
            "threshold": row[3],
            "low_stock": row[2] <= row[3]
        })
    return jsonify({"status": "success", "data": products})

@app.route('/products', methods=['POST'])
def add_product():
    data = request.json
    try:
        conn = sqlite3.connect('stock.db')
        c = conn.cursor()
        c.execute("INSERT INTO products (name, quantity, threshold) VALUES (?, ?, ?)",
                  (data['name'].strip().lower(), data['quantity'], data['threshold']))
        conn.commit()
        conn.close()
        return jsonify({"status": "success", "message": "Product added successfully!"})
    except sqlite3.IntegrityError:
        return jsonify({"status": "error", "message": "Product already exists!"}), 400

@app.route('/products/<int:id>', methods=['PUT'])
def update_product(id):
    data = request.json
    conn = sqlite3.connect('stock.db')
    c = conn.cursor()
    c.execute("UPDATE products SET name=?, quantity=?, threshold=? WHERE id=?",
              (data['name'].strip().lower(), data['quantity'], data['threshold'], id))
    conn.commit()
    rows_updated = c.rowcount
    conn.close()

    if rows_updated == 0:
        return jsonify({"status": "error", "message": "Product not found"}), 404
    return jsonify({"status": "success", "message": "Product updated successfully!"})

@app.route('/products/<int:id>', methods=['DELETE'])
def delete_product(id):
    conn = sqlite3.connect('stock.db')
    c = conn.cursor()
    c.execute("DELETE FROM products WHERE id=?", (id,))
    conn.commit()
    rows_deleted = c.rowcount
    conn.close()

    if rows_deleted == 0:
        return jsonify({"status": "error", "message": "Product not found"}), 404
    return jsonify({"status": "success", "message": "Product deleted successfully!"})

# -------------------- PURCHASES --------------------
@app.route('/purchases', methods=['GET'])
def get_purchases():
    conn = sqlite3.connect('stock.db')
    c = conn.cursor()
    # Join purchases with products to show product name
    c.execute("""SELECT purchases.id, products.name, purchases.quantity, purchases.date
                 FROM purchases
                 JOIN products ON purchases.product_id = products.id
                 ORDER BY purchases.id DESC""")
    rows = c.fetchall()
    conn.close()

    purchases = []
    for row in rows:
        purchases.append({
            "id": row[0],
            "name": row[1],
            "quantity": row[2],
            "date": row[3]
        })
    return jsonify({"status": "success", "data": purchases})

@app.route('/purchases', methods=['POST'])
def record_purchase():
    data = request.json
    date_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    conn = sqlite3.connect('stock.db')
    c = conn.cursor()

    # ✅ Get current stock by product_id
    c.execute("SELECT quantity FROM products WHERE id=?", (data['product_id'],))
    result = c.fetchone()
    if not result:
        conn.close()
        return jsonify({"status": "error", "message": "Product not found"}), 404
    
    current_qty = result[0]
    if current_qty < data['quantity']:
        conn.close()
        return jsonify({"status": "error", "message": "Not enough stock available"}), 400

    # Insert purchase using product_id
    c.execute("INSERT INTO purchases (product_id, quantity, date) VALUES (?, ?, ?)",
              (data['product_id'], data['quantity'], date_now))

    # Reduce stock
    c.execute("UPDATE products SET quantity = quantity - ? WHERE id=?",
              (data['quantity'], data['product_id']))

    conn.commit()
    conn.close()
    return jsonify({"status": "success", "message": "Purchase recorded successfully!"})


# -------------------- RUN APP --------------------
if __name__ == '__main__':
    # host=0.0.0.0 → allows access from phone (use your laptop’s IP)
    app.run(host='0.0.0.0', port=5000, debug=True)
