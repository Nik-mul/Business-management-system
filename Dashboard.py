import customtkinter as ctk
from Category import Categoryclass
from products import productclass
from Company import Companyclass
from Billing import Billing
from Analysis import Analysis
from pendingStocks import PendingStock
from tkinter import *
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import sqlite3
import pandas as pd
import time
from datetime import datetime
import math

# Sample fake data
sample_data = {"Employee": 12, "Products": 45, "Quantity": 5615, "Billing": 37}
pie_data = {
    "Electronics": 40,
    "Clothing": 25,
    "Books": 20,
    "Others": 15
}

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class DashboardApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Your Inventory Name| developed by Nikhil Multani")
        self.root.geometry("1400x800+0+0")

        self.sidebar = ctk.CTkFrame(self.root, width=250, height=800, corner_radius=0)
        self.sidebar.place(x=0, y=0)
        self.sidebar.pack_propagate(False)  # 🔥 this prevents shrinking to content



        ctk.CTkLabel(self.sidebar, text="Dashboard Menu", font=("Arial", 18, "bold")).pack(pady=15)

        btns = [
            "Company", "Products", "Category", "Billing","Analysis" ,"Ratios"
        ]
        for b in btns:
            ctk.CTkButton(self.sidebar, text=b, command=lambda name=b: self.on_menu_click(name),width=200,height=110).pack(pady=5, fill="x", padx=10)
        
        # Main Frame .....................
        self.main_frame=ctk.CTkFrame(self.root,width=1150, height=800)
        self.main_frame.place(x=250,y=60)
        
        # Company,Shop name................
        self.text_frame = ctk.CTkFrame(self.root, width=1150, height=60, fg_color="transparent")
        self.text_frame.place(x=250,y=0)
        self.text_frame.pack_propagate(False) 

        title_label = ctk.CTkLabel(self.text_frame, text="Your Shop", font=("Arial", 28, "bold"))
        title_label.place(y=60)
        title_label.pack(pady=10)

        # Total Products............
        self.P_frame=ctk.CTkFrame(self.main_frame,width=290,height=150, fg_color="black")
        self.P_frame.place(x=10,y=0)  
        
        self.p_label= ctk.CTkLabel(self.P_frame, text="Total Prodcucts:0", font=("Arial", 24, "bold"))
        self.p_label.place(x=50,y=50)
        
        #Total Category.........
        self.C_frame=ctk.CTkFrame(self.main_frame,width=290, height=150,fg_color='Black')
        self.C_frame.place(x=10,y=160)
        
        self.c_label= ctk.CTkLabel(self.C_frame, text="Total Categories:0", font=("Arial", 24, "bold"))
        self.c_label.place(x=50,y=50)

        # Total Sale
        self.S_frame=ctk.CTkFrame(self.main_frame,width=290, height=150,fg_color='Black')
        self.S_frame.place(x=10,y=320)
        
        self.s_label= ctk.CTkLabel(self.S_frame, text="Total Sales:9000000", font=("Arial", 24, "bold")).place(x=50,y=50)

        self.update_dashboard_counts()
        # =======chart section=============
        # Load sample sales data
        self.load_sample_data()

        # Chart frame
        self.chart_container = ctk.CTkFrame(self.main_frame, width=1100, height=500, fg_color="transparent")
        self.chart_container.place(x=310, y=0)
        self.chart_container.pack_propagate(False)

        # Draw initial chart

        self.update_sales_chart("Monthly")
# ==========pie chart===============

        self.draw_category_pie_chart()
        
# =============slicer===================
        self.slicer_option = ctk.StringVar(value="Monthly")
        self.slicer_menu = ctk.CTkOptionMenu(self.main_frame, values=["Weekly", "Monthly", "Quarterly", "Yearly"],
                                            variable=self.slicer_option, command=self.update_sales_chart)
        self.slicer_menu.place(x=370, y=20)
        self.slicer_menu.lift()

        # ==================pending stock ==============
        btn = ctk.CTkButton(self.root, text="i", command=self.pendingstock,height=40,width=40)
        btn.place(x=1310,y=10)
        # === Notification Badge ===
        try:
            import sqlite3
            def get_pending_stock_count():
                con = sqlite3.connect('ims.db')
                cur = con.cursor()
                cur.execute("SELECT COUNT(*) FROM Product WHERE CAST(Quantity AS INTEGER) < 5")
                count = cur.fetchone()[0]
                con.close()
                return count
        except:
            def get_pending_stock_count():
                return 0

        pending_count = get_pending_stock_count()

        if pending_count > 0:
            badge = ctk.CTkLabel(self.root,
                                text=str(pending_count),
                                text_color="white",
                                fg_color="red",
                                corner_radius=50,
                                width=20,
                                height=20,
                                font=("Arial", 12, "bold"))
            badge.place(x=1335, y=5) 

    # ===== Clock=====
        self.canvas = Canvas(self.main_frame, width=340, height=300, bg="#0f0f0f", highlightthickness=0)
        self.canvas.place(x=20,y=600)

        self.center_x = 170
        self.center_y = 150
        self.clock_radius = 145

        self.draw_clock_face()
        self.update_clock()

        # =====info frame====
        # Chart frame
        self.info_frame = ctk.CTkFrame(self.main_frame, width=500, height=305, fg_color="white")
        self.info_frame.place(x=635, y=410)
        self.info_frame.pack_propagate(False)

        self.Avg_label= ctk.CTkLabel(self.info_frame, text="Average Sale per day:-55,000", font=("Arial", 26, "bold"),text_color="Black")
        self.Avg_label.place(x=20,y=30)
        self.exp_label= ctk.CTkLabel(self.info_frame, text="Total Expenses in a month:- 40,000", font=("Arial", 26, "bold"),text_color="Black")
        self.exp_label.place(x=20,y=130)
        self.Avg_label= ctk.CTkLabel(self.info_frame, text="Average profit per day:-20000", font=("Arial", 24, "bold"),text_color="Black")
        self.Avg_label.place(x=20,y=230)

        






    def update_dashboard_counts(self):
        con = sqlite3.connect("ims.db")
        cur = con.cursor()

        try:
            # Total Products
            cur.execute("SELECT COUNT(*) FROM Product")
            total_products = cur.fetchone()[0]

            # Total Categories
            cur.execute("SELECT COUNT(*) FROM Category")
            total_categories = cur.fetchone()[0]

            # # Total Sales for current month
            # now = datetime.now()
            # month = now.strftime("%m")
            # year = now.strftime("%Y")
            # cur.execute("SELECT SUM(total) FROM daily_sales WHERE strftime('%m', date) = ? AND strftime('%Y', date) = ?", (month, year))
            # total_sales = cur.fetchone()[0]
            # total_sales = total_sales if total_sales is not None else 0

            # Update labels
            self.p_label.configure(text=f"Total Products: {total_products}")
            self.c_label.configure(text=f"Total Categories: {total_categories}")
            # self.s_label.configure(text=f"Total Sales: ₹{total_sales:.2f}")

        except Exception as ex:
            print("Dashboard update error:", ex)
        finally:
            con.close()

       
        
                

    def load_sample_data(self):

        conn = sqlite3.connect("ims.db")
        query = "SELECT sale_date AS Date, total_sale AS TotalSale FROM daily_sales"
        self.sales_df = pd.read_sql_query(query, conn)
        conn.close()

        self.sales_df["Date"] = pd.to_datetime(self.sales_df["Date"])

    def load_category_sales(self):
        import sqlite3
        import pandas as pd

        conn = sqlite3.connect("ims.db")
        df = pd.read_sql_query("SELECT Category, Price, Quantity FROM product_sales", conn)
        conn.close()

        # Total sale = price × quantity
        df["TotalSale"] = df["Price"] * df["Quantity"]

        # Group by category
        category_sales = df.groupby("Category")["TotalSale"].sum()
        return category_sales
    
    def category(self):
        self.new_win=Toplevel(self.root)
        self.new_obj=Categoryclass(self.new_win)
    def product(self):
        self.new_win=Toplevel(self.root)
        self.new_obj=productclass(self.new_win)

    def company(self):
        self.new_win=Toplevel(self.root)
        self.new_obj=Companyclass(self.new_win)
    
    def Billing(self):
        self.new_win=Toplevel(self.root)
        self.new_obj=Billing(self.new_win)
    
    def Analysis(self):
        self.new_win=Toplevel(self.root)
        self.new_obj=Analysis(self.new_win)
    def pendingstock(self):
        self.new_win=Toplevel(self.root)
        self.new_obj=PendingStock(self.new_win)
    
    def on_menu_click(self, name):
        if name=="Category":
            self.category()
        elif name=="Products":
            self.product()
        elif name=="Company":
            self.company()
        elif name=="Billing":
            self.Billing()
        elif name=="Analysis":
            self.Analysis()
        else:
            print("nothing")
        print(f"{name} button clicked")


    
 
    def update_sales_chart(self, period):
        df = self.sales_df.copy()
        df.set_index("Date", inplace=True)

        if period == "Weekly":
            grouped = df.resample("W").sum()
        elif period == "Monthly":
            grouped = df.resample("ME").sum()
        elif period == "Quarterly":
            grouped = df.resample("Q").sum()
        elif period == "Yearly":
            grouped = df.resample("Y").sum()
        else:
            grouped = df

        self.draw_sales_chart(grouped, period)

    def draw_sales_chart(self, grouped_df, label):
        for widget in self.chart_container.winfo_children():
            widget.destroy()

        fig, ax = plt.subplots(figsize=(7, 2.5))
        ax.bar(grouped_df.index.strftime('%Y-%m-%d'), grouped_df['TotalSale'], color='orange')
        ax.set_title(f"Sales by {label}", fontsize=12)
        ax.set_ylabel("Total Sales", fontsize=10)
        ax.tick_params(axis='x', labelsize=8,)
        ax.set_xticks(ax.get_xticks()[::max(1, len(grouped_df)//10)])


        canvas = FigureCanvasTkAgg(fig, master=self.chart_container)
        canvas.draw()
        canvas.get_tk_widget().place(x=0, y=0, width=1000, height=500)

    def draw_category_pie_chart(self):
        category_sales = self.load_category_sales()

        # Frame for pie chart (add to self.main_frame)
        self.category_pie_frame = ctk.CTkFrame(self.main_frame, width=300, height=300)
        self.category_pie_frame.place(x=330, y=410)

        fig, ax = plt.subplots(figsize=(3, 3))
        colors = ['#ff9999','#66b3ff','#99ff99','#ffcc99']
        ax.pie(category_sales.values, labels=category_sales.index, colors=colors,
            autopct='%1.1f%%', startangle=90)
        ax.axis('equal')

        canvas = FigureCanvasTkAgg(fig, master=self.category_pie_frame)
        canvas.draw()
        canvas.get_tk_widget().place(x=0, y=0, width=370, height=370)

        # ==========clock=======
    def draw_clock_face(self):
        # Outer circle
        self.canvas.create_oval(self.center_x - self.clock_radius, self.center_y - self.clock_radius,
                                self.center_x + self.clock_radius, self.center_y + self.clock_radius,
                                outline="#0ff", width=4)

        # Hour marks
        for i in range(12):
            angle = math.radians(i * 30)
            x_inner = self.center_x + math.sin(angle) * (self.clock_radius - 20)
            y_inner = self.center_y - math.cos(angle) * (self.clock_radius - 20)
            x_outer = self.center_x + math.sin(angle) * (self.clock_radius - 5)
            y_outer = self.center_y - math.cos(angle) * (self.clock_radius - 5)
            self.canvas.create_line(x_inner, y_inner, x_outer, y_outer, fill="#0ff", width=2)

    def update_clock(self):
        self.canvas.delete("hands")

        t = time.localtime()
        second = t.tm_sec
        minute = t.tm_min
        hour = t.tm_hour % 12 + minute / 60.0

        # Draw hour hand
        self.draw_hand(hour * 30, self.clock_radius * 0.5, width=6, color="#ff69b4")  # pink
        # Draw minute hand
        self.draw_hand(minute * 6, self.clock_radius * 0.7, width=4, color="#ffff00")  # yellow
        # Draw second hand
        self.draw_hand(second * 6, self.clock_radius * 0.9, width=2, color="#00ffff")  # cyan

        self.root.after(1000, self.update_clock)

    def draw_hand(self, angle_deg, length, width, color):
        angle_rad = math.radians(angle_deg)
        x_end = self.center_x + math.sin(angle_rad) * length
        y_end = self.center_y - math.cos(angle_rad) * length
        self.canvas.create_line(self.center_x, self.center_y, x_end, y_end,
                                fill=color, width=width, tags="hands", capstyle=ROUND)

# Run the app
if __name__ == "__main__":
    root = ctk.CTk()
    app = DashboardApp(root)
    root.mainloop()
