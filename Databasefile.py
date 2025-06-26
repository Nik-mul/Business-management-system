import sqlite3
import random
import datetime
def create_db():
    con=sqlite3.connect(database=r'ims.db')
    cur=con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS  Category(cid INTEGER PRIMARY KEY AUTOINCREMENT, Name text)")
    con.commit()
  
    cur.execute("CREATE TABLE IF NOT EXISTS  Company(Coid INTEGER PRIMARY KEY AUTOINCREMENT, Name text)")
    con.commit()
    
    cur.execute("CREATE TABLE IF NOT EXISTS  Product(Pid INTEGER PRIMARY KEY AUTOINCREMENT,Company text,Category text, Name text, Price text,Quantity text)")
    con.commit()

    # Create product_sales table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS product_sales (
            Pid INTEGER PRIMARY KEY AUTOINCREMENT,
            Category TEXT,
            Name TEXT,
            Price REAL,
            Quantity INTEGER,
            SaleDate TEXT
        )
    """)

    # Clear existing product_sales data
    cur.execute("DELETE FROM product_sales")

    # Sample categories and product names
    categories = {
        "Electronics": ["Phone", "Laptop", "TV"],
        "Clothing": ["Shirt", "Jacket", "Jeans"],
        "Books": ["Novel", "Comics", "Biography"],
        "Furniture": ["Chair", "Table", "Sofa"]
    }

    # Insert 1 year of sales
    start_date = datetime.date(2024, 6, 1)
    for i in range(365):
        day = start_date + datetime.timedelta(days=i)
        for cat, names in categories.items():
            for name in names:
                price = random.randint(500, 5000)
                quantity = random.randint(1, 20)
                cur.execute("""
                    INSERT INTO product_sales (Category, Name, Price, Quantity, SaleDate)
                    VALUES (?, ?, ?, ?, ?)
                """, (cat, name, price, quantity, day.isoformat()))

    print("✅ Auto-incremented Pid and category-wise sales inserted.")

    # Create daily_sales table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS daily_sales (
            sale_date TEXT,
            total_sale REAL
        )
    """)


    for i in range(365):
        date = start_date + datetime.timedelta(days=i)
        sale = random.randint(1000, 20000)
        cur.execute("INSERT INTO daily_sales (sale_date, total_sale) VALUES (?, ?)", (date.isoformat(), sale))

    print("✅ sales.db created with 1 year of data.")

    con.commit()
    con.close()

create_db()