from tkinter import *
from tkinter import ttk  # themed tkinter, it allows us to create modern-looking, themed widgets
from tkinter import messagebox
from datetime import datetime
import sqlite3
import random
from PIL import Image, ImageTk

conn = sqlite3.connect('medicines_1.db')

# create cursor
cursor=conn.cursor()
cursor1=conn.cursor()

# create table
conn.execute('''CREATE TABLE IF NOT EXISTS test1 (
          Med_id INTEGER PRIMARY KEY AUTOINCREMENT,
          Medicine_name text NOT NULL,
          Date_Of_Purchase text,
          Quantity int,
          Price_per_item decimal(10,2),
          invoice int,
          Manufacture_date text,
          Expiry_date text,
          batch_no text,
          Wholesaler_name text
          );''')

conn.execute('''CREATE TABLE IF NOT EXISTS sale_hist (
          Pat_id INTEGER PRIMARY KEY AUTOINCREMENT ,
          Patient_name text NOT NULL,
          Medicine_name text NOT NULL,
          Date_Of_Purchase text,
          Price_per_item decimal(10,2)
          );''')

# Checking if the column exists
cursor.execute("PRAGMA table_info(sale_hist)")
columns = [info[1] for info in cursor.fetchall()]

# Adding the column if it does not exist
if 'quantity' not in columns:
    cursor.execute('ALTER TABLE sale_hist ADD COLUMN quantity INTEGER DEFAULT 1')

conn.execute('''CREATE TABLE IF NOT EXISTS patient (
          Pat_id INTEGER PRIMARY KEY  ,
          Patient_name text NOT NULL,
          Patient_age INTEGER,
          Medicine_name text NOT NULL,
          Date_Of_Purchase text,
          Price_per_item decimal(10,2)
          );''')


def main():
    app=Tk()
    ob=LoginPage(app)
    app.mainloop()


def insert_data(self):
      Medicine_name=medicine_entry.get()
      date_purchase=dateOfPurchase_entry.get()
      quantity=qntity_entry.get()
      pricePer=price_of_one_entry.get()
      invoice=invoice_entry.get()
      manufacture=manufacture_date_entry.get()
      expiry=expiry_entry.get()
      batch=batchNo_entry.get()
      wholesaler=wholesaler_entry.get()


    
      if Medicine_name and date_purchase and quantity and pricePer and invoice and manufacture and expiry and batch and wholesaler:
          try:
              cursor.execute('INSERT INTO test1 (Medicine_name,Date_Of_Purchase,Quantity,Price_per_item,invoice,Manufacture_date,Expiry_date,batch_no,Wholesaler_name) VALUES (?, ?, ?, ?, ?, ?, ?, ?,?)', (Medicine_name,date_purchase,quantity,pricePer,invoice,manufacture,expiry,batch,wholesaler))
              #conn.commit()
              messagebox.showinfo('Success', 'Data inserted successfully',parent=self.win)
              update_listbox(self)
              new_quantity = cursor.execute('SELECT quantity FROM test1 WHERE Medicine_name = ?', (Medicine_name,)).fetchone()[0]
              if new_quantity < 5:
                messagebox.showwarning("Low Stock Warning", f"The stock of {Medicine_name} is low ({new_quantity} left)",parent=self.win)
            #   conn.commit()

            #   cursor.execute("""
            #     CREATE TRIGGER check_quantity
            #     BEFORE INSERT ON test1
            #     FOR EACH ROW
            #     BEGIN
            #         WHEN qntity_entry.get() < 5 THEN
            #             SIGNAL SQLSTATE '45000'
            #             SET MESSAGE_TEXT = 'Quantity is less than 5';
            #         END IF;
            #     END;
            #     """)
              conn.commit()


              
          except Exception as e:
              messagebox.showerror('Error', str(e))
      else:
          messagebox.showerror('Error', 'All fields are required')

def insert_to_sales(self):
    p_name=patient_entry.get()
    p_age=int(patientAge_entry.get())
    med_name=medicine_entry.get()
    d_o_p=dateOfPurchase_entry.get()
    cost_=price_of_one_entry.get()
    qntity=qntity_entry.get()
    


    if p_name and p_age and med_name and d_o_p and cost_:
              cursor1.execute('INSERT INTO patient (Patient_name,Patient_age,Medicine_name,Date_Of_Purchase,Price_per_item) VALUES (?, ?, ?, ?, ?)', (p_name,p_age,med_name,d_o_p,cost_))
              cursor.execute('UPDATE test1 SET quantity = quantity-? WHERE Medicine_name = ?',(qntity, med_name))
    
              #conn.commit()
              #messagebox.showinfo('Success', 'Data inserted successfully',parent=self.win)
              #update_listbox(self)
              conn.commit()
    else:
        pass
        #messagebox.showerror('Error', 'Error in adding to sales',parent=self.win)

    if p_name and med_name and d_o_p and cost_:
              cursor1.execute('INSERT INTO sale_hist (Patient_name,Medicine_name,Date_Of_Purchase,Price_per_item,quantity) VALUES (?, ?, ?, ?, ?)', (p_name,med_name,d_o_p,cost_,qntity))
              #conn.commit()
              messagebox.showinfo('Success', 'Data inserted successfully',parent=self.win)
              #update_listbox(self)
              conn.commit()
    else:
        messagebox.showerror('Error', 'Error in adding to sales',parent=self.win)

               

def clear_area():
    medicine_entry.delete(0,END)
    dateOfPurchase_entry.delete(0,END)
    qntity_entry.delete(0,END)
    price_of_one_entry.delete(0,END)
    invoice_entry.delete(0,END)
    manufacture_date_entry.delete(0,END)
    expiry_entry.delete(0,END)
    batchNo_entry.delete(0,END)
    wholesaler_entry.delete(0,END)

def reset_data():
    patient_entry.delete(0,END)
    patientcontact_entry.delete(0,END)
    medicine_entry.delete(0,END)
    price_of_one_entry.delete(0,END)
    qntity_entry.delete(0,END)

def total_trans():
    cursor.execute('SELECT SUM(quantity*Price_per_item) FROM sale_hist')
    total = cursor.fetchone()
    return str(total)




def update_listbox(app):
    #app.listbox.delete(0, tk.END)
    cursor.execute('SELECT Med_id, Medicine_name, Date_Of_Purchase, Quantity, Price_per_item FROM test1')
    records = cursor.fetchall()
    if len(records)!=0:
        app.pharmacy_table.delete(*app.pharmacy_table.get_children())
        for i in records:
           app.pharmacy_table.insert("",END, values=i)

def display_all(app):
    #app.pharmacy_table.delete(0, END)
    cursor.execute('SELECT * FROM test1')
    records = cursor.fetchall()
    if len(records)!=0:
        app.pharmacy_table.delete(*app.pharmacy_table.get_children())
    for i in records:
           app.pharmacy_table.insert("",END, values=i)
           #print()

def display_pat_det(app):
    #app.pharmacy_table.delete(0, END)
    cursor.execute('SELECT * FROM patient')
    records = cursor.fetchall()
    if len(records)!=0:
        app.pharmacy_table.delete(*app.pharmacy_table.get_children())
        for i in records:
           app.pharmacy_table.insert("",END, values=i)
    

def update_fun(self):
      Medicine_name=medicine_entry.get()
      quantity=qntity_entry.get()
      cost=price_of_one_entry.get()
      med_id=Med_id_entry.get()

      if Medicine_name or quantity or cost or med_id:
          try:
              update_query = """
              UPDATE test1 
              SET Medicine_name = ?, 
                Quantity = ?, 
                Price_per_item = ? 
              WHERE Med_id = ?;
              """
              cursor.execute(update_query, (Medicine_name, quantity, cost, med_id))
              #conn.commit()
              messagebox.showinfo('Success', 'Data updated successfully',parent=self.win)
              conn.commit()

                # Execute the query with the actual values
               

          except ValueError:
              messagebox.showerror('Error', 'Error in updation',parent=self.win)
      else:
          messagebox.showerror('Error', 'All fields are required',parent=self.win)

def update_stock(self):
      Medicine_name=self.med_name_entry.get()
      quantity=self.qntity_entry.get()
      cost=self.cost_entry.get()

      if Medicine_name and quantity and cost:
        try:
              update_query = """
              UPDATE test1 
              SET  Quantity = ?, 
                Price_per_item = ? 
              WHERE Med_id = ?;
              """
              cursor.execute(update_query, (quantity, cost, Medicine_name))
              #conn.commit()
              messagebox.showinfo('Success', 'Data updated successfully',parent=self.win)
              conn.commit()

                # Execute the query with the actual values
               

        except ValueError:
              messagebox.showerror('Error', 'Error in updation',parent=self.win)
      else:
          messagebox.showerror('Error', 'All fields are required',parent=self.win)



def delete_recent(self):
    try:
        # Select the most recent record
        cursor.execute('SELECT Med_id FROM test1 ORDER BY Med_id DESC LIMIT 1;')
        recent_record = cursor.fetchone()
        
        if recent_record:
            # Extract the Med_id of the most recent record
            recent_med_id = recent_record[0]
            
            # Delete the most recent record
            cursor.execute('DELETE FROM test1 WHERE Med_id = ?;', (recent_med_id,))
            update_listbox(self)
            conn.commit()
            messagebox.showinfo('Success', 'Deleted recent data',parent=self.win)
        else:
            messagebox.showinfo('Info', 'No records to delete',parent=self.win)
    
    except Exception as e:
        conn.rollback()  # Roll back any changes if an error occurs
        messagebox.showerror('Error', f'Cannot delete data: {e}',parent=self.win)

def low_qnt_items(app):
    cursor.execute('SELECT * FROM test1 WHERE Quantity < 10')
    records = cursor.fetchall()
    if len(records)!=0:
        app.pharmacy_table.delete(*app.pharmacy_table.get_children())
    for i in records:
           app.pharmacy_table.insert("",END, values=i)


def clear_list_box(self):
    self.listbox.delete(0,END)

def sale_hist(self):
    cursor.execute('SELECT * FROM sale_hist')
    records = cursor.fetchall()
    for record in records:
        self.pharmacy_table.insert("",END, values=record)
        #self.pharmacy_table.insert(END,"")


def delete_record_fun(self):
    Medicine_name=medicine_entry.get()
    med_id=Med_id_entry.get()

    if Medicine_name and med_id:
        try:
            cursor.execute('DELETE FROM test1 WHERE Med_Id = ? AND Medicine_name = ?',(med_id,Medicine_name))
            conn.commit()
            messagebox.showinfo('Success', 'Deleted data',parent=self.win)
        except:
            conn.rollback()  # Roll back any changes if an error occurs
            messagebox.showerror('Error', f'Cannot delete data: ',parent=self.win)

    elif Medicine_name:
        try:
            cursor.execute('DELETE FROM test1 WHERE Medicine_name = ?',(Medicine_name))
            conn.commit()
            messagebox.showinfo('Success', 'Deleted data',parent=self.win)
        except:
            conn.rollback()  # Roll back any changes if an error occurs
            messagebox.showerror('Error', f'Cannot delete data: ',parent=self.win)

    elif med_id:
        try:
            cursor.execute('DELETE FROM test1 WHERE Med_Id = ?',(med_id))
            conn.commit()
            messagebox.showinfo('Success', 'Deleted data',parent=self.win)
        except:
            conn.rollback()  # Roll back any changes if an error occurs
            messagebox.showerror('Error', f'Cannot delete data: ',parent=self.win)

        


def delete_all_records(self):
    try:
        cursor.execute('DELETE FROM test1')
        conn.commit()
        messagebox.showinfo('Success', 'Deleted all records',parent=self.win)
    except:
        conn.rollback()  # Roll back any changes if an error occurs
        messagebox.showerror('Error', 'Cannot delete records',parent=self.win)

def log_out():
    username_ent.delete(0,END)
    password_ent.delete(0,END)
    messagebox.showinfo('Success','Successfully logged out')

def fetch_medicine_names():
            cursor.execute("SELECT Medicine_name FROM test1")
            medicines = cursor.fetchall()
            #conn.close()
            return [medicine[0] for medicine in medicines]

def update_cost(event):
            selected_medicine = medicine_entry.get()
            cursor.execute("SELECT Price_per_item FROM test1 WHERE Medicine_name = ?", (selected_medicine,))
            cost = cursor.fetchone()
            # new_quantity = cursor.execute('SELECT quantity FROM test1 WHERE Medicine_name = ?', (Medicine_name,)).fetchone()[0]
            # if new_quantity < 5:
            #     messagebox.showwarning("Low Stock Warning", f"The stock of {Medicine_name} is low ({new_quantity} left)",parent=self.win)
            #conn.close()
            # if cost:
            #     price_of_one_entry.set(cost[0])

def checkQuantity(self):
    med_name=medicine_entry.get()
    new_quantity = cursor.execute('SELECT quantity FROM test1 WHERE Medicine_name = ?', (med_name,)).fetchone()[0]
    if int(new_quantity) < 5:
        messagebox.showwarning("Low Stock Warning", f"The stock of {med_name} is low ({new_quantity} left)",parent=self.win)
    else:
        messagebox.showinfo('Quantity','Sufficient Stock',parent=self.win)

def reduce_qntity():
    qnty=qntity_entry.get()
    name=medicine_entry.get()
    cursor.execute('UPDATE test1 SET quantity = quantity-qnty WHERE Medicine_name = name')




class LoginPage:
    def __init__(self,win):
        self.win=win
        self.win.geometry("1530x850")
        self.win.title("Pharmacy Management System  |  Login")

        # Load the image file
        self.img_path_1 = 'C:/Users/incha/OneDrive/Documents/projects/DBMS Project/pharmacyManagementSystem/pharma_logo.jpg'  # Update this path to your image file
        self.img_path_2 = 'C:/Users/incha/OneDrive/Documents/projects/DBMS Project/pharmacyManagementSystem/tablet_image.jpg'
        self.img_path_3 = 'C:/Users/incha/OneDrive/Documents/projects/DBMS Project/pharmacyManagementSystem/store_image.jpg'
        self.img_path_4 = 'C:/Users/incha/OneDrive/Documents/projects/DBMS Project/pharmacyManagementSystem/tablet_image.jpg'
        self.img_path_5 = 'C:/Users/incha/OneDrive/Documents/projects/DBMS Project/pharmacyManagementSystem/medical_image.jpg'
        try:
            self.bg_image_1 = Image.open(self.img_path_1)
            self.bg_image_1 = self.bg_image_1.resize((200,200), Image.Resampling.LANCZOS)
            self.bg_logo = ImageTk.PhotoImage(self.bg_image_1)

            self.bg_image_2 = Image.open(self.img_path_2)
            self.bg_image_2 = self.bg_image_2.resize((430,290), Image.Resampling.LANCZOS)
            self.bg_img_1 = ImageTk.PhotoImage(self.bg_image_2)

            self.bg_image_3 = Image.open(self.img_path_3)
            self.bg_image_3 = self.bg_image_3.resize((430,290), Image.Resampling.LANCZOS)
            self.bg_img_2 = ImageTk.PhotoImage(self.bg_image_3)

            self.bg_image_4 = Image.open(self.img_path_5)
            self.bg_image_4 = self.bg_image_4.resize((430,290), Image.Resampling.LANCZOS)
            self.bg_img_3 = ImageTk.PhotoImage(self.bg_image_4)

            self.bg_image_5 = Image.open(self.img_path_4)
            self.bg_image_5 = self.bg_image_5.resize((430,290), Image.Resampling.LANCZOS)
            self.bg_img_4 = ImageTk.PhotoImage(self.bg_image_5)
            
        except Exception as e:
            print(f"Error loading image: {e}")
            self.bg_photo = None


        self.title_lbl=Label(self.win,text="+  MediCare Pharmacy  +",bg="green",fg="yellow",bd=5,relief=GROOVE,font=("Times New Roman",60,"bold"))
        self.title_lbl.pack(side="top",fill='x')
        self.b1=Button(self.win,image=self.bg_logo,borderwidth=0)
        self.b1.place(x=5,y=5)

        # self.time_lbl = Label(self.win, font=("Arial", 12))
        # self.time_lbl.pack(side="top", pady=10)
        #self.time_lbl.update_time()

        #*******************************************************************************

        self.time_lbl=Label(self.win,font=('Helvetica',20),bg='white',fg='darkgreen')
        self.time_lbl.pack(pady=20)

        self.update_clock()

        #***************************************************************************************

        self.login_lbl=Label(self.win,text="-----------Login----------",bg="white",fg="darkgreen",bd=5,relief=GROOVE,font=("Times New Roman",30,"bold"))
        self.login_lbl.pack(side='top',fill='x',pady=5)

        self.main_frame=Frame(self.win,bg='green',bd=5,relief=RIDGE)
        #self.main_frame.pack_propagate(False)  # Prevent frame from resizing to fit contents
        self.main_frame.place(x=440,y=250,width=650,height=520)

        self.photo_frame_1=Frame(self.win,bg='lightgrey',bd=0,relief=FLAT)
        self.photo_frame_1.place(x=2,y=250,width=430,height=580)

        self.photo_frame_2=Frame(self.win,bg='lightgrey',bd=0,relief=FLAT)
        self.photo_frame_2.place(x=1100,y=250,width=430,height=580)

        # Button Frame

        self.but_frame_1=Button(self.photo_frame_1,image=self.bg_img_1,bg='lightpink',font=('Arial',13),relief=FLAT)
        self.but_frame_1.place(x=2,y=2,height=290,width=430)

        self.but_frame_2=Button(self.photo_frame_1,image=self.bg_img_3,bg='lightblue',font=('Arial',13),relief=FLAT)
        self.but_frame_2.place(x=2,y=290,height=290,width=430)

        self.but_frame_3=Button(self.photo_frame_2,image=self.bg_img_1,bg='lightblue',font=('Arial',13),relief=FLAT)
        self.but_frame_3.place(x=2,y=2,height=290,width=430)

        self.but_frame_4=Button(self.photo_frame_2,image=self.bg_img_3,bg='lightpink',font=('Arial',13),relief=FLAT)
        self.but_frame_4.place(x=2,y=290,height=290,width=430)
        

        self.entryFrame=LabelFrame(self.main_frame,text='Enter Credentials',bg='lightgrey',fg='darkgreen',bd=5,relief=RIDGE,font=("Arial",16,'bold'))
        self.entryFrame.pack(side='top',fill=BOTH,pady=10)

        self.login_as_frame=LabelFrame(self.main_frame,text='Login as',bg='lightgrey',fg='darkgreen',bd=5,font=('Arial',16,'bold'),relief=RIDGE)
        self.login_as_frame.pack(side='top',fill=BOTH,pady=10)



        #******** text variables ***************
        username=StringVar()
        Password=StringVar()    
        #***************************************

        def update_time(self):
           now = datetime.now()
           current_time = now.strftime("%Y-%m-%d %H:%M:%S")
           self.time_lbl.config(text=current_time)
           self.win.after(1000, self.update_time)  # update every second

        def employee_login():
            if username.get()=='emp' or username.get()=='emp1' and Password.get()=='123' or Password.get()=='999':
                self.submit_but.config(state=NORMAL)
            else:
                messagebox.showerror('Error','Invalid Employee Credentials')
            

        def admin_login():
            if username.get()=='admin' or username.get()=='admin1' and Password.get()=='123' or Password.get()=='999':
                self.submit_but.config(state=NORMAL)
            else:
                messagebox.showerror('Error','Invalid admin credentials')


        #=============================================================

        self.login_as_emp=Button(self.login_as_frame,text='Employee',bd=4,width=15,font=('Arial',15),bg='lightblue',command=employee_login)
        self.login_as_emp.grid(row=0,column=0,padx=6,pady=6)

        self.login_as_admin=Button(self.login_as_frame,text='Admin',bd=4,width=15,font=('Arial',15),bg='lightblue',command=admin_login)
        self.login_as_admin.grid(row=0,column=1,padx=6,pady=6)

        self.username_lbl=Label(self.entryFrame,text="Username: ",font=('Calibri',15),bg='lightgrey')
        self.username_lbl.grid(row=0,column=0,padx=2,pady=2)
        global username_ent
        username_ent=Entry(self.entryFrame,border=3,textvariable=username,font=("Arial",15))
        username_ent.grid(row=0,column=1,padx=2,pady=2)

        self.password_lbl=Label(self.entryFrame,text="Password: ",bg="lightgrey",font=("Calibri",15))
        self.password_lbl.grid(row=1,column=0,padx=2,pady=2)
        global password_ent
        password_ent=Entry(self.entryFrame,textvariable=Password,show='*',border=3,font=("Arial",15))
        password_ent.grid(row=1,column=1,padx=2,pady=2)

        self.false_frame1=Frame(self.entryFrame,bd=5,bg='lightgrey')
        
        # Reset function

        def reset_fun():
            username.set("")
            Password.set("")
            self.submit_but.config(state=DISABLED)
        
        def exit_fun():
            # Add a message box here
            self.win.destroy()

        def next_sec():
            if username.get()=='emp' or username.get()=='emp1':
                self.newWindow=Toplevel(self.win)
                self.app=window2(self.newWindow)
            elif username.get()=='admin' or username.get()=='admin1':
                self.newWindow2=Toplevel(self.win)
                self.app=admin_window(self.newWindow2)



        # Button Frame

        self.button_frame=LabelFrame(self.main_frame,text="Options",bg='lightgrey',fg='darkgreen',relief=RIDGE,bd=5,font=("Arial",16,'bold'))
        self.button_frame.pack(side='top',fill=BOTH,pady=10)

        # Submit Button

        self.submit_but=Button(self.button_frame,bd=2,bg='lightblue',state=DISABLED,width=15,text='Submit',font=("Arial",15),command=next_sec)
        self.submit_but.grid(row=0,column=1,padx=6,pady=6)

        # Label to show status
        status_label =Label(self.button_frame, text="")
        status_label.grid(pady=10)

        self.reset_but=Button(self.button_frame,bg='lightblue',bd=2,width=15,text='Reset',font=("Arial",15),command=reset_fun)
        self.reset_but.grid(row=0,column=2,padx=6,pady=6)

        self.exit_but=Button(self.button_frame,bd=2,bg='lightblue',width=15,text='Exit',font=("Arial",15),command=exit_fun)
        self.exit_but.grid(row=0,column=3,padx=6,pady=6)

        self.txt='''
    The Best and Most Efficient Pharmacy
    is Within Your Own System
                 '''

        self.bill_txt_1=Label(self.main_frame,bg='white',font=('Brush Script MT',35,'bold'),text=self.txt,fg='green')  #Comic Sans MS  Brush Script MT  Segoe Script
        self.bill_txt_1.pack(fill=BOTH,expand=True)

    def update_clock(self):
        current_time=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.time_lbl.config(text=current_time)
        self.win.after(1000,self.update_clock)

class window2:
    def __init__(self,win):
        self.win=win
        self.win.geometry("1300x900")
        self.win.title("Billing Section")

        self.title_lbl=Label(self.win,text="+  MediCare Pharmacy  +",bg="green",fg="yellow",bd=5,relief=GROOVE,font=("Times",35,"bold"))
        self.title_lbl.pack(side="top",fill='x')

        self.login_lbl=Label(self.win,text="---------Billing----------",bg="white",fg="darkgreen",bd=5,relief=GROOVE,font=("Times",30,"bold"))
        self.login_lbl.pack(side='top',fill='x',pady=5)

        self.entry_frame=LabelFrame(self.win,text='Enter Details',bg='lightgrey',fg='darkgreen',bd=5,font=('Arial',15,'bold'))
        self.entry_frame.place(x=20,y=150,width=500,height=600)

        # Text variables ===========================================
        bill_no = IntVar()
        bill_no = random.randint(100,999)

        # ****************Functions********************
        def default_bill():
            self.bill_txt.insert(END,'\t\t\t\t Pharmaceticals Limited')
            self.bill_txt.insert(END,'\n\t\t\t Near BEML, Koorgalli Industrial area, Mysuru')
            self.bill_txt.insert(END,'\n\t\t\t\t contact - +9345892130')
            self.bill_txt.insert(END,'\n*********************************************************************************\n\n')
            self.bill_txt.insert(END,f"Bill Number : {bill_no}")

        #********************************************************************************************

        def generate_bill():
            self.bill_txt_1.insert(END,f'\nPatient Name : {pat_name.get()}')
            self.bill_txt_1.insert(END,f'\nPatient Contact no : {pat_cont.get()}')
            self.bill_txt_1.insert(END,f'\nMedicine Name : {med_name.get()}')
            self.bill_txt_1.insert(END,f'\nDate of Purchase : {date_pr.get()}')
            self.bill_txt_1.insert(END,f'\nQuantity : {item_qntity.get()}')
            self.bill_txt_1.insert(END,f'\nCost per item : {cost_of_one.get()}')

        #****************************************************************************
        
        def total_bill():
            cost=float(cost_of_one.get())
            quantity=float(item_qntity.get())
            self.bill_txt_1.insert(END,f'\n\nTotal Amount : {cost*quantity}\n\n')

        #*******************************************************************************

        def clear_bill():
            self.bill_txt_1.delete('1.0', END)
        #The line self.bill_txt_1.delete('1.0', tk.END) is used to clear all the text in a Text widget in tkinter


        #********************************************************************************


        pat_name=StringVar()
        pat_age=StringVar()
        pat_cont=StringVar()
        date_pr=StringVar()
        med_name=StringVar()
        item_qntity=StringVar()
        cost_of_one=StringVar()

        date_pr.set(datetime.now().strftime('%Y-%m-%d'))



        #==================================================================

        self.patientname_lbl=Label(self.entry_frame,text='Patient Name',bd=5,font=('Calibri',15),bg='lightgrey')
        self.patientname_lbl.grid(row=0,column=0,padx=5,pady=5)
        global patient_entry
        patient_entry=Entry(self.entry_frame,textvariable=pat_name,bd=2,width=25,font=('Calibri',15))
        patient_entry.grid(row=0,column=1,padx=5,pady=5)

        self.patientAge_lbl=Label(self.entry_frame,text='Patient Age',bd=5,font=('Calibri',15),bg='lightgrey')
        self.patientAge_lbl.grid(row=1,column=0,padx=5,pady=5)
        global patientAge_entry
        patientAge_entry=Entry(self.entry_frame,textvariable=pat_age,bd=2,width=25,font=('Calibri',15))
        patientAge_entry.grid(row=1,column=1,padx=5,pady=5)

        self.patientcontact_lbl=Label(self.entry_frame,text='Patient Contact',bd=5,font=('Calibri',15),bg='lightgrey')
        self.patientcontact_lbl.grid(row=2,column=0,padx=5,pady=5)
        global patientcontact_entry
        patientcontact_entry=Entry(self.entry_frame,textvariable=pat_cont,bd=2,width=25,font=('Calibri',15))
        patientcontact_entry.grid(row=2,column=1,padx=5,pady=5)
        
        self.medicine_name=Label(self.entry_frame,text='Medicine Name',bd=5,font=('Calibri',15),bg='lightgrey')
        self.medicine_name.grid(row=3,column=0,padx=5,pady=5)
        global medicine_entry
        #medicine_entry=Entry(self.entry_frame,bd=2,textvariable=med_name,width=25,font=('Calibri',15))
        medicine_entry = ttk.Combobox(self.entry_frame, textvariable=med_name, values=fetch_medicine_names(), font=('Calibri', 17))
        medicine_entry.grid(row=3,column=1,padx=5,pady=5)
        medicine_entry.bind("<<ComboboxSelected>>", update_cost)

        self.date=Label(self.entry_frame,text='Date',bd=5,font=('Calibri',15),bg='lightgrey')
        self.date.grid(row=4,column=0,padx=5,pady=5)
        global dateOfPurchase_entry
        dateOfPurchase_entry=Entry(self.entry_frame,textvariable=date_pr,bd=2,width=25,font=('Calibri',15))
        dateOfPurchase_entry.grid(row=4,column=1,padx=5,pady=5)

        self.qntity_lbl=Label(self.entry_frame,text='Quantity',bd=5,font=('Calibri',15),bg='lightgrey')
        self.qntity_lbl.grid(row=5,column=0,padx=5,pady=5)
        global qntity_entry
        qntity_entry=Entry(self.entry_frame,textvariable=item_qntity,bd=2,width=25,font=('Calibri',15))
        qntity_entry.grid(row=5,column=1,padx=5,pady=5)


        self.cost_lbl=Label(self.entry_frame,text='Cost of one',bd=5,font=('Calibri',15),bg='lightgrey')
        self.cost_lbl.grid(row=6,column=0,padx=5,pady=5)
        global price_of_one_entry
        price_of_one_entry=Entry(self.entry_frame,textvariable=cost_of_one,bd=2,width=25,font=('Calibri',15))
        price_of_one_entry.grid(row=6,column=1,padx=5,pady=5)


        # Bill frame

        self.bill_frame=LabelFrame(self.win,text='Bill Area',bg='lightgrey',bd=4,relief=RIDGE,font=('Arial',14))
        self.bill_frame.place(x=585,y=220,width=680,height=350)
        self.y_scroll=Scrollbar(self.bill_frame,orient='vertical')
        self.bill_txt=Text(self.bill_frame,bg='white',yscrollcommand=self.y_scroll.set)

        self.bill_frame_1=Frame(self.bill_frame)
        self.bill_frame_1.place(x=2,y=100,width=640,height=220)
        self.bill_txt_1=Text(self.bill_frame_1,bg='white')

        self.y_scroll.config(command=self.bill_txt.yview)
        self.y_scroll.pack(side=RIGHT,fill=Y)
        self.bill_txt.pack(fill=BOTH,expand=True)
        self.bill_txt_1.pack(fill=BOTH,expand=True)

        default_bill()
            

        # Button Frame

        self.false_frame2=Frame(self.entry_frame,bd=5,bg='lightgrey')

        self.but_frame=LabelFrame(self.entry_frame,bg='lightgrey',relief=FLAT)
        self.but_frame.place(x=20,y=350,height=270,width=300)

        self.total_but=Button(self.but_frame,text='Total',font=('Ariel',13,'bold'),bd=2,width=10,command=total_bill)
        self.total_but.grid(row=0,column=0,padx=7,pady=7)

        self.generateBill_but=Button(self.but_frame,text='Generate Bill',font=('Arial',13,'bold'),bd=2,width=15,command=generate_bill)
        self.generateBill_but.grid(row=0,column=1,padx=7,pady=7)

        self.add_but=Button(self.but_frame,text='Add',font=('Ariel',13,'bold'),bd=2,width=10,command=self.insert_to_sales_1)
        self.add_but.grid(row=1,column=0,padx=7,pady=7)

        self.Clear_but=Button(self.but_frame,text='Clear',font=('Ariel',13,'bold'),bd=2,width=15,command=clear_bill)
        self.Clear_but.grid(row=1,column=1,padx=7,pady=7)

        self.reset_but=Button(self.but_frame,text='Reset',font=('Ariel',13,'bold'),bd=2,width=10,command=reset_data)
        self.reset_but.grid(row=2,column=0,padx=7,pady=7)

        self.checkQ_but=Button(self.but_frame,text='Check Quantity',font=('Ariel',13,'bold'),bd=2,width=15,command=self.check_Quant)
        self.checkQ_but.grid(row=2,column=1,padx=7,pady=7)

    def insert_to_sales_1(self):
        insert_to_sales(self)

    def check_Quant(self):
        checkQuantity(self)


class admin_window:
    def __init__(self,win):
        self.win=win
        self.win.geometry("900x650")
        self.win.title("Admin Options")

        self.title_lbl=Label(self.win,text="+  MediCare Pharmacy  +",bg="green",fg="yellow",bd=5,relief=GROOVE,font=("Times",40,"bold"))
        self.title_lbl.pack(side="top",fill='x')

        self.login_lbl=Label(self.win,text="----------Admin Panel---------",bg="white",fg="darkgreen",bd=5,relief=GROOVE,font=("Times",35,"bold"))
        self.login_lbl.pack(side='top',fill='x',pady=5)

        self.bg_frame=Frame(self.win,bg='white')
        self.bg_frame.place(x=2,y=150,width=1500,height=900)

        # Load the image file
        self.img_path = 'C:/Users/incha/OneDrive/Documents/projects/DBMS Project/pharmacyManagementSystem/pharmacy.jpeg'  # Update this path to your image file
        try:
            self.bg_image = Image.open(self.img_path)
            self.bg_image = self.bg_image.resize((900,900), Image.Resampling.LANCZOS)
            self.bg_img = ImageTk.PhotoImage(self.bg_image)
            
        except Exception as e:
            print(f"Error loading image: {e}")
            self.bg_photo = None

        self.b1=Button(self.bg_frame,borderwidth=0)
        self.b1.place(x=5,y=5)

        self.entry_frame=LabelFrame(self.win,text='Options',bg='lightgrey',fg='darkgreen',bd=5,font=('Arial',15,'bold'))
        self.entry_frame.place(x=120,y=200,width=700,height=300)

        #==========================================================
        def go_to_purchase():
            self.newWindow3=Toplevel(self.win)
            self.app=purchase(self.newWindow3)

        def go_to_stock():
            self.newWindow4=Toplevel(self.win)
            self.app=stock_manage(self.newWindow4)

        def go_to_sales():
            self.newWindow5=Toplevel(self.win)
            self.app=sales_window(self.newWindow5)

        def go_to_pat_details():
            self.newWindow6=Toplevel(self.win)
            self.app=patient_details(self.newWindow6)



        # Button Frame

        self.but_frame=LabelFrame(self.entry_frame,bg='lightgrey',font=('Arial',13),relief=FLAT)
        self.but_frame.place(x=50,y=10,height=300,width=600)

        self.purchase_but=Button(self.but_frame,text='Purchase',font=('Arial',14),bd=4,relief=RIDGE,width=20,command=go_to_purchase)
        self.purchase_but.grid(row=0,column=0,padx=15,pady=8)

        self.stock_but=Button(self.but_frame,text='Stock',font=('Arial',14),bd=4,relief=RIDGE,width=20,command=go_to_stock)
        self.stock_but.grid(row=0,column=1,padx=15,pady=8)

        self.Sale_history=Button(self.but_frame,text='Sale History',font=('Arial',14),bd=4,relief=RIDGE,width=20,command=go_to_sales)
        self.Sale_history.grid(row=1,column=0,padx=15,pady=8)

        self.wholesalers=Button(self.but_frame,text='Patient Details',font=('Arial',14),bd=4,relief=RIDGE,width=20,command=go_to_pat_details)
        self.wholesalers.grid(row=1,column=1,padx=15,pady=8)

        # self.register=Button(self.but_frame,text='Register',font=('Arial',14),bd=4,relief=RIDGE,width=20)
        # self.register.grid(row=2,column=0,padx=15,pady=8)

        # self.change_password=Button(self.but_frame,text='Change Password',font=('Arial',14),bd=4,relief=RIDGE,width=20)
        # self.change_password.grid(row=2,column=1,padx=15,pady=8)

        # self.manage_emp=Button(self.but_frame,text='Manage Emp',font=('Arial',14),bd=4,relief=RIDGE,width=20)
        # self.manage_emp.grid(row=3,column=0,padx=15,pady=8)

        self.logout=Button(self.but_frame,text='Logout',font=('Arial',14),bd=4,relief=RIDGE,width=20,command=log_out)
        self.logout.grid(row=2,columnspan=2,padx=15,pady=8)



class purchase:
    def show_recents(): 
        cursor.execute('SELECT Med_id, Medicine_name, Date_Of_Purchase, Quantity, Price_per_item from test1')

    def __init__(self,win):
        self.win=win
        self.win.geometry("1530x850")
        self.win.title("Purchase")

        self.title_lbl=Label(self.win,text="+  MediCare Pharmacy  +",bg="white",fg="darkgreen",bd=5,relief=GROOVE,font=("Times New Roman",34,"bold"))
        self.title_lbl.pack(side="top",fill='x')

        self.purchase_lbl=Label(self.win,text="------------Purchase Section------------",bg="white",fg="darkgreen",bd=5,relief=GROOVE,font=("Times New Roman",30,"bold"))
        self.purchase_lbl.pack(side='top',fill='x',pady=5)

        self.entry_frame=LabelFrame(self.win,text='Manage Purchases',bg='lightgrey',fg='darkgreen',bd=5,font=('Arial',15,'bold'))
        self.entry_frame.place(x=20,y=160,width=600,height=600)

        #**********function*******************************
        def go_to_update():
            self.top=Toplevel(win)
            self.app=update_details(self.top)

        self.medicine_name=Label(self.entry_frame,text='Medicine Name',bg='lightgrey',font=('Calibri',16))
        self.medicine_name.grid(row=0,column=0,padx=4,pady=4)
        global medicine_entry
        medicine_entry=Entry(self.entry_frame,bd=4,relief=GROOVE,width=20,font=('Calibri',15))
        medicine_entry.grid(row=0,column=1,padx=4,pady=4)

        self.dateOfPurchase=Label(self.entry_frame,text='Date of Purchase',bg='lightgrey',font=('Claibri',16))
        self.dateOfPurchase.grid(row=1,column=0,padx=4,pady=4)
        global dateOfPurchase_entry
        dateOfPurchase_entry=Entry(self.entry_frame,bd=4,relief=GROOVE,width=20,font=('Calibri',15))
        dateOfPurchase_entry.grid(row=1,column=1,padx=4,pady=4)

        self.quantity=Label(self.entry_frame,text='Enter Quantity',bg='lightgrey',font=('Claibri',16))
        self.quantity.grid(row=2,column=0,padx=4,pady=4)
        global qntity_entry
        qntity_entry=Entry(self.entry_frame,bd=4,relief=GROOVE,width=20,font=('Calibri',15))
        qntity_entry.grid(row=2,column=1,padx=4,pady=4)

        self.price_of_one=Label(self.entry_frame,text='Enter Price of one',bg='lightgrey',font=('Claibri',16))
        self.price_of_one.grid(row=3,column=0,padx=4,pady=4)
        global price_of_one_entry
        price_of_one_entry=Entry(self.entry_frame,bd=4,relief=GROOVE,width=20,font=('Calibri',15))
        price_of_one_entry.grid(row=3,column=1,padx=4,pady=4)

        self.invoice_lbl=Label(self.entry_frame,text='Enter Invoice',bg='lightgrey',font=('Claibri',16))
        self.invoice_lbl.grid(row=4,column=0,padx=4,pady=4)
        global invoice_entry
        invoice_entry=Entry(self.entry_frame,bd=4,relief=GROOVE,width=20,font=('Calibri',15))
        invoice_entry.grid(row=4,column=1,padx=4,pady=4)

        self.manufacture_lbl=Label(self.entry_frame,text='Enter Manufacture Date',bg='lightgrey',font=('Claibri',16))
        self.manufacture_lbl.grid(row=5,column=0,padx=4,pady=4)
        global manufacture_date_entry
        manufacture_date_entry=Entry(self.entry_frame,bd=4,relief=GROOVE,width=20,font=('Calibri',15))
        manufacture_date_entry.grid(row=5,column=1,padx=4,pady=4)

        self.expiry_lbl=Label(self.entry_frame,text='Enter Expiry Date',bg='lightgrey',font=('Claibri',16))
        self.expiry_lbl.grid(row=6,column=0,padx=4,pady=4)
        global expiry_entry
        expiry_entry=Entry(self.entry_frame,bd=4,relief=GROOVE,width=20,font=('Calibri',15))
        expiry_entry.grid(row=6,column=1,padx=4,pady=4)

        self.batchNo_lbl=Label(self.entry_frame,text='Batch No',bg='lightgrey',font=('Claibri',16))
        self.batchNo_lbl.grid(row=7,column=0,padx=4,pady=4)
        global batchNo_entry
        batchNo_entry=Entry(self.entry_frame,bd=4,relief=GROOVE,width=20,font=('Calibri',15))
        batchNo_entry.grid(row=7,column=1,padx=4,pady=4)

        self.wholesaler_lbl=Label(self.entry_frame,text='Wholesaler Name',bg='lightgrey',font=('Claibri',16))
        self.wholesaler_lbl.grid(row=8,column=0,padx=4,pady=4)
        global wholesaler_entry
        wholesaler_entry=Entry(self.entry_frame,bd=4,relief=GROOVE,width=20,font=('Calibri',15))
        wholesaler_entry.grid(row=8,column=1,padx=4,pady=4)

        # Button Frame

        self.but_frame=LabelFrame(self.entry_frame,bg='lightgrey',relief=FLAT)
        self.but_frame.place(x=20,y=390,width=500,height=130)

        self.add_but=Button(self.but_frame,text='Add',font=('Arial',14,'bold'),bd=4,relief=RIDGE,width=10,command=self.insert_fun)
        self.add_but.grid(row=0,column=0,padx=10,pady=5)

        self.update_but=Button(self.but_frame,text='Update',font=('Arial',14,'bold'),bd=4,relief=RIDGE,width=10,command=go_to_update)
        self.update_but.grid(row=0,column=1,padx=10,pady=5)

        self.Delete_but=Button(self.but_frame,text='Delete',font=('Arial',14,'bold'),bd=4,relief=RIDGE,width=10,command=self.delete_rec)
        self.Delete_but.grid(row=0,column=2,padx=10,pady=5)

        self.clear_but=Button(self.but_frame,text='Clear',font=('Arial',14,'bold'),bd=4,relief=RIDGE,width=10,command=clear_area)
        self.clear_but.grid(row=1,column=0,padx=10,pady=5)

        # create listbox
        
        # self.listbox=Listbox(self.win,bg='lightgrey',bd=3)
        # self.listbox.place(x=680,y=120,width=700,height=500)
        #self.listbox.insert(END,'Med_id           Medicine_name           Date_Of_Purchase           Quantity           Price_per_item')
        #update_listbox(self)

        self.framedet=Frame(self.win,bd=5,relief=RIDGE)
        self.framedet.place(x=680,y=160,width=700,height=500)

        self.sc_x=ttk.Scrollbar(self.framedet,orient=HORIZONTAL)
        self.sc_x.pack(side=BOTTOM,fill=X)
        self.sc_y=ttk.Scrollbar(self.framedet,orient=VERTICAL)
        self.sc_y.pack(side=RIGHT,fill=Y)

        self.pharmacy_table=ttk.Treeview(self.framedet,columns=('Med_Id','Medicine_name','Date_Of_Purchase','Quantity','Price_per_item'),xscrollcommand=self.sc_x.set,yscrollcommand=self.sc_y.set)
        self.sc_x.config(command=self.pharmacy_table.xview)
        self.sc_y.config(command=self.pharmacy_table.yview)

        self.pharmacy_table['show']='headings'

        self.pharmacy_table.heading('Med_Id',text='Medicine Id')
        self.pharmacy_table.heading('Medicine_name',text='Medicine_name')
        self.pharmacy_table.heading('Date_Of_Purchase',text='Date_Of_Purchase')
        self.pharmacy_table.heading('Quantity',text='Quantity')
        self.pharmacy_table.heading('Price_per_item',text='Price_per_item')

        self.pharmacy_table.pack(fill=BOTH,expand=1)

        self.pharmacy_table.column('Medicine Id',width=100)
        self.pharmacy_table.column('Medicine_name',width=100)
        self.pharmacy_table.column('Date_Of_Purchase',width=100)
        self.pharmacy_table.column('Quantity',width=100)
        self.pharmacy_table.column('Price_per_item',width=100)

    def insert_fun(self):
        insert_data(self)

    def delete_rec(self):
        delete_recent(self)

    

class update_details:
    def __init__(self,win):
        self.win=win
        self.win.geometry("900x500")
        self.win.title("Update")

        self.title_lbl=Label(self.win,text="+  MediCare Pharmacy  +",bg="green",fg="yellow",bd=5,relief=GROOVE,font=("Times",40,"bold"))
        self.title_lbl.pack(side="top",fill='x')

        self.entry_frame=LabelFrame(self.win,text='-----------Manage Purchases----------',bg='white',fg='darkgreen',bd=5,font=('Times',25,'bold'))
        self.entry_frame.place(x=20,y=120,width=600,height=470)

        self.purchase_lbl=Label(self.win,text="Update Details",bg="blue",fg="yellow",bd=5,relief=GROOVE,font=("Arial",25,"bold"))
        self.purchase_lbl.pack(side='top',fill='x',pady=5)


        self.Med_id=Label(self.entry_frame,text='Enter id',bg='lightgrey',font=('Claibri',16))
        self.Med_id.grid(row=0,column=0,padx=4,pady=4)
        global Med_id_entry
        Med_id_entry=Entry(self.entry_frame,bd=4,relief=GROOVE,width=20,font=('Calibri',15))
        Med_id_entry.grid(row=0,column=1,padx=4,pady=4)

        self.medicine_name=Label(self.entry_frame,text='Medicine Name',bg='lightgrey',font=('Claibri',16))
        self.medicine_name.grid(row=1,column=0,padx=4,pady=4)
        global medicine_entry
        medicine_entry=Entry(self.entry_frame,bd=4,relief=GROOVE,width=20,font=('Calibri',15))
        medicine_entry.grid(row=1,column=1,padx=4,pady=4)

        self.quantity=Label(self.entry_frame,text='Enter Quantity',bg='lightgrey',font=('Claibri',16))
        self.quantity.grid(row=2,column=0,padx=4,pady=4)
        global qntity_entry
        qntity_entry=Entry(self.entry_frame,bd=4,relief=GROOVE,width=20,font=('Calibri',15))
        qntity_entry.grid(row=2,column=1,padx=4,pady=4)

        self.price_of_one=Label(self.entry_frame,text='Enter Price of one',bg='lightgrey',font=('Claibri',16))
        self.price_of_one.grid(row=3,column=0,padx=4,pady=4)
        global price_of_one_entry
        price_of_one_entry=Entry(self.entry_frame,bd=4,relief=GROOVE,width=20,font=('Calibri',15))
        price_of_one_entry.grid(row=3,column=1,padx=4,pady=4)

        # Button Frame

        self.but_frame=LabelFrame(self.entry_frame,bg='lightgrey',relief=FLAT)
        self.but_frame.place(x=20,y=180,width=300,height=130)

        self.update_but=Button(self.but_frame,text='Update',font=('Arial',14,'bold'),bd=4,relief=RIDGE,width=10,command=self.go_to_update_1)
        self.update_but.grid(row=0,column=1,padx=10,pady=5)

    def go_to_update_1(self):
        update_fun(self)



class stock_manage:
    def __init__(self,win):
        self.win=win
        self.win.geometry("1530x850")
        self.win.title("Stock")

        self.title_lbl=Label(self.win,text="+  MediCare Pharmacy  +",bg="green",fg="yellow",bd=5,relief=GROOVE,font=("Times",25,"bold"))
        self.title_lbl.pack(side="top",fill='x')

        self.purchase_lbl=Label(self.win,text="----------Stock Management----------",bg="white",fg="darkgreen",bd=5,relief=GROOVE,font=("Times",25,"bold"))
        self.purchase_lbl.pack(side='top',fill='x',pady=5)

        self.entry_frame=LabelFrame(self.win,text='Options',bg='lightgrey',fg='darkgreen',bd=5,font=('Arial',15,'bold'))
        self.entry_frame.place(x=20,y=120,width=550,height=570)

        self.low_qntity_lbl=Label(self.entry_frame,text='See Low Quantity Items',bg='lightgrey',font=('Claibri',16))
        self.low_qntity_lbl.grid(row=0,column=0,padx=4,pady=4)

        self.low_qnt_but=Button(self.entry_frame,text='Low Quantity',font=('Arial',14),bd=4,width=15,height=2,command=self.low_quantity)
        self.low_qnt_but.grid(row=0,column=1,padx=5,pady=5)

        self.update_item_lbl=Label(self.entry_frame,text='Update Item Data',bg='lightgrey',font=('Claibri',16))
        self.update_item_lbl.grid(row=1,column=0,padx=4,pady=4)

        # ******************function***********************************

        def activate_sub():
          self.sub_but.config(state=NORMAL)

        def clear_entry():
            self.med_name_entry.delete(0,END)
            self.qntity_entry.delete(0,END)
            self.cost_entry.delete(0,END)

            

        def go_to_delete_section():
            self.newWindow5=Toplevel(self.win)
            self.app=delete_record(self.newWindow5)

        self.update_item_but=Button(self.entry_frame,text='Update',font=('Arial',14),bd=4,width=15,height=2,command=activate_sub)
        self.update_item_but.grid(row=1,column=1,padx=5,pady=5)

        self.delete_data_lbl=Label(self.entry_frame,text='Delete Data',bg='lightgrey',font=('Calibri',16))
        self.delete_data_lbl.grid(row=2,column=0,padx=4,pady=4)

        self.delete_data_lbl_but=Button(self.entry_frame,text='Delete',font=('Arial',14),bd=4,width=15,height=2,command=go_to_delete_section)
        self.delete_data_lbl_but.grid(row=2,column=1,padx=5,pady=5)

        self.see_all_lbl=Label(self.entry_frame,text='See All',bg='lightgrey',font=('Claibri',16))
        self.see_all_lbl.grid(row=3,column=0,padx=4,pady=4)

        # create listbox
        
        # self.listbox1=Listbox(self.win,bg='lightgrey',bd=3)
        # self.listbox1.place(x=600,y=120,width=680,height=450)
        #self.listbox1.insert(END,'Med_id           Medicine_name           Date_Of_Purchase           Quantity           Price_per_item')

        self.framedet=Frame(self.win,bd=5,relief=RIDGE)
        self.framedet.place(x=580,y=120,width=890,height=600)

        self.sc_x=ttk.Scrollbar(self.framedet,orient=HORIZONTAL)
        self.sc_x.pack(side=BOTTOM,fill=X)
        self.sc_y=ttk.Scrollbar(self.framedet,orient=VERTICAL)
        self.sc_y.pack(side=RIGHT,fill=Y)

        self.pharmacy_table=ttk.Treeview(self.framedet,columns=('Med Id','Medicine Name','Date Of Purchase','Quantity','Price Per Item','invoice','ManufactureDate','Expiry Date','batchNo','WholesalerName'),xscrollcommand=self.sc_x.set,yscrollcommand=self.sc_y.set)
        self.sc_x.config(command=self.pharmacy_table.xview)
        self.sc_y.config(command=self.pharmacy_table.yview)

        self.pharmacy_table['show']='headings'

        self.pharmacy_table.heading('Med Id',text='Medicine Id')
        self.pharmacy_table.heading('Medicine Name',text='Medicine Name')
        self.pharmacy_table.heading('Date Of Purchase',text='Date Of Purchase')
        self.pharmacy_table.heading('Quantity',text='Quantity')
        self.pharmacy_table.heading('Price Per Item',text='Price Per Item')
        self.pharmacy_table.heading('invoice',text='invoice')
        self.pharmacy_table.heading('ManufactureDate',text='Manufacture Date')
        self.pharmacy_table.heading('Expiry Date',text='Expiry Date')
        self.pharmacy_table.heading('batchNo',text='batchNo')
        self.pharmacy_table.heading('WholesalerName',text='WholesalerName')
        
        
        
        self.pharmacy_table.pack(fill=BOTH,expand=1)

        self.pharmacy_table.column('Med Id',width=100)
        self.pharmacy_table.column('Medicine Name',width=100)
        self.pharmacy_table.column('Date Of Purchase',width=100)
        self.pharmacy_table.column('Quantity',width=100)
        self.pharmacy_table.column('Price Per Item',width=100)
        self.pharmacy_table.column('invoice',width=100)
        self.pharmacy_table.column('ManufactureDate',width=100)
        self.pharmacy_table.column('Expiry Date',width=100)
        self.pharmacy_table.column('batchNo',width=100)
        self.pharmacy_table.column('WholesalerName',width=100)

        self.see_all_but=Button(self.entry_frame,text='See All',font=('Arial',14),bd=4,width=15,height=2,command=self.on_see_all)
        self.see_all_but.grid(row=3,column=1,padx=5,pady=5)

        self.mini_frame=Frame(self.entry_frame,bd=2,bg='lightgrey',relief=RIDGE)
        self.mini_frame.place(x=20,y=330,width=500,height=180)

        self.med_name_lbl=Label(self.mini_frame,text='Medicine Id',font=('Arial',15),bg='lightgrey')
        self.med_name_lbl.grid(row=0,column=0,padx=20,pady=5)
        self.med_name_entry=Entry(self.mini_frame,relief=RIDGE,width=25,font=('Arial',15))
        self.med_name_entry.grid(row=0,column=1,padx=5,pady=5)

        self.qntity_lbl=Label(self.mini_frame,text='Quantity',font=('Arial',15),bg='lightgrey')
        self.qntity_lbl.grid(row=1,column=0,padx=20,pady=5)
        self.qntity_entry=Entry(self.mini_frame,relief=RIDGE,width=25,font=('Arial',15))
        self.qntity_entry.grid(row=1,column=1,padx=5,pady=5)

        self.cost_lbl=Label(self.mini_frame,text='Cost',font=('Arial',15),bg='lightgrey')
        self.cost_lbl.grid(row=2,column=0,padx=20,pady=5)
        self.cost_entry=Entry(self.mini_frame,relief=RIDGE,width=25,font=('Arial',15))
        self.cost_entry.grid(row=2,column=1,padx=5,pady=5)

        self.sub_but=Button(self.mini_frame,bd=4,relief=GROOVE,text='Submit',state=DISABLED,width=10,font=('Arial',15,'bold'),command=self.update_stcck_1)
        self.sub_but.grid(row=3,column=0,padx=7,pady=7)

        self.clear_but=Button(self.mini_frame,bd=4,relief=GROOVE,text='Clear',width=10,font=('Arial',15,'bold'),command=clear_entry)
        self.clear_but.grid(row=3,column=1,padx=7,pady=7)

    def on_see_all(self):
        display_all(self)
    
    def low_quantity(self):
        low_qnt_items(self)
    
    def update_stcck_1(self):
        update_stock(self)

class delete_record:
    def __init__(self,win):
        self.win=win
        self.win.geometry("800x400")
        self.win.title("Delete")

        self.title_lbl=Label(self.win,text="+  MediCare Pharmacy  +",bg="green",fg="yellow",bd=5,relief=GROOVE,font=("Times",25,"bold"))
        self.title_lbl.pack(side="top",fill='x')

        self.purchase_lbl=Label(self.win,text="--------Delete Section--------",bg="white",fg="green",bd=5,relief=GROOVE,font=("Times",25,"bold"))
        self.purchase_lbl.pack(side='top',fill='x',pady=5)

        self.entry_frame=LabelFrame(self.win,text='Delete Data',bg='lightgrey',fg='darkgreen',bd=5,font=('Arial',15,'bold'))
        self.entry_frame.place(x=20,y=120,width=700,height=300)

        self.Med_id=Label(self.entry_frame,text='Enter id',bg='lightgrey',font=('Claibri',16))
        self.Med_id.grid(row=0,column=0,padx=4,pady=4)
        global Med_id_entry
        Med_id_entry=Entry(self.entry_frame,bd=4,relief=GROOVE,width=20,font=('Calibri',15))
        Med_id_entry.grid(row=0,column=1,padx=4,pady=4)

        self.medicine_name=Label(self.entry_frame,text='Medicine Name',bg='lightgrey',font=('Claibri',16))
        self.medicine_name.grid(row=1,column=0,padx=4,pady=4)
        global medicine_entry
        medicine_entry=Entry(self.entry_frame,bd=4,relief=GROOVE,width=20,font=('Calibri',15))
        medicine_entry.grid(row=1,column=1,padx=4,pady=4)

        # Button Frame

        self.but_frame=LabelFrame(self.entry_frame,bg='lightgrey',relief=FLAT)
        self.but_frame.place(x=20,y=150,width=300,height=50)
            

        self.delete_but=Button(self.but_frame,text='Delete',font=('Arial',14,'bold'),bd=4,relief=RIDGE,width=10,command=self.del_record)
        self.delete_but.grid(row=0,column=0,padx=10,pady=5)

        self.delete_all_but=Button(self.but_frame,text='Delete All',font=('Arial',14,'bold'),bd=4,relief=RIDGE,width=10,command=self.del_all)
        self.delete_all_but.grid(row=0,column=1,padx=10,pady=5)

    def del_record(self):
        delete_record_fun(self)

    def del_all(self):
        delete_all_records(self)


class sales_window:
    def __init__(self,win):
        self.win=win
        self.win.geometry("1300x700")
        self.win.title("Delete")

        self.title_lbl=Label(self.win,text="+  MediCare Pharmacy  +",bg="green",fg="yellow",bd=5,relief=GROOVE,font=("Times New Roman",33,"bold"))
        self.title_lbl.pack(side="top",fill='x')

        self.purchase_lbl=Label(self.win,text="-------Sales History--------",bg="white",fg="darkgreen",bd=5,relief=GROOVE,font=("Times New Roman",28,"bold"))
        self.purchase_lbl.pack(side='top',fill='x',pady=5)

        # Button Frame

        # self.but_frame=LabelFrame(self.win,bg='white',relief=FLAT)
        # self.but_frame.place(x=20,y=150,width=400,height=50)

        # self.lblSearch=Label(self.but_frame,font=('Times New Roman',20,'bold'),text='Search By',padx=2,bg='white',fg='darkgreen')
        # self.lblSearch.grid(row=0,column=0,sticky=W)

        self.total=total_trans()

        self.lblTotal=Label(self.win,font=('Times New Roman',20,'bold'),text='Total Transaction : ₹'+self.total,padx=2,bg='white',fg='darkgreen')
        self.lblTotal.place(x=380,y=150,height=50,width=400)

        # self.search_combo=ttk.Combobox(self.but_frame,width=12,font=('Times New Roman',15,'bold'),state='readonly')
        # self.search_combo['values']=('Medname','patientId')
        # self.search_combo.grid(row=0,column=2)
        # self.search_combo.current(0)

        # create listbox

        self.framedet=Frame(self.win,bd=5,relief=RIDGE)
        self.framedet.place(x=250,y=220,width=800,height=400)

        self.sc_x=ttk.Scrollbar(self.framedet,orient=HORIZONTAL)
        self.sc_x.pack(side=BOTTOM,fill=X)
        self.sc_y=ttk.Scrollbar(self.framedet,orient=VERTICAL)
        self.sc_y.pack(side=RIGHT,fill=Y)

        self.pharmacy_table=ttk.Treeview(self.framedet,columns=('Patient Id','Patient Name','Medicine Name','Date Of Purchase','Price Per Item'),xscrollcommand=self.sc_x.set,yscrollcommand=self.sc_y.set)
        self.sc_x.config(command=self.pharmacy_table.xview)
        self.sc_y.config(command=self.pharmacy_table.yview)

        self.pharmacy_table['show']='headings'

        self.pharmacy_table.heading('Patient Id',text='Patient Id')
        self.pharmacy_table.heading('Patient Name',text='Patient Name')
        self.pharmacy_table.heading('Medicine Name',text='Medicine Name')
        self.pharmacy_table.heading('Date Of Purchase',text='Date Of Purchase')
        self.pharmacy_table.heading('Price Per Item',text='Price Per Item')
        self.pharmacy_table.pack(fill=BOTH,expand=1)

        self.pharmacy_table.column('Patient Id',width=100)
        self.pharmacy_table.column('Patient Name',width=100)
        self.pharmacy_table.column('Medicine Name',width=100)
        self.pharmacy_table.column('Date Of Purchase',width=100)
        self.pharmacy_table.column('Price Per Item',width=100)

        


        
        # self.listbox=Listbox(self.win,bg='lightgrey',bd=3)
        # self.listbox.place(x=20,y=220,width=680,height=280)
        sale_hist(self)


class patient_details:
    def __init__(self,win):
        self.win=win
        self.win.geometry("1300x700")
        self.win.title("Patient Details")

        self.title_lbl=Label(self.win,text="+  MediCare Pharmacy  +",bg="green",fg="yellow",bd=5,relief=GROOVE,font=("Times New Roman",33,"bold"))
        self.title_lbl.pack(side="top",fill='x')

        self.purchase_lbl=Label(self.win,text="-------Patient Details--------",bg="white",fg="darkgreen",bd=5,relief=GROOVE,font=("Times New Roman",28,"bold"))
        self.purchase_lbl.pack(side='top',fill='x',pady=5)

        #*********************************************************************************

        self.framedet=Frame(self.win,bd=5,relief=RIDGE)
        self.framedet.place(x=250,y=120,width=890,height=550)

        self.sc_x=ttk.Scrollbar(self.framedet,orient=HORIZONTAL)
        self.sc_x.pack(side=BOTTOM,fill=X)
        self.sc_y=ttk.Scrollbar(self.framedet,orient=VERTICAL)
        self.sc_y.pack(side=RIGHT,fill=Y)

        self.pharmacy_table=ttk.Treeview(self.framedet,columns=('Pat_Id','Patient_name','Patient_age','Medicine_name','Date_Of_Manufacture','Price_per_item'),xscrollcommand=self.sc_x.set,yscrollcommand=self.sc_y.set)
        self.sc_x.config(command=self.pharmacy_table.xview)
        self.sc_y.config(command=self.pharmacy_table.yview)

        self.pharmacy_table['show']='headings'

        self.pharmacy_table.heading('Pat_Id',text='Patient Id')
        self.pharmacy_table.heading('Patient_name',text='Patient_name')
        self.pharmacy_table.heading('Patient_age',text='Patient_age')
        self.pharmacy_table.heading('Medicine_name',text='Medicine_name')
        self.pharmacy_table.heading('Date_Of_Manufacture',text='Date_Of_Manufacture')
        self.pharmacy_table.heading('Price_per_item',text='Price_per_item')

        self.pharmacy_table.pack(fill=BOTH,expand=1)

        self.pharmacy_table.column('Pat_Id',width=100)
        self.pharmacy_table.column('Patient_name',width=100)
        self.pharmacy_table.column('Patient_age',width=100)
        self.pharmacy_table.column('Medicine_name',width=100)
        self.pharmacy_table.column('Date_Of_Manufacture',width=100)
        self.pharmacy_table.column('Price_per_item',width=100)

        display_pat_det(self)





        




if __name__=="__main__":
    main()



#SELECT * FROM medicines ORDER BY Med_id DESC LIMIT 1;
