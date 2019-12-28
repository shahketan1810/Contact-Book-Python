from Tkinter import *
from tkMessageBox import *
import sqlite3
root1=Tk()
def close(e=1):
    root1.destroy()
    
#intro
root1.geometry("800x300")      
Label(root1,text='Project : Phone Book',font='times 20 bold').grid(row=0,column=0)
Label(root1,text='Project of Python and Database',font='times 20 bold').grid(row=2,column=1)
Label(root1,text='Name : Ketan Shah',font='Arial 20').grid(row=3,column=1)
Label(root1,text='Enrollment no.: 181B109',font='Arial 20').grid(row=4,column=1)
Label(root1,text='Batch : B4',font='Arial 20').grid(row=5,column=1)
root1.bind('<Motion>',close)
root1.mainloop()

#create contact interface
root=Tk()
root.title('PhoneBook')
root.geometry("550x600")
con=sqlite3.Connection('pbdb')
cur=con.cursor()
cur.execute("create table if not exists detail(contactID Integer Primary Key  Autoincrement,fname Varchar(20),lname Varchar(20),company Varchar(20),address Varchar(40),city Varchar(20),PIN Number(6),web Varchar(20),dob date)") 
cur.execute("create table if not exists phone(contactID Integer,contype Varchar(20),Pno Integer,Foreign Key(contactID) references detail(contactID) on delete cascade)")
cur.execute("create table if not exists mail(contactID Integer,mtype Varchar(20),email Varchar(30),Foreign Key(contactID) references detail(contactID) on delete cascade)")
img = PhotoImage(file="pb.gif")
Label(root, image = img).grid(row=0,column=1)
Label(root,text='First Name').grid(row=1,column=0)
e1=Entry(root)
e1.grid(row=1,column=1)
Label(root,text='Last Name').grid(row=2,column=0)
e2=Entry(root)
e2.grid(row=2,column=1)
Label(root,text='Company Name').grid(row=3,column=0)
e3=Entry(root)
e3.grid(row=3,column=1)
Label(root,text='Address').grid(row=4,column=0)
e4=Entry(root)
e4.grid(row=4,column=1)
Label(root,text='City').grid(row=5,column=0)
e5=Entry(root)
e5.grid(row=5,column=1)
Label(root,text='Pin Code').grid(row=6,column=0)
e6=Entry(root)
e6.grid(row=6,column=1)
Label(root,text='Website URL').grid(row=7,column=0)
e7=Entry(root)
e7.grid(row=7,column=1)
Label(root,text='Date of Birth').grid(row=8,column=0)
e8=Entry(root)
e8.grid(row=8,column=1)
Label(root,text='(dd-mm-yyyy)',fg='red').grid(row=8,column=2)
Label(root,text='Select Phone Type :',font='Arial 12').grid(row=9,column=0)
v1=IntVar()
Radiobutton(root,text='Office',variable=v1,value=1).grid(row=9,column=1)
Radiobutton(root,text='Home',variable=v1,value=2).grid(row=9,column=2)
Radiobutton(root,text='Mobile',variable=v1,value=3).grid(row=9,column=3)
Label(root,text='Phone Number').grid(row=10,column=0)
e9=Entry(root)
e9.grid(row=10,column=1)
Label(root,text='Select Email Type :',font='Arial 12').grid(row=11,column=0)
v2=IntVar()
Radiobutton(root,text='Office',variable=v2,value=4).grid(row=11,column=1)
Radiobutton(root,text='Personal',variable=v2,value=5).grid(row=11,column=2)
Label(root,text='Email id').grid(row=12,column=0)
e10=Entry(root)
e10.grid(row=12,column=1)

#save function
def Save():
    if e1.get()==e2.get() and e1.get()!='' and e2.get()!='':
        showinfo('Name Error','Contact cannot be Saved because no one has same first name and last name')
        return
    elif(e1.get()=='' and e2.get()=='' and e3.get()=='' and e4.get()=='' and e5.get()=='' and e6.get()=='' and e7.get()=='' and e8.get()=='' and e9.get()=='' and e10.get()==''):
        showerror('Error','Enter atleast one field to save a contact')
        return
    elif(e5.get().isdigit()):
        showerror('City Error','City name should be in characters')
        return
    else:
        if len(e6.get())!=0:                
            pin=e6.get().isdigit()
            if(pin==False and len(e6.get())!=6):
                showerror('PinCode Error','Pincode should be a six digit number')
                return
        if v1.get()==1:
            ptype='Office'
        if v1.get()==2:
            ptype='Home'
        if v1.get()==3:
            ptype='Mobile'
        if v1.get()!=1 and v1.get()!=2 and v1.get()!=3:
            ptype='Mobile'
        if v2.get()==4:
            etype='Office'
        if v2.get()==5:
            etype='Personal'
        if v2.get()!=4 and v2.get()!=5:
            etype='Personal'

        detail_data=(e1.get(),e2.get(),e3.get(),e4.get(),e5.get(),e6.get(),e7.get(),e8.get())
        phone_data=(ptype,e9.get())
        mail_data=(etype,e10.get())
        cur.execute("insert into detail(fname,lname,company,address,city,PIN,web,dob) values(?,?,?,?,?,?,?,?)",detail_data)
        cur.execute("insert into phone values((select max(contactID) from detail),?,?)",phone_data)
        cur.execute("insert into mail values((select max(contactID) from detail),?,?)",mail_data)
        e1.delete(0,END)
        e2.delete(0,END)
        e3.delete(0,END)
        e4.delete(0,END)
        e5.delete(0,END)
        e6.delete(0,END)
        e7.delete(0,END)
        e8.delete(0,END)
        e9.delete(0,END)
        e10.delete(0,END)
        v1.set(10)
        v2.set(8)
        con.commit()
        showinfo('Saved','Contact Saved Successfully')
        return

#search
def Search():
    def searchclose():
        showinfo('Closing!!','Exiting Search')
        root2.destroy()
                
    def namesearch(e=1):
        op.delete(0,END)
        cur.execute("select fname,lname from detail where fname like '%"+str(s.get())+"%' or lname like '%"+str(s.get())+"% order by fname'")
        x=cur.fetchall()
        for i in range(len(x)):
            y=str(x[i][0])+' '+str(x[i][1])
            op.insert(END,y)
        
    def printme(e=1):
        clicked_item=op.curselection()
        for item in clicked_item:
            c_name=op.get(item).split(' ')
            op.delete(0,END)
            cur.execute("select * from detail where fname like '%"+str(c_name[0])+"%' or lname like '%"+str(c_name[1])+"%'")
            a=cur.fetchall()
            cur.execute("select contactID from detail where fname like '%"+str(c_name[0])+"%' or lname like '%"+str(c_name[1])+"%'")
            d=cur.fetchall()
            d=d[0]
            cur.execute("select contype,Pno from phone where contactID=(?)",d)
            b=cur.fetchall()
            cur.execute("select mtype,email  from mail where contactID=(?)",d)
            c=cur.fetchall()
            
            def delete(e=1):
                cur.execute("delete from detail where contactID=(?)",d)
                showinfo('Delete','Contact Deleted Successfully')
                con.commit()
                root2.destroy()
                Search()
                return
            
            op.insert(END,'First Name : '+str(a[0][1]))
            op.insert(END,'Last Name : '+str(a[0][2]))
            op.insert(END,'Company : '+str(a[0][3]))
            op.insert(END,'Address : '+str(a[0][4]))
            op.insert(END,'City : '+str(a[0][5]))
            op.insert(END,'Pin Code : '+str(a[0][6]))
            op.insert(END,'Website : '+str(a[0][7]))
            op.insert(END,'Date of Birth : '+str(a[0][8]))
            op.insert(END,'Contact Type :'+str(b[0][0]))
            op.insert(END,'Phone no. :'+str(b[0][1]))
            op.insert(END,'Email Type :'+str(c[0][0]))
            op.insert(END,'Email ID :'+str(c[0][1]))
            Button(root2,text='Delete',bg='light yellow',command=delete).grid(row=3,column=0)
            
            
    root2=Tk()
    root2.title("Search")
    Label(root2,text='Search Bar : ',font='times 15 bold italic').grid(row=0,column=0)
    s=Entry(root2)
    s.grid(row=1,column=0)
    op=Listbox(root2,height=20,width=60,font='Arial',selectmode=SINGLE)
    op.grid(row=2,column=0)
    cur.execute("select fname,lname from detail")
    f=cur.fetchall()
    for j in range(len(f)):
        k=str(f[j][0])+' '+str(f[j][1])
        op.insert(END,k)
    root2.bind('<ButtonRelease-1>',printme)
    root2.bind('<KeyPress>',namesearch)
    Button(root2,text='Close',bg='light yellow',command=searchclose).grid(row=4,column=0)
    root2.mainloop()

#edit
def Edit():
    def updateclose():
        showinfo('Closing!!','Exiting Edit')
        root3.destroy()
        
    def namesearch(e=1):
        op.delete(0,END)
        cur.execute("select fname,lname from detail where fname like '%"+str(s.get())+"%' or lname like '%"+str(s.get())+"%'")
        x=cur.fetchall()
        for i in range(len(x)):
            y=str(x[i][0])+' '+str(x[i][1])
            op.insert(END,y)
        
    def printme(e=1):
        clicked_item=op.curselection()
        for item in clicked_item:
            c_name=op.get(item).split(' ')
            op.delete(0,END)
            cur.execute("select * from detail where fname like '%"+str(c_name[0])+"%' or lname like '%"+str(c_name[1])+"%'")
            a=cur.fetchall()
            cur.execute("select contactID from detail where fname like '%"+str(c_name[0])+"%' or lname like '%"+str(c_name[1])+"%'")
            d=cur.fetchall()
            d=d[0]
            cur.execute("select contype,Pno from phone where contactID=(?)",d)
            b=cur.fetchall()
            cur.execute("select mtype,email  from mail where contactID=(?)",d)
            c=cur.fetchall()
                
            def update():
                def realupdate():
                    g=d[0]
                    if e1.get()==e2.get() and e1.get()!='' and e2.get()!='':
                         showinfo('Name Error','Contact cannot be Saved because no one has same first name and last name')
                         return
                    elif(e1.get()=='' and e2.get()=='' and e3.get()=='' and e4.get()=='' and e5.get()=='' and e6.get()=='' and e7.get()=='' and e8.get()=='' and e9.get()=='' and e10.get()==''):
                        showerror('Error','Enter atleast one field to save a contact')
                        return
                    elif(e5.get().isdigit()):
                        showerror('City Error','City name should be in characters')
                        return
                    else:
                        if len(e6.get())!=0:                
                            pin=e6.get().isdigit()
                            if(pin==False and len(e6.get())!=6):
                                showerror('PinCode Error','Pincode should be a six digit number')
                                return

                    cur.execute("update detail set fname=(?),lname=(?),company=(?),address=(?),city=(?),PIN=(?),web=(?),dob=(?) where contactID=(?)",(e1.get(),e2.get(),e3.get(),e4.get(),e5.get(),e6.get(),e7.get(),e8.get(),g))
                    cur.execute("update phone set contype=(?),Pno=(?) where contactID=(?)",(ptype,e9.get(),g))                  
                    cur.execute("update mail set mtype=(?),email=(?) where contactID=(?)",(etype,e10.get(),g))
                    showinfo('Updated','Contact Updated Successfully')
                    con.commit()
                    root3.destroy()
                    root4.destroy()
                    Edit()
                    return
                
                root4=Tk()
                root4.title('Update')
                Label(root4,text='First Name').grid(row=1,column=0)
                e1=Entry(root4)
                e1.insert(0,a[0][1])
                e1.grid(row=1,column=1)
                Label(root4,text='Last Name').grid(row=2,column=0)
                e2=Entry(root4)
                e2.insert(0,a[0][2])
                e2.grid(row=2,column=1)
                Label(root4,text='Company Name').grid(row=3,column=0)    
                e3=Entry(root4)
                e3.insert(0,a[0][3])
                e3.grid(row=3,column=1)
                Label(root4,text='Address').grid(row=4,column=0)
                e4=Entry(root4)
                e4.insert(0,a[0][4])
                e4.grid(row=4,column=1)
                Label(root4,text='City').grid(row=5,column=0)
                e5=Entry(root4)
                e5.insert(0,a[0][5])
                e5.grid(row=5,column=1)
                Label(root4,text='Pin Code').grid(row=6,column=0)
                e6=Entry(root4)
                e6.insert(0,a[0][6])
                e6.grid(row=6,column=1)
                Label(root4,text='Website URL').grid(row=7,column=0)
                e7=Entry(root4)
                e7.insert(0,a[0][7])
                e7.grid(row=7,column=1)
                Label(root4,text='Date of Birth').grid(row=8,column=0)
                e8=Entry(root4)
                e8.insert(0,a[0][8])
                e8.grid(row=8,column=1)
                Label(root4,text='Select Phone Type :',font='Arial 10').grid(row=9,column=0)
                v1=IntVar()
                Radiobutton(root4,text='Office',variable=v1,value=1).grid(row=9,column=1)
                Radiobutton(root4,text='Home',variable=v1,value=2).grid(row=9,column=2)
                Radiobutton(root4,text='Mobile',variable=v1,value=3).grid(row=9,column=3)
                Label(root4,text='Phone Number').grid(row=10,column=0)
                e9=Entry(root4)
                e9.insert(0,b[0][1])
                e9.grid(row=10,column=1)
                Label(root4,text='Select Email Type :',font='Arial 10').grid(row=11,column=0)
                v2=IntVar()
                Radiobutton(root4,text='Office',variable=v2,value=4).grid(row=11,column=1)
                Radiobutton(root4,text='Personal',variable=v2,value=5).grid(row=11,column=2)
                Label(root4,text='Email id').grid(row=12,column=0)
                e10=Entry(root4)
                e10.insert(0,c[0][1])
                e10.grid(row=12,column=1)

                if v1.get()==1:
                    ptype='Office'
                if v1.get()==2:
                    ptype='Home'
                if v1.get()==3:
                    ptype='Mobile'
                if v1.get()!=1 and v1.get()!=2 and v1.get()!=3:
                    ptype='Mobile'
                if v2.get()==4:
                    etype='Office'
                if v2.get()==5:
                    etype='Personal'
                if v2.get()!=4 and v2.get()!=5:
                    etype='Personal'
                z=Button(root4,text='Save',bg='light yellow',command=realupdate)
                z.grid(row=13,column=1)
           
            op.insert(END,'First Name : '+str(a[0][1]))
            op.insert(END,'Last Name : '+str(a[0][2]))
            op.insert(END,'Company : '+str(a[0][3]))
            op.insert(END,'Address : '+str(a[0][4]))
            op.insert(END,'City : '+str(a[0][5]))
            op.insert(END,'Pin Code : '+str(a[0][6]))
            op.insert(END,'Website : '+str(a[0][7]))
            op.insert(END,'Date of Birth : '+str(a[0][8]))
            op.insert(END,'Contact Type :'+str(b[0][0]))
            op.insert(END,'Phone no. :'+str(b[0][1]))
            op.insert(END,'Email Type :'+str(c[0][0]))
            op.insert(END,'Email ID :'+str(c[0][1]))
            Button(root3,text='Update',bg='light yellow',command=update).grid(row=3,column=0)

            
    root3=Tk()
    root3.title("Edit")
    Label(root3,text='Search Bar : ').grid(row=0,column=0)
    s=Entry(root3)
    s.grid(row=1,column=0)
    op=Listbox(root3,height=20,width=60,font='Arial',selectmode=SINGLE)
    op.grid(row=2,column=0)
    cur.execute("select fname,lname from detail")
    f=cur.fetchall()
    for j in range(len(f)):
        k=str(f[j][0])+' '+str(f[j][1])
        op.insert(END,k)
    ptype=''
    etype=''
    root3.bind('<ButtonRelease-1>',printme)
    root3.bind('<KeyPress>',namesearch)
    Button(root3,text='Close',bg='light yellow',command=updateclose).grid(row=4,column=0)
    root3.mainloop()

#close
def Close():
    showinfo('Closing!!','Exiting Phone Book')
    root.destroy()

Label(root,text=' ').grid(row=13,column=0)    
Button(root,text='Save',bg='light yellow',command=Save).grid(row=14,column=0)
Button(root,text='Search',bg='light yellow',command=Search).grid(row=14,column=1)
Button(root,text='Edit',bg='light yellow',command=Edit).grid(row=14,column=2)
Button(root,text='Close',bg='light yellow',command=Close).grid(row=14,column=3)
root.mainloop()
