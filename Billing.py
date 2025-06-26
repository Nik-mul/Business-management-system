from tkinter import*
from  PIL import Image
from tkinter import ttk,messagebox
# from discount import Discountclass
import time
import sqlite3
import qrcode
import PIL
import pandas as pd
class Billing:
    def __init__(self,root):
        self.root=root
        self.root.geometry("1363x700+0+0")
        self.root.title(" Billing | developed by Nikhil Multani")
        self.root.config(bg="white")
        self.cartlist=[]

        # ==title==
        self.icon=PhotoImage(file="")
        tile=Label(self.root , text="Billing Section" , image=self.icon, compound=LEFT, font=("Gil Sans",40,"bold"), bg="black",fg="white").place(x=0,y=0,relwidth=1,height=70)
         
        # ==button==
        logoutbtn=Button(self.root, text="exit", font=("Gill Sans",15,"bold"),bg="red", cursor="hand2").place(x=1150,y=10,height=50,width=150)

        # ==clock==
        self.samaye=Label(self.root, text="Your Welcome\t\t Date: DD/MM/YY\t\t Time=HH:MM:SS",font=("Gill Sans",15,"bold"),bg="grey").place(x=0,y=70,height=30,relwidth=1)


        # =====productframe====
        self.var_search=StringVar()
        ProductFrame1=Frame(self.root,bd=4,relief=RIDGE, bg="white")
        ProductFrame1.place(x=6,y=110,width=410,height=580)
        
        ProductFrame2=Frame(ProductFrame1,bd=2,relief=RIDGE, bg="white")
        ProductFrame2.place(x=2,y=42,width=398,height=120)
        P_tile=Label(ProductFrame1, text="All Products",font=("Gil Sans",20,"bold"), bg="black",fg="white").pack(side=TOP,fill=X)

        lbl_search=Label(ProductFrame2,text="Search product| By Name",font=("Gill Sans",15,"bold"),bg="white",fg="green", ).place(x=2,y=5)
        lbl_name=Label(ProductFrame2,text="Product Name",font=("times new roman",15,),bg="white",).place(x=2,y=45)
        lbl_txt=Entry(ProductFrame2,text=self.var_search,font=("times new roman",15,),bg="light yellow",).place(x=128,y=47,width=150,height=22)
        lbl_btn=Button(ProductFrame2,text="Search",command=self.search,font=("Gills sans",15,),bg="green",cursor="hand2").place(x=285,y=45,width=100,height=25)
        lbl_btn=Button(ProductFrame2,text="Show All",command=self.show,font=("Gills sans",15,),bg="pink",cursor="hand2").place(x=285,y=5,width=100,height=25)

        productframe3=Frame(ProductFrame1,bd=3,relief=RIDGE,)
        productframe3.place(x=2,y=140,width=398,height=425)

        scrollx=Scrollbar(productframe3,orient=HORIZONTAL)
        scrolly=Scrollbar(productframe3,orient=VERTICAL)

        self.Producttable=ttk.Treeview(productframe3,columns=("Pid","Name","Price","Qty"),yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM,fill=X)
        scrolly.pack(side=RIGHT,fill=Y)
        scrollx.config(command=self.Producttable.xview)
        scrolly.config(command=self.Producttable.yview)

        self.Producttable.heading("Pid",text="Pid")
        self.Producttable.heading("Name",text="Name")
        self.Producttable.heading("Price",text="Price")
        self.Producttable.heading("Qty",text="Qty")
        self.Producttable["show"]="headings"
        self.Producttable.column("Pid",width=30)
        self.Producttable.column("Name",width=100)
        self.Producttable.column("Price",width=50)
        self.Producttable.column("Qty",width=50)
        self.Producttable.pack(fill=BOTH,expand=1)
        self.Producttable.bind("<ButtonRelease-1>",self.get_data)
        self.show()


        # =============================Customerframe========================
        self.var_cname=StringVar()
        self.var_Contact=StringVar()

        Coustomerframe=Frame(self.root,bd=3,relief=RIDGE,)
        Coustomerframe.place(x=420,y=110,width=530,height=80)

        C_tile=Label(Coustomerframe, text="Costomer Detalis",font=("Gil Sans",15,"bold"), bg="black",fg="white").pack(side=TOP,fill=X)
        
        lbl_name=Label(Coustomerframe,text="Name",font=("times new roman",15),bg="white",).place(x=5,y=35)
        lbl_txt=Entry(Coustomerframe,text=self.var_cname,font=("times new roman",15,),bg="light yellow",).place(x=80,y=35,width=160)
        
        lbl_name=Label(Coustomerframe,text="ContactNo.",font=("times new roman",15,),bg="white",).place(x=260,y=35)
        lbl_txt=Entry(Coustomerframe,text=self.var_Contact,font=("times new roman",15,),bg="light yellow",).place(x=360,y=35,width=160)
        
        Cal_Cart_frame=Frame(self.root,bd=2,relief=RIDGE,)
        Cal_Cart_frame.place(x=420,y=190,width=530,height=500)
        
        # ======calculator frame======
        self.cal_input=StringVar()
        
        Calcu_frame=Frame(Cal_Cart_frame,bd=9,relief=RIDGE,)
        Calcu_frame.place(x=5,y=10,width=268,height=375)
        
        txt_cal_input=Entry(Calcu_frame,textvariable=self.cal_input,font=('arial',15,'bold'),width=21,bd=10,relief=GROOVE,state="readonly",justify=RIGHT)
        txt_cal_input.grid(row=0,columnspan=4)
     
        btn7=Button(Calcu_frame,text='7',font=('arial',15,'bold'),bd=5,width=4,pady=8,cursor='hand2',command=lambda:self.get_input(7)).grid(row=1,column=0)
        btn8=Button(Calcu_frame,text='8',font=('arial',15,'bold'),bd=5,width=4,pady=8,cursor='hand2',command=lambda:self.get_input(8)).grid(row=1,column=1)
        btn9=Button(Calcu_frame,text='9',font=('arial',15,'bold'),bd=5,width=4,pady=8,cursor='hand2',command=lambda:self.get_input(9)).grid(row=1,column=2)
        btnmul=Button(Calcu_frame,text='×',font=('arial',15,'bold'),bd=5,width=4,pady=8,cursor='hand2',command=lambda:self.get_input('*')).grid(row=1,column=3)
       
        btn4=Button(Calcu_frame,text='4',font=('arial',15,'bold'),bd=5,width=4,pady=8,cursor='hand2',command=lambda:self.get_input(4)).grid(row=2,column=0)
        btn5=Button(Calcu_frame,text='5',font=('arial',15,'bold'),bd=5,width=4,pady=8,cursor='hand2',command=lambda:self.get_input(5)).grid(row=2,column=1)
        btn6=Button(Calcu_frame,text='6',font=('arial',15,'bold'),bd=5,width=4,pady=8,cursor='hand2',command=lambda:self.get_input(6)).grid(row=2,column=2)
        btndiv=Button(Calcu_frame,text='÷',font=('arial',15,'bold'),bd=5,width=4,pady=8,cursor='hand2',command=lambda:self.get_input('/')).grid(row=2,column=3)

        btn1=Button(Calcu_frame,text='1',font=('arial',15,'bold'),bd=5,width=4,pady=8,cursor='hand2',command=lambda:self.get_input(1)).grid(row=3,column=0)
        btn2=Button(Calcu_frame,text='2',font=('arial',15,'bold'),bd=5,width=4,pady=8,cursor='hand2',command=lambda:self.get_input(2)).grid(row=3,column=1)
        btn3=Button(Calcu_frame,text='3',font=('arial',15,'bold'),bd=5,width=4,pady=8,cursor='hand2',command=lambda:self.get_input(3)).grid(row=3,column=2)
        btnminus=Button(Calcu_frame,text='-',font=('arial',15,'bold'),bd=5,width=4,pady=8,cursor='hand2',command=lambda:self.get_input('-')).grid(row=3,column=3)

        btn0=Button(Calcu_frame,text='0',font=('arial',15,'bold'),bd=5,width=4,pady=8,cursor='hand2',command=lambda:self.get_input(0)).grid(row=4,column=0)
        btndecimal=Button(Calcu_frame,text='.',font=('arial',15,'bold'),bd=5,width=4,pady=8,cursor='hand2',command=lambda:self.get_input('.')).grid(row=4,column=1)
        btnbracket=Button(Calcu_frame,text='(',font=('arial',15,'bold'),bd=5,width=4,pady=8,cursor='hand2',command=lambda:self.get_input('(')).grid(row=4,column=2)
        btnadd=Button(Calcu_frame,text='+',font=('arial',15,'bold'),bd=5,width=4,pady=8,cursor='hand2',command=lambda:self.get_input('+')).grid(row=4,column=3)
        
        btnpercentage=Button(Calcu_frame,text='%',font=('arial',15,'bold'),bd=5,width=4,pady=8,cursor='hand2',command=self.find_percentage).grid(row=5,column=0)
        btnclear=Button(Calcu_frame,text='C',font=('arial',15,'bold'),bd=5,width=4,pady=8,cursor='hand2',command=self.clear_cal).grid(row=5,column=1)
        btnBracket=Button(Calcu_frame,text=')',font=('arial',15,'bold'),bd=5,width=4,pady=8,cursor='hand2',command=lambda:self.get_input(')')).grid(row=5,column=2)
        btnequal=Button(Calcu_frame,text='=',font=('arial',15,'bold'),bd=5,width=4,pady=8,cursor='hand2',command=self.perform_cal).grid(row=5,column=3)

        
        # =======cart frame====

        Cart_frame=Frame(Cal_Cart_frame,bd=3,relief=RIDGE,)
        Cart_frame.place(x=280,y=8,width=245,height=342)

        self.Cart_tile=Label(Cart_frame, text="Cart \tTotal Products:[0]",font=("Gil Sans",13,), bg="Light grey")
        self.Cart_tile.pack(side=TOP,fill=X)

        scrollx=Scrollbar(Cart_frame,orient=HORIZONTAL)
        scrolly=Scrollbar(Cart_frame,orient=VERTICAL)

        self.CartTable=ttk.Treeview(Cart_frame,columns=("Pid","Name","Price","Qty","Stock"),yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM,fill=X)
        scrolly.pack(side=RIGHT,fill=Y)
        scrollx.config(command=self.CartTable.xview)
        scrolly.config(command=self.CartTable.yview)

        self.CartTable.heading("Pid",text="Pid")
        self.CartTable.heading("Name",text="Name")
        self.CartTable.heading("Price",text="Price")
        self.CartTable.heading("Qty",text="Qty")
        self.CartTable.heading("Stock", text="Stock")
        self.CartTable["show"]="headings"
        self.CartTable.column("Pid",width=40)
        self.CartTable.column("Name",width=100)
        self.CartTable.column("Price",width=90)
        self.CartTable.column("Qty",width=40)
        self.CartTable.column("Stock", width=60)
        self.CartTable.pack(fill=BOTH,expand=1)
        self.CartTable.bind("<ButtonRelease-1>",self.get_datacart)
        self.show()


        # ==================Add cart frame===========
        self.var_Pid=StringVar()
        self.var_pname=StringVar()
        self.var_price=StringVar()
        self.var_Quan=StringVar()
        self.var_Stock=StringVar()

        addcartwidget_frame=Frame(self.root,bd=2,relief=RIDGE,)
        addcartwidget_frame.place(x=420,y=575,width=530,height=110)

        p_name=Label(addcartwidget_frame,text="Product Name",font=("times new roman",15,),bg="white",).place(x=5,y=5)
        txt_p_name=Entry(addcartwidget_frame,text=self.var_pname,font=("times new roman",15,),bg="light yellow",state="readonly").place(x=5,y=35,width=190,height=22)
        
        price_name=Label(addcartwidget_frame,text="Price per Qty",font=("times new roman",15,),bg="white",).place(x=220,y=5)
        txt_price_name=Entry(addcartwidget_frame,text=self.var_price,font=("times new roman",15,),bg="light yellow",state="readonly").place(x=220,y=35,width=150,height=22)

        Qty_name=Label(addcartwidget_frame,text="Qty",font=("times new roman",15,),bg="white",).place(x=390,y=5)
        txt_Qty_name=Entry(addcartwidget_frame,text=self.var_Quan,font=("times new roman",15,),bg="light yellow").place(x=390,y=35,width=120,height=22)

        self.lbl_instock=Label(addcartwidget_frame,text="In Stock",font=("times new roman",15,),bg="white",)
        self.lbl_instock.place(x=5,y=70)

        btn_clear=Button(addcartwidget_frame,text="Clear",font=("Gil Sans",15,),bg="light blue",cursor="hand2",command=self.clearcart).place(x=180,y=70,width=150,height=30)
        btn_add=Button(addcartwidget_frame,text="ADD|Update Cart",command=self.add_update_cart,font=("Gil Sans",15,),bg="orange",cursor="hand2").place(x=340,y=70,width=180,height=30)
         


    # =========================================Billing frame==========================
    
        bill_frame=Frame(self.root,bd=3,relief=RIDGE,)
        bill_frame.place(x=950,y=110,width=410,height=440)

        bill_tile=Label(bill_frame, text="Customer Bill",font=("Gil Sans",20,"bold"), bg="black",fg="white").pack(side=TOP,fill=X)

        scrolly2=Scrollbar(bill_frame,orient=VERTICAL)
        scrolly2.pack(side=RIGHT,fill=Y)
        self.txt_bill_area=Text(bill_frame,yscrollcommand=scrolly2.set)
        self.txt_bill_area.pack(fill=BOTH,expand=1)
        scrolly2.config(command=self.txt_bill_area.yview)


        # ===========bill button=========
        
        billMenu_frame=Frame(self.root,bd=3,relief=RIDGE,)
        billMenu_frame.place(x=950,y=550,width=410,height=140)

        self.lbl_amount=Label(billMenu_frame,text="Bill Amount\n[0]",font=('goudy old style',15,"bold"),fg='white',bg='black')
        self.lbl_amount.place(x=2,y=3,width=120,height=70)
        
        self.lbl_Discount=Label(billMenu_frame,text="Discount\n[5%]",font=('goudy old style',15,"bold"),fg='white',bg='black')
        self.lbl_Discount.place(x=124,y=3,width=120,height=70)
       
        self.lbl_netpay=Label(billMenu_frame,text="Net Pay\n[0]",font=('goudy old style',15,"bold"),fg='white',bg='black')
        self.lbl_netpay.place(x=246,y=3,width=160,height=70)
        
        btn_lbl_print=Button(billMenu_frame,text="Print",font=('goudy old style',15,"bold"),fg='Black',bg='orange',cursor='hand2')
        btn_lbl_print.place(x=2,y=75,width=120,height=59)
        
        btn_lbl_clearall=Button(billMenu_frame,text="Clear All",font=('goudy old style',15,"bold"),fg='black',bg='light blue',cursor='hand2',command=self.clearall)
        btn_lbl_clearall.place(x=124,y=75,width=120,height=59)
       
        btn_lbl_generate=Button(billMenu_frame,text="Generate/Save Bill",command=self.generate_bill,font=('goudy old style',15,"bold"),fg='black',bg='green',cursor='hand2')
        btn_lbl_generate.place(x=246,y=75,width=160,height=59)

        self.show()
        
       

# ===============All fucntions======
    def get_input(self,num):
        xnum=self.cal_input.get()+str(num)
        self.cal_input.set(xnum)

    def clear_cal(self):
        self.cal_input.set('')

    def perform_cal(self):
        try:
            result=self.cal_input.get()
            self.cal_input.set(eval(result))

        except Exception as e:
            self.cal_input.set("Invalid Format")





    def show(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            cur.execute("select Pid,Name,Price,Quantity from product")
            rows=cur.fetchall()
            self.Producttable.delete(*self.Producttable.get_children())
            for i in rows:
                self.Producttable.insert('',END,values=i)
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to {str(ex)}",parent=self.root)

    
    def search(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            if self.var_search.get()=="":
                messagebox.showerror("Error","Search input should be required")
            else:
                cur.execute("Select Pid,Name,Price,Quantity from Product where Name LIKE '%"+self.var_search.get()+"%'")
                rows=cur.fetchall()
                if len(rows)!=0:
                    self.Producttable.delete(*self.Producttable.get_children())
                    for row in rows:
                        self.Producttable.insert('' , END,values=row)
                else:
                    messagebox.showerror("Error","No record found!!!",parent=self.root)

        except Exception as ex:
            messagebox.showerror("Error",f"Error due to: {str(ex)}")

    def get_data(self,ev):
        f=self.Producttable.focus()
        content=(self.Producttable.item(f))
        row=content["values"]
        self.var_Pid.set(row[0])
        self.var_pname.set(row[1])
        self.var_price.set(row[2])
        self.var_Stock.set(row[3])
        self.lbl_instock.config(text=f"In Stock [{str(row[3])}]")
    
    def get_datacart(self,ev):
        f=self.CartTable.focus()
        content=(self.CartTable.item(f))
        row=content["values"]
        self.var_Pid.set(row[0])
        self.var_pname.set(row[1])
        self.var_price.set(row[2])
        self.var_Quan.set(row[3])
        self.var_Stock.set(row[4])
        self.lbl_instock.config(text=f"In Stock [{str(row[4])}]")


    def add_update_cart(self):
        if self.var_Quan.get()=="":
            messagebox.showerror("Error","Enter Quantity first", parent=self.root)
        elif self.var_Pid.get()=="":
            messagebox.showerror("Error","Product toh select kar bhai", parent=self.root)
        elif int(self.var_Quan.get())>int(self.var_Stock.get()):
                messagebox.showerror("Error","insufficient Quantity in stock")
        else:
            # price_calculate=int(self.var_Quan.get())*float(self.var_price.get())
            # price_calculate=float(price_calculate)
            
            price_calculate=self.var_price.get()
            carddata=[self.var_Pid.get(),self.var_pname.get(),price_calculate,self.var_Quan.get(),self.var_Stock.get()]
            # =========update=========
            present='no'
            index=0
            for i in self.cartlist:
                if self.var_Pid.get()==i[0]:
                    present='yes'
                    break
                index+=1
            if present=='yes':
                op=messagebox.askyesno('Confirm',"Product is already there\n aapko update ya remove karna hai? ")
                if op==True:
                    if self.var_Quan.get()=="0":
                        self.cartlist.pop(index)
                    else:
                        # self.cartlist[index][2]=price_calculate
                        self.cartlist[index][3]=self.var_Quan.get()
                        
            else:    
                self.cartlist.append(carddata)
            self.show_cart()
            self.bill_updates()

    def bill_updates(self):
        self.billamount=0
        self.net_pay=0
        self.discount=0
        for row in self.cartlist:
            self.billamount=self.billamount+(float(row[2])*int(row[3]))
        self.discount=(self.billamount*5)/100
        self.net_pay=self.billamount-(self.discount)
        self.lbl_amount.config(text=f'Bill Amnt(Rs.)\n[{str(self.billamount)}]')    
        self.lbl_netpay.config(text=f'Net Pay(Rs.)\n[{str(self.net_pay)}]')    
        self.Cart_tile.config(text=f"Cart \tTotal Products:[{str(len(self.cartlist))}]")
            

        
    def show_cart(self):
        try:
            self.CartTable.delete(*self.CartTable.get_children())
            for i in self.cartlist:
                self.CartTable.insert('',END,values=i)
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to {str(ex)}",parent=self.root)

    def find_percentage(self):
        try:
            val = float(self.cal_input.get())
            percent = val / 100
            self.cal_input.set(str(percent))
        except:
            self.cal_input.set("Error")

    def generate_bill(self):
        if self.var_cname.get()=='' or  self.var_Contact.get()=='':
            messagebox.showerror("Error","ग्राहक का नाम और संपर्क नंबर. आवश्यक है",parent=self.root)
        elif len(self.cartlist)==0:
             messagebox.showerror("Error","कृपया अपने कार्ट में उत्पाद जोड़ें",parent=self.root)

        else:

            # =====Billtop=====
            self.bill_top()
            # =====Billmid=====
            self.bill_mid()
            # =====Billbottom=====
            self.bill_bottom()
            # ====Qrcode====
            self.Qrcode()
            
            # fp=open(f"bill/{str(self.invoice)}.txt",'w')
            # fp.write(self.txt_bill_area.get('1.0',END))
            # fp.close()

            # === saving bill ===
            con=sqlite3.connect(database=r'ims.db')
            cur=con.cursor()
            for i in self.cartlist:
                Pid=i[0]
                name=i[2]
                quantity=i[3]
                cur.execute("SELECT Category FROM Product WHERE Pid = ?", (Pid,))
                category = cur.fetchone()[0]

                sale_date = time.strftime("%d%m%Y")


                cur.execute("""
                INSERT INTO CategorySales (P_Id, Category_name, Quantity_sold, Sale_Date)
                VALUES (?, ?, ?, ?)
            """, (Pid, category, quantity, sale_date))
                
            con.commit()
            con.close()

        self.export_sales_to_excel()

    def bill_top(self):
        self.invoice=int(time.strftime("%H%M%S"))+int(time.strftime("%d%m%Y"))
        bill_top=f'''
\t\t Bill of Supply
\t      Your Inventory
 Phone No.=9837217569 , \t\tAgra 282005
 Gst no.=AGFTRXXXXXXX
{str("-"*47)}
 Customer Name: {self.var_cname.get()}
 Contact No.: {self.var_Contact.get()}
 Bill No: {str(self.invoice)}\t\t\tDate:{str(time.strftime("%d/%m/%Y"))}
 {str("-"*46)}
 Product Name:\t\t\tQty\tPrice
 {str("-"*46)}
        '''
        self.txt_bill_area.delete('1.0',END)
        self.txt_bill_area.insert('1.0',bill_top)

    def bill_mid(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:  
            for i in self.cartlist:
                Pid=i[0]
                name=i[1]
                qty=int(i[4])-int(i[3])
                # if int(Qty)==int(i[4]):
                #     status='Inactive'
                # if int(Qty)!=int(i[4]):
                #     status='Active'
                price=float(i[2])*int(i[3])
                price=str(price)
                self.txt_bill_area.insert(END,"\n"+name+"\t\t\t"+i[3]+"\tRs."+price)

                # ===============update qty in product table=====
                cur.execute("Update Product set Quantity=? where Pid=?",(
                    qty,
                    Pid
                    ))
                con.commit()
            con.close()
            self.show()
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to {str(ex)}",parent=self.root)
    
    
    def bill_bottom(self):
        billtemp=f'''
{str("-")*47}
 Bill Amount\t\t\tRs.{self.billamount}
 Discount\t\t\tRs.{self.discount}
 Net Pay\t\t\tRs.{self.net_pay}
{str("-")*47}
        '''
        self.txt_bill_area.insert(END,billtemp)

    def clearcart(self):
        self.var_Pid.set('')
        self.var_pname.set('')
        self.var_price.set('')
        self.var_Quan.set('')
        self.var_Stock.set('')
        self.lbl_instock.config(text=f"In Stock")

    def clearall(self): 
        del self.cartlist[:]
        self.var_cname.set('')
        self.var_Contact.set('')
        self.txt_bill_area.delete('1.0',END)
        self.var_search.set('')
        self.clearcart()
        self.show()
        self.show_cart()
        self.Cart_tile.config(text=f"Cart \tTotal Products:[0]")

    def Qrcode(self):
        self.Upi_id="gurumukhdass1989@okicici"
        phonepay_url=f"upi://pay?pa={self.Upi_id}&pn=Gurumukhdass%20Fashions&am={self.net_pay}"
        paytm_url=f"upi://pay?pa={self.Upi_id}$pn=Gurumukhdass%20Fashions&am={self.net_pay}"
        googlepay_url=f"upi://pay?pa={self.Upi_id}$pn=Gurumukhdass%20Fashions&am={self.net_pay}"

        # ===create qr code===
        self.phoenpay_qr=qrcode.make(phonepay_url)
        self.paytm_qr=qrcode.make(paytm_url)
        self.googlepay_qr=qrcode.make(googlepay_url)

        # =====display qr code====
        self.phoenpay_qr.show(),
        self.googlepay_qr.show(),
        self.paytm_qr.show()

    def export_sales_to_excel(self):
        con = sqlite3.connect("ims.db")
        df = pd.read_sql_query("SELECT * FROM Categorysales", con)
        df.to_excel("Categorysales.xlsx", index=False)
        con.close()








        
        


if __name__=="__main__":
    root=Tk()
    obj=Billing(root)
    root.mainloop()