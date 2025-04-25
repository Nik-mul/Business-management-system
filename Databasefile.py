import sqlite3
def create_db():
    con=sqlite3.connect(database=r'ims.db')
    cur=con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS  Category(cid INTEGER PRIMARY KEY AUTOINCREMENT, Name text)")
    con.commit()
  
    cur.execute("CREATE TABLE IF NOT EXISTS  Company(Coid INTEGER PRIMARY KEY AUTOINCREMENT, Name text)")
    con.commit()

    cur.execute("CREATE TABLE IF NOT EXISTS  Product(Pid INTEGER PRIMARY KEY AUTOINCREMENT,Company text,Category text, Name text, Price text,Quantity text)")
    con.commit()

    cur.execute("CREATE TABLE IF NOT EXISTS Sales(Pid INTEGER, Total_sale TEXT)")
    con.commit()
    
create_db()