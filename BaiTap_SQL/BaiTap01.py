import sqlite3

conn = sqlite3.connect('test.db')

cursor = conn.cursor()

#2. thao tac voi database

# Lenh SQL tao bang products
sql1 = """
CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    price REAL NOT NULL,
    quantity INTEGER NOT NULL
);
"""
#thuc thi lenh tao bang 
cursor.execute(sql1)
conn.commit()

# 3. CRUD
# 3.1 them du lieu
products = [
    ('Laptop', 1200.50, 10),
    ('Smartphone', 800.00, 25),
    ('Tablet', 450.75, 15)
]

# lenh sql de chen du lieu. dung '?'' de tranh loi SQL Injection
sql2 = """
INSERT INTO products (name, price, quantity) 
VALUES (?, ?, ?)
"""

# them nhieu ban ghi 
cursor.executemany(sql2, products)
conn.commit()

# 3.2 doc du lieu
sql3 = "SELECT * FROM products"

# thuc thi lenh
cursor.execute(sql3)

#lay tat ca ket qua
all_products = cursor.fetchall()

#in tieu de
print(f"{'ID':<5} {'Name':<15} {'Price':<10} {'Quantity':<10}")
#lap va in ra 
for p in all_products:
    print(f"{p[0]:<5} {p[1]:<15} {p[2]:<10} {p[3]:<10}")

#3.3 cap nhat du lieu
sql4 = """
UPDATE products
SET price = ? , quantity = ?
WHERE id = ?
"""
cursor.execute(sql4, (999.99, 30, 2))
conn.commit()

#3.4 xoa du lieu
sql5 = """  
DELETE FROM products
WHERE id = ?
"""
cursor.execute(sql5, (3,))
conn.commit()