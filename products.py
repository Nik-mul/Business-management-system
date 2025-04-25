from tkinter import*
from  PIL import Image
from tkinter import ttk,messagebox
import sqlite3
class productclass:
    def __init__(self,root):
        self.root=root
        self.root.geometry("1100x500+220+130")
        self.root.title("Business Management Syestem | developed by Grp-No.-102 | Nikhil Multani")
        self.root.config(bg="white")
        self.root.focus_force()

        # ========var=======
        self.var_cat=StringVar()
        self.var_supp=StringVar()
        self.var_Pid=StringVar()
        self.cat_list=[]
        self.com_list=[]
        self.fetch_cat_and_supp()
        self.var_proname=StringVar()
        self.var_price=StringVar()
        self.var_Quan=StringVar()
        self.var_stat=StringVar()
        self.var_searchby=StringVar()
        self.var_searchtxt=StringVar()

        # =======Productsframe======
        pro_frame=Frame(self.root,bd=2,relief=RIDGE,bg="white")
        pro_frame.place(x=10,y=10,height=480,width=450)

        tile=Label(pro_frame,text="Manage Product Details" , font=("Gil Sans",30,), bg="black",fg="white",bd=3,relief=RIDGE).pack(side=TOP,fill=X,padx=10)
        label_supp=Label(pro_frame,text="Company" , font=("Gil Sans",18,),bg="white",fg="black").place(x=30,y=110)
        label_cat=Label(pro_frame,text="Category" , font=("Gil Sans",18,),bg="white",fg="black").place(x=30,y=60)
        label_product=Label(pro_frame,text="Pro Name" , font=("Gil Sans",18,),bg="white",fg="black").place(x=30,y=160)
        label_price=Label(pro_frame,text="Price" , font=("Gil Sans",18,),bg="white",fg="black").place(x=30,y=210)
        label_quan=Label(pro_frame,text="Quantity" , font=("Gil Sans",18,),bg="white",fg="black").place(x=30,y=260)
        label_stat=Label(pro_frame,text="Status" , font=("Gil Sans",18,),bg="white",fg="black").place(x=30,y=310)

        # ===options=====
        cmb_cat=ttk.Combobox(pro_frame,text=self.var_cat,values=self.cat_list,state="readonly", justify=CENTER,font=("Gil Sans",15,))
        cmb_cat.place(x=150,y=60,width=200)
        cmb_cat.current(0)
        
        cmb_supp=ttk.Combobox(pro_frame,text=self.var_supp,values=self.com_list,state="readonly", justify=CENTER,font=("Gil Sans",15,))
        cmb_supp.place(x=150,y=110,width=200)
        cmb_supp.current(0)

        Name_pro=Entry(pro_frame,text=self.var_proname,font=("Gil Sans",15,),bg="light yellow").place(x=150,y=160,width=200)
        Name_price=Entry(pro_frame,text=self.var_price,font=("Gil Sans",15,),bg="light yellow").place(x=150,y=210,width=200)
        Name_quan=Entry(pro_frame,text=self.var_Quan,font=("Gil Sans",15,),bg="light yellow").place(x=150,y=260,width=200)

        # ======button=====
        btn_add=Button(self.root,text="ADD",font=("Gil Sans",20,),command=self.add,bg="Green",cursor="hand2").place(x=10,y=400,width=100,height=40)
        btn_delete=Button(self.root,text="Delete",font=("Gil Sans",20,),command=self.Delete,bg="red",cursor="hand2").place(x=120,y=400,width=100,height=40)
        btn_update=Button(self.root,text="Update",font=("Gil Sans",20,),command=self.update,bg="Yellow",cursor="hand2").place(x=230,y=400,width=100,height=40)
        btn_clear=Button(self.root,text="Clear",font=("Gil Sans",20,),command=self.clear,bg="light blue",cursor="hand2").place(x=340,y=400,width=100,height=40)

        # ============searchbar========
        Searchframe=LabelFrame(self.root,text="Search Products",font=("Gills sans",12,"bold"),bd=2,relief=RIDGE)
        Searchframe.place(x=480,y=10,width=600,height=80)

        # =======option of search bar=====
        cmb_search=ttk.Combobox(Searchframe,textvariable=self.var_searchby,font=("Gills sans",12,"bold"),values=("Select","Category","Company","Name"))
        cmb_search.place(x=10,y=10,width=180)
        cmb_search.current(0)

        txtsearch=Entry(Searchframe,textvariable=self.var_searchtxt,font=("Gills sans",12,"bold"),bg="light yellow").place(x=250,y=10,width=180)
        btnsearch=Button(Searchframe,text="Search",command=self.search,font=("Gills Sans",18,"bold")).place(x=440,y=5,width=120,height=30)


        # ========productsdetails======
        p_frame=Frame(self.root,bd=3,relief=RIDGE,)
        p_frame.place(x=480,y=100,width=600,height=390)

        scrollx=Scrollbar(p_frame,orient=HORIZONTAL)
        scrolly=Scrollbar(p_frame,orient=VERTICAL)

        self.ProductTable=ttk.Treeview(p_frame,columns=("Pid","Company","Category","Name","Price","Quantity"),yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM,fill=X)
        scrolly.pack(side=RIGHT,fill=Y)
        scrollx.config(command=self.ProductTable.xview)
        scrolly.config(command=self.ProductTable.yview)

        self.ProductTable.heading("Pid",text="Pid")
        self.ProductTable.heading("Company",text="Company")
        self.ProductTable.heading("Category",text="Category")
        self.ProductTable.heading("Name",text="Name")
        self.ProductTable.heading("Price",text="Price")
        self.ProductTable.heading("Quantity",text="Quantity")
        self.ProductTable["show"]="headings"
        self.ProductTable.column("Pid",width=90)
        self.ProductTable.column("Company",width=90)
        self.ProductTable.column("Category",width=90)
        self.ProductTable.column("Name",width=90)
        self.ProductTable.column("Price",width=90)
        self.ProductTable.column("Quantity",width=90)
        self.ProductTable.pack(fill=BOTH,expand=1)
        self.ProductTable.bind("<ButtonRelease-1>",self.get_data)
        self.show()
        

        # =========function of button======
    def show(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()

        try:
            cur.execute("select * from product")
            rows=cur.fetchall()
            self.ProductTable.delete(*self.ProductTable.get_children())
            for i in rows:
                self.ProductTable.insert('',END,values=i)
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to {str(ex)}",parent=self.root)

    def fetch_cat_and_supp(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            cur.execute("Select Name from Category")
            cat=cur.fetchall()
            self.cat_list.append("Empty")
            if len(cat)>0:
                del self.cat_list [:]
                self.cat_list.append("Select")
                for i in cat:
                    self.cat_list.append(i[0])
            cur.execute("Select Name from Company")
            com=cur.fetchall()
            self.com_list.append("Empty")
            if len(com)>0:
                del self.com_list [:]
                self.com_list.append("Select")
                for i in com:
                    self.com_list.append(i[0])

          
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to: {str(ex)}")

    

    def add(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            if self.var_cat.get()=="Select" or self.var_supp=="Select" or self.var_proname=="":
                messagebox.showerror("Error", "Product with category and Company name must be required",parent=self.root)
            else:
                cur.execute("Select * from Product where name=?",(self.var_proname.get(),))
                row=cur.fetchone()
                if row!=None:
                    messagebox.showerror("Error"," Product already present",parent=self.root)
                else:
                    cur.execute("Insert into Product (Company,Category,Name,Price,Quantity) values(?,?,?,?,?)",(
                        self.var_cat.get(),
                        self.var_supp.get(),
                        self.var_proname.get(),
                        self.var_price.get(),
                        self.var_Quan.get(),
                        ))
                    con.commit()
                    messagebox.showinfo("Success","Product added successfully",parent=self.root)
                    self.show()

        except Exception as ex:
            messagebox.showerror("Error",f"Error due to: {str(ex)}")

    def get_data(self,ev):
        f=self.ProductTable.focus()
        content=(self.ProductTable.item(f))
        row=content["values"]
        self.var_Pid.set(row[0]),
        self.var_supp.set(row[2]),
        self.var_cat.set(row[1]),
        self.var_proname.set(row[3]),
        self.var_price.set(row[4]),
        self.var_Quan.set(row[5]),

    def update(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            if self.var_Pid.get()=="":
                messagebox.showerror("Error","Please Select product from list",parent=self.root)
            else:
                cur.execute("Select* from product where pid=?",(self.var_Pid.get(),))
                row=cur.fetchone()
                if row==None:
                    messagebox.showerror("Error"," Invalid Product Id",parent=self.root)

                else:
                    cur.execute("Update product set Category=?,Company=?,Name=?,Price=?,Quantity=? where Pid=?",(
                        self.var_supp.get(),
                        self.var_cat.get(),
                        self.var_proname.get(),
                        self.var_price.get(),
                        self.var_Quan.get(),
                        self.var_Pid.get(),
                        ))
                    con.commit()
                    messagebox.showinfo("Success", "Product updated successfully",parent=self.root)
                    self.show()
        

        
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to: {str(ex)}",parent=self.root)

    def clear(self):
        self.var_Pid.set(""),
        self.var_supp.set("Select"),
        self.var_cat.set("Select"),
        self.var_proname.set(""),
        self.var_price.set(""),
        self.var_Quan.set("")  
        self.var_searchtxt.set("") 
        self.var_searchby.set("Select")
        self.show() 
        
        
    def Delete(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            if self.var_Pid.get()=="":
                messagebox.showerror("Error","Please Select product from list",parent=self.root)
            else:
                cur.execute("Select* from product where pid=?",[self.var_Pid.get()],)
                row=cur.fetchone()
                if row==None:
                    messagebox.showerror("Error"," Invalid Product Id",parent=self.root)
                else:
                    op=messagebox.askyesno("Confirm","Do you want to delete?",parent=self.root)
                    if op==True:
                        cur.execute("Delete from product where Pid=?",(
                            self.var_Pid.get(),
                            ))
                        con.commit()
                        messagebox.showinfo("Succes", "Product Deleted successfully")
                        self.clear()
        

        except Exception as ex:
            messagebox.showerror("Error",f"Error due to: {str(ex)}")

    def search(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            if self.var_searchby=="Select" :
                messagebox.showerror("Error", "Select search by options",parent=self.root)
            elif self.var_searchtxt=="":
                messagebox.showerror("Error","Search input should be required")
            else:
                cur.execute("Select * from Product where"+self.var_searchby.get()+"LIKE '%" +self.var_searchtxt.get()+"'%")
                rows=cur.fetchall()
                if len(rows)!=0:
                    self.ProductTable.delete(*self.ProductTable.get_children())
                    for row in rows:
                        self.ProductTable.insert('' , END,values=row)
                else:
                    messagebox.showerror("Error","No record found!!!",parent=self.root)

        except Exception as ex:
            messagebox.showerror("Error",f"Error due to: {str(ex)}")


    


if __name__=="__main__":
    root=Tk()
    obj=productclass(root)
    root.mainloop()