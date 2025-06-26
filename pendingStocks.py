from tkinter import *
from tkinter import messagebox, ttk
import sqlite3

class PendingStock:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1000x600+400+0")
        self.root.title("Low stocks | Developed By Nikhil Multani")
        self.root.config(bg="white")

        self.stock_limit = 5  # Default threshold

        product_frame = Frame(self.root, bd=10, relief=RIDGE)
        product_frame.place(x=0, y=2, width=1000, height=600)

        scrollx = Scrollbar(product_frame, orient=HORIZONTAL)
        scrolly = Scrollbar(product_frame, orient=VERTICAL)

        self.ProductTable = ttk.Treeview(product_frame, columns=("Pid", "Name", "Pending Qty"),
                                         yscrollcommand=scrolly.set, xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM, fill=X)
        scrolly.pack(side=RIGHT, fill=Y)
        scrollx.config(command=self.ProductTable.xview)
        scrolly.config(command=self.ProductTable.yview)

        self.ProductTable.heading("Pid", text="Pid")
        self.ProductTable.heading("Name", text="Name")
        self.ProductTable.heading("Pending Qty", text="Pending Qty")
        self.ProductTable["show"] = "headings"

        self.ProductTable.column("Pid", width=100)
        self.ProductTable.column("Name", width=500)
        self.ProductTable.column("Pending Qty", width=150)
        self.ProductTable.pack(fill=BOTH, expand=1)

        self.show_pending_stocks()

    def show_pending_stocks(self):
        try:
            con = sqlite3.connect(database='ims.db')
            cur = con.cursor()
            cur.execute("SELECT Pid, Name, Quantity FROM Product")
            products = cur.fetchall()
            self.ProductTable.delete(*self.ProductTable.get_children())

            for prod in products:
                pid, name, qty = prod
                try:
                    qty = int(qty)
                    if qty < self.stock_limit:
                        pending_qty = self.stock_limit - qty
                        self.ProductTable.insert('', END, values=(pid, name, pending_qty))
                except ValueError:
                    continue  # Skip rows with invalid quantities

            con.close()

        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}", parent=self.root)

    def get_pending_stock_count(self):
        try:
            con = sqlite3.connect(database='ims.db')
            cur = con.cursor()
            cur.execute("SELECT COUNT(*) FROM Product WHERE CAST(Quantity AS INTEGER) < ?", (self.stock_limit,))
            count = cur.fetchone()[0]
            con.close()
            return count
        except:
            return 0


# To test this page directly
if __name__ == "__main__":
    root = Tk()
    obj = PendingStock(root)
    root.mainloop()
