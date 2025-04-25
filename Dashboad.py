from tkinter import*
from  PIL import Image
from Category import Categoryclass
from products import productclass
from Company import Companyclass
from pendingStocks import Discountclass
from tkcalendar import Calendar
import time
import math

class IMS:
    def __init__(self,root):
        self.root=root
        self.root.geometry("1350x700+0+0")
        self.root.title("Business Management Syestem | developed by Grp-No.-102| Nikhil Multani")
        self.root.config(bg="white")

        # ==title==
        self.icon=PhotoImage(file="")
        tile=Label(self.root , text="Business Management System" , image=self.icon, compound=LEFT, font=("Gil Sans",40,"bold"), bg="black",fg="white").place(x=0,y=0,relwidth=1,height=70)

        # ==button==
        logoutbtn=Button(self.root, text="EXIT", font=("Gill Sans",15,"bold"),bg="red", cursor="hand2").place(x=1155,y=10,height=50,width=150)
        logoutbtn=Button(self.root, text="(i)", font=("Gill Sans",10,"bold"),bg="blue",fg='white', cursor="hand2",command=self.pendingstock).place(x=1075,y=10,height=50,width=50)

        self.samaye=Label(self.root, text="आपका स्वागत है/Welcome\t\t Date: DD/MM/YY\t\t Time=HH:MM:SS",font=("Gill Sans",15,"bold"),bg="grey")
        self.samaye.place(x=0,y=70,height=30,relwidth=1)
        
        self.update_time()
        
        # ==leftmenu==
        LeftMenu=Frame(self.root,bd=2,relief=RIDGE, bg="white")
        LeftMenu.place(x=0,y=102,width=200,height=700)
        
        labelmenu=Label(LeftMenu ,text="Menu",font=("Gil Sans",20), bg="black",fg="white").pack(side=TOP,fill=X)
        labelbutton=Button(LeftMenu ,text="Employee",font=("Gil Sans",20,"bold"), bg="dark blue",fg="white",bd=3,cursor="hand2").pack(side=TOP,fill=X)
        labelbutton=Button(LeftMenu ,text="Company",command=self.company,font=("Gil Sans",20,"bold"), bg="dark blue",fg="white",bd=3,cursor="hand2").pack(side=TOP,fill=X)
        labelbutton=Button(LeftMenu ,text="Category",command=self.category,font=("Gil Sans",20,"bold"), bg="dark blue",fg="white",bd=3,cursor="hand2").pack(side=TOP,fill=X)
        labelbutton=Button(LeftMenu ,text="Sales",font=("Gil Sans",20,"bold"), bg="dark blue",fg="white",bd=3,cursor="hand2").pack(side=TOP,fill=X)
        labelbutton=Button(LeftMenu ,text="Products",font=("Gil Sans",20,"bold"),command=self.product, bg="dark blue",fg="white",bd=3,cursor="hand2").pack(side=TOP,fill=X)

        # ==content==

        self.lbl_emplyee=Label(self.root,text="Total Employee\n[0]",bd=3,relief=RIDGE, bg="Black",fg="white",font=("Gills Sans",20))
        self.lbl_emplyee.place(x=210,y=120,width=300,height=80)
       
        self.lbl_supplier=Label(self.root,text="Total Supplier\n[0]",bd=3,relief=RIDGE, bg="Black",fg="white",font=("Gills Sans",20))
        self.lbl_supplier.place(x=560,y=120,width=300,height=80)
       
        self.lbl_category=Label(self.root,text="Total Category\n[0]",bd=3,relief=RIDGE, bg="Black",fg="white",font=("Gills Sans",20))
        self.lbl_category.place(x=910,y=120,width=300,height=80)
       
        self.lbl_sales=Label(self.root,text="Total Sales\n[0]",bd=3,relief=RIDGE, bg="Black",fg="white",font=("Gills Sans",20))
        self.lbl_sales.place(x=210,y=220,width=300,height=80)
       
        self.lbl_products=Label(self.root,text="Total Product\n[0]",bd=3,relief=RIDGE, bg="Black",fg="white",font=("Gills Sans",20))
        self.lbl_products.place(x=560,y=220,width=300,height=80)

        # ==calender==
        Calender_frame=Frame(self.root,bd=2,relief=RIDGE, bg="yellow")
        Calender_frame.place(x=210,y=320,width=280,height=250)
        # Calendar widget
        cal = Calendar(
                        Calender_frame,
                        font=('Arial',14),
                        selectmode='day',  # other options: 'none', 'day', 'week', 'month'
                        year=2025,
                        month=4,
                        day=14,
                        date_pattern='yyyy-mm-dd',  # or 'dd/mm/yyyy'
                        background='lightblue',
                        foreground='black',
                        headersbackground='grey',
                        headersforeground='white',
                        selectbackground='blue',
                        selectforeground='white'
                    )
        cal.pack(pady=5)
        # ==Clock==
        self.canvas = Canvas(self.root, width=320, height=320, bg="#0f0f0f", highlightthickness=0)
        self.canvas.place(x=550,y=310)

        self.center_x = 160
        self.center_y = 160
        self.clock_radius = 150

        self.draw_clock_face()
        self.update_clock()
        # ===StickyNotes===
        Sticky_frame=Frame(self.root,bd=2,relief=RIDGE,bg='white')
        Sticky_frame.place(x=885,y=220,width=400,height=400)
        sticky_title = Label(Sticky_frame, text="📝 Sticky Notes", font=("Arial", 14, "bold"),fg='white',bg='black')
        sticky_title.pack(pady=5)

        # Text area
        text =Text(Sticky_frame, wrap="word", font=("Arial", 11))
        text.pack(padx=10, expand=True, fill='both')

        # Buttons
        SB_frame = Frame(Sticky_frame)
        SB_frame.pack(side=BOTTOM,fill=X,pady=5)

        save_btn = Button(SB_frame, text="💾 Save", width=10)
        save_btn.pack(side=LEFT, padx=5)

        load_btn = Button(SB_frame, text="📂 Load", width=10)
        load_btn.pack(side=LEFT, padx=5)



        # ==footer==
        self.footer=Label(self.root, text="THANK YOU|Developed by Group-No.-102|Nikhil Multani",font=("Gill Sans",15,"bold"),bg="grey").pack(side=BOTTOM,fill=X)

# =================================================================

    def category(self):
        self.new_win=Toplevel(self.root)
        self.new_obj=Categoryclass(self.new_win)
    def product(self):
        self.new_win=Toplevel(self.root)
        self.new_obj=productclass(self.new_win)

    def company(self):
        self.new_win=Toplevel(self.root)
        self.new_obj=Companyclass(self.new_win)
    
    def pendingstock(self):
        self.new_win=Toplevel(self.root)
        self.new_obj=Discountclass(self.new_win)

    def update_time(self):
        current_time = time.strftime("%H:%M:%S")  # Get the current time in HH:MM:SS format
        current_date = time.strftime("%d/%m/%y")  # Get the current date in DD/MM/YY format
        self.samaye.config(text=f"आपका स्वागत है/Welcome\t\t Date:{current_date} \t\t Time={current_time}")
        self.root.after(1000, self.update_time)

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


if __name__=="__main__":
    root=Tk()
    obj=IMS(root)
    root.mainloop()