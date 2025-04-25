from tkinter import*
from  PIL import Image
from tkinter import ttk,messagebox
import sqlite3
class Categoryclass:
    def __init__(self,root):
        self.root=root
        self.root.geometry("1100x500+220+130")
        self.root.title("Business Management Syestem | developed by Grp-102 | Nikhil Multani")
        self.root.config(bg="white")
        self.root.focus_force()

        # =====variable======
        self.var_catid=StringVar()
        self.var_name=StringVar()

    # ======searchframe=======
        tile=Label(self.root,text="Manage Product Category" , font=("Gil Sans",30,), bg="black",fg="white",bd=3,relief=RIDGE).pack(side=TOP,fill=X,padx=10,pady=10)
        tilename=Label(self.root,text="Enter Category Name" , font=("Gil Sans",30,), bg="black",fg="white",).place(x=50,y=100,width=400)
        Name_cat=Entry(self.root,text=self.var_name,font=("Gil Sans",20,),bg="light yellow").place(x=50,y=170,width=300)
        btn_add=Button(self.root,text="ADD",command=self.add,font=("Gil Sans",20,),bg="Green",cursor="hand2").place(x=360,y=170,width=150,height=30)
        btn_delete=Button(self.root,text="Delete",font=("Gil Sans",20,),bg="red",cursor="hand2",command=self.Delete).place(x=520,y=170,width=150,height=30)

        # =======category detLIS======
        cat_frame=Frame(self.root,bd=3,relief=RIDGE)
        cat_frame.place(x=700,y=100,width=380,height=350)

        scrollx=Scrollbar(cat_frame,orient=HORIZONTAL)
        scrolly=Scrollbar(cat_frame,orient=VERTICAL)

        self.categoryTable=ttk.Treeview(cat_frame,columns=("C-ID","Name"),yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM,fill=X)
        scrolly.pack(side=RIGHT,fill=Y)
        scrollx.config(command=self.categoryTable.xview)
        scrolly.config(command=self.categoryTable.yview)

        self.categoryTable.heading("C-ID",text="C-ID")
        self.categoryTable.heading("Name",text="Name")
        self.categoryTable["show"]="headings"
        self.categoryTable.column("C-ID",width=90)
        self.categoryTable.column("Name",width=180)
        self.categoryTable.pack(fill=BOTH,expand=1)
        self.show()
        # ==============function of add and delete=============
        
    def add(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            if self.var_name.get()=="":
                messagebox.showerror("Error", "Category name must required",parent=self.root)
            else:
                cur.execute("Select * from category where Name=?",(self.var_name.get(),))
                row=cur.fetchone()
                if row!=None:
                    messagebox.showerror("Eroor","Category already present",parent=self.root)
                else:
                    cur.execute("Insert into category (Name) values(?)",(self.var_name.get(),))
                    con.commit()
                    messagebox.showinfo("Success","category added successfully",parent=self.root)
                    self.show()

        except Exception as ex:
            messagebox.showerror("Error",f"Error due to: {str(ex)}")


    def show(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()

        try:
            cur.execute("select * from category")
            rows=cur.fetchall()
            self.categoryTable.delete(*self.categoryTable.get_children())
            for i in rows:
                self.categoryTable.insert('',END,values=i)
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to {str(ex)}",parent=self.root)
    
    def Delete(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            if self.var_name.get()=="":
                messagebox.showerror("Error", "Category name must required to Delete something",parent=self.root)
            else:
                cur.execute("Select * from category where Name=",(self.var_name.get(),))
                row=cur.fetchone()
                if row!=None:
                    messagebox.showerror("Eroor","Category already present",parent=self.root)
                else:
                    cur.execute("Insert into category (Name) values(?)",(self.var_name.get(),))
                    con.commit()
                    messagebox.showinfo("Success","category added successfully",parent=self.root)
                    self.show()
                    
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to: {str(ex)}")
    
        

if __name__=="__main__":
    root=Tk()
    obj=Categoryclass(root)
    root.mainloop()