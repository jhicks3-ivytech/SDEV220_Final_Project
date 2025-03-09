import tkinter as tk
import sqlite3
from tkinter import filedialog, messagebox, Toplevel, ANCHOR, Scrollbar
import pandas as pd
from tkinter.font import Font

# Main window class
class MainWindow:
    def __init__(self,db):
        # Create the main application window
        self.db = db
        self.conn = self.db.conn
        self.curr = self.db.cursor
        self.root = tk.Tk()
        self.root.title("Tool Crib")  # Set the title
        self.root.minsize(400,400)
        self.root.config(bg='#1E1E78')
        self.create_widgets()
        self.query_available()
        self.query_unavailable()

        # Start the main event loop
        self.root.mainloop()


    def check_out(self):
        #Window and logic for checking out tools
        popup = Toplevel(self.root)
        popup.title("Check Out")
        popup.minsize(400,400)
        popup.config(bg='#DEDEF6')
        title = tk.Label(popup,text='Select a Tool and Employee to Check Out',font=("calibri", 20, "bold"),anchor="center")
        title.grid(row=0,column=0,columnspan=3,sticky='nsew')
        title.config(bg='#DEDEF6')
        label1 = tk.Label(popup, text='Tool', font=(16))
        label1.grid(row=1, column=0)
        label1.config(bg='#DEDEF6')
        label2 = tk.Label(popup, text='Employee', font=(16))
        label2.grid(row=1, column=1)
        label2.config(bg='#DEDEF6')

        # Add a List Box
        self.listbox1 = tk.Listbox(popup, height=20, width=40,exportselection=False)
        self.listbox1.grid(row=2,column=0, padx=(10,5), pady=(0,10))
        self.listbox1.config(bg='#D4D4F4')
        self.listbox2 = tk.Listbox(popup, height=20, width=40, exportselection=False)
        self.listbox2.grid(row=2,column=1, padx=(10,0), pady=(0,10))
        self.listbox2.config(bg='#D4D4F4')
        scrollbar1 = tk.Scrollbar(popup, orient="vertical", command=self.listbox1.yview)
        scrollbar1.grid(row=2, column=0, sticky='nse')
        self.listbox1.config(yscrollcommand=scrollbar1.set)
        scrollbar2 = tk.Scrollbar(popup, orient="vertical", command=self.listbox2.yview)
        scrollbar2.grid(row=2, column=1, sticky='nse')
        self.listbox2.config(yscrollcommand=scrollbar2.set)


        #Populate List box of available tools
        tools = self.db.fetch_available()
        self.listbox1.delete(0,tk.END)
        for tool in tools:
            self.listbox1.insert(tk.END,f"{tool[0]}, {tool[1]}, {tool[2]}")
        employees = self.db.fetch_employees()
        self.listbox2.delete(0,tk.END)
        for employee in employees:
            self.listbox2.insert(tk.END, f"{employee[1]}, {employee[2]}, {employee[3]}")

        def sign_out():
            #Sign out selected tool too selected employee
            list1 = self.listbox1.get(ANCHOR).split(", ")
            list2 = self.listbox2.get(ANCHOR).split(", ")
            record = "INSERT INTO checkouts (id, tool, serial_number, name, department, shift) VALUES (?,?,?,?,?,?)"
            update = "UPDATE tools SET available = 0 WHERE id = (?)"
            self.curr.execute(record, (list1[0], list1[1],list1[2], list2[0], list2[1], list2[2]))
            self.curr.execute(update, (list1[0],))
            self.conn.commit()
            popup.destroy()
            self.query_available()
            self.query_unavailable()

        tk.Button(popup, width=20, text="Submit", command=sign_out).grid(row=3, column=0,sticky='E',padx=(0,10))
        tk.Button(popup, width=20, text="Cancel", command=popup.destroy).grid(row=3, column=1,sticky='W',padx=(10,0))

    def check_in(self):
        popup = Toplevel(self.root)
        popup.title("Check In")
        popup.minsize(400,400)
        popup.config(bg='#DEDEF6')
        title = tk.Label(popup,text='Select a Tool to Check In',font=("calibri", 20, "bold"),anchor="center")
        title.grid(row=0,column=0,columnspan=3,sticky='nsew')
        title.config(bg='#DEDEF6')
        label1 = tk.Label(popup, text='Tool', font=(16))
        label1.grid(row=1, column=0, columnspan=2)
        label1.config(bg='#DEDEF6')
        

        # Add a List Box
        self.listbox1 = tk.Listbox(popup, height=20, width=40,exportselection=False)
        self.listbox1.grid(row=2,column=0, columnspan=3, padx=(10,5), pady=(0,10))
        self.listbox1.config(bg='#D4D4F4')
        scrollbar1 = tk.Scrollbar(popup, orient="vertical", command=self.listbox1.yview)
        scrollbar1.grid(row=2, column=0, columnspan=3, sticky='nse')
        self.listbox1.config(yscrollcommand=scrollbar1.set)        


        #Populate List box of unavailable tools
        tools = self.db.fetch_not_available()
        self.listbox1.delete(0,tk.END)
        for tool in tools:
            self.listbox1.insert(tk.END,f"{tool[0]}, {tool[1]}, {tool[2]}")
        

        def sign_in():
            #Sign out selected tool to selected employee
            list1 = self.listbox1.get(ANCHOR).split(", ")
            available = 1
            id = list1[0]
            record = self.db.update_status(available, id)
            update = "DELETE FROM checkouts WHERE id = (?)"
            self.curr.execute(update, (id,))
            self.conn.commit()
            popup.destroy()
            self.query_available()
            self.query_unavailable()

        tk.Button(popup, width=20, text="Submit", command=sign_in).grid(row=3, column=0,sticky='E',padx=(0,10))
        tk.Button(popup, width=20, text="Cancel", command=popup.destroy).grid(row=3, column=1,sticky='W',padx=(10,0))

    def open_out_list(self):
        #Window to show what is checked out and to whom
        popup = Toplevel(self.root)
        popup.title("Out List")
        popup.minsize(900,500)                  
        popup.config(bg='#DEDEF6')
        title = tk.Label(popup,text='Tools Still Checked Out',font=("calibri", 20, "bold"),anchor="center")
        title.grid(row=0,column=0,columnspan=3,sticky='nsew')
        title.config(bg='#DEDEF6')
               

        # Add a Text Box
        self.textbox = tk.Text(popup, height=20, width=40, bg='#D4D4F4', wrap="none")
        self.textbox.grid(row=2, column=0, columnspan=2, padx=(10, 5), pady=(0, 10), sticky="nsew")

        # Configure grid to allow resizing
        popup.grid_columnconfigure(0, weight=1)  
        popup.grid_rowconfigure(2, weight=1)   

        # Add vertical scrollbar
        scrollbar1 = Scrollbar(popup, orient="vertical", command=self.textbox.yview)
        scrollbar1.grid(row=2, column=2, sticky='ns')  
        self.textbox.config(yscrollcommand=scrollbar1.set)

        # Add horizontal scrollbar (optional)
        h_scrollbar = Scrollbar(popup, orient="horizontal", command=self.textbox.xview)
        h_scrollbar.grid(row=3, column=0, columnspan=2, sticky="ew")
        self.textbox.config(xscrollcommand=h_scrollbar.set)

        # Populate Textbox with unavailable tools
        rows = self.db.fetch_checkouts()
        df = pd.DataFrame(rows)

        # Clear the Textbox
        self.textbox.delete("1.0", tk.END)

        # Insert header row into Textbox
        self.textbox.insert(tk.END, f"{'ID':<5}{'Tool':<30}{'Serial Number':<20}{'Name':<28}{'Department':<15}{'Shift':<10}\n")
        self.textbox.insert(tk.END, "_" * 105 + "\n")

        # Insert rows from the database
        for row in rows:
            self.textbox.insert(tk.END, f"{row[0]:<5}{row[1]:<30}{row[2]:<20}{row[3]:<28}{row[4]:<15}{row[5]:<10}\n")
        

        def download():
            import os
            with open("out_list.txt", "w") as file:
                file.write(self.textbox.get("1.0", tk.END)) 
            messagebox.showinfo("Save Successful","Data saved to out_list.txt")
            popup.destroy()
            os.startfile("out_list.txt")


        tk.Button(popup, width=20, text="Download", command=download).grid(row=4, column=0,sticky='E',padx=(0,10), pady=(10,10))
        tk.Button(popup, width=20, text="Cancel", command=popup.destroy).grid(row=4, column=1,sticky='W',padx=(10,0), pady=(10,10))
    

    def query_available(self):
        tools = self.db.fetch_available()
        if tools:
            cols = ['ID','Tool','Serial Number']
            df = pd.DataFrame(tools,columns=cols)
            df_string = df.to_string(index=False)
            self.textbox1.delete(1.0,tk.END)
            self.textbox1.insert(tk.END,df_string)
        else:
            self.textbox1.insert(tk.END,"All tools are checked out.")


    def query_unavailable(self):
        tools = self.db.fetch_not_available()
        if tools:
            cols = ['ID','Tool','Serial Number']
            df = pd.DataFrame(tools,columns=cols)
            df_string = df.to_string(index=False)
            self.textbox2.delete(1.0,tk.END)
            self.textbox2.insert(tk.END,df_string)
        else:
            self.textbox2.delete(1.0,tk.END)
            self.textbox2.insert(tk.END,"All tools are checked in.")
        

    def manage_employees(self):
        popup = Toplevel(self.root) 
        popup.title("Manage Employees")
        popup.geometry("300x200+400+300")
        popup.config(bg='#DEDEF6')

        tk.Label(popup, text="Employee ID").grid(row=0, column=0,sticky='E')
        id_entry = tk.Entry(popup)
        id_entry.grid(row=0, column=1)
        tk.Label(popup, text="Name").grid(row=1, column=0,sticky='E')
        name_entry = tk.Entry(popup)
        name_entry.grid(row=1,column=1)
        tk.Label(popup, text="Department").grid(row=2,column=0,sticky='E')
        dept_entry = tk.Entry(popup)
        dept_entry.grid(row=2,column=1)
        tk.Label(popup, text="Shift").grid(row=3,column=0,sticky='E')
        shift_entry = tk.Entry(popup)
        shift_entry.grid(row=3,column=1)

        def submit():
            try:
                emp_id = int(id_entry.get())
                name = name_entry.get()
                dept = dept_entry.get()
                shift = shift_entry.get()
                # Add other fields and database logic here
                self.db.add_employee(emp_id, name, dept, shift)
                messagebox.showinfo("Success", "Employee added successfully!")
                popup.destroy()
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {e}")

        tk.Button(popup, text="Submit", command=submit).grid(row=4, column=0,sticky='E',pady=10)
        tk.Button(popup, text="Cancel", command=popup.destroy).grid(row=4, column=1,sticky='W',pady=10)
        tk.Button(popup, text="Import from Template", command=lambda: self.import_csv
                  (table='employees', conn=self.conn)).grid(row=5, column=0,columnspan=2,sticky='EW',pady=10)
        

    def manage_tools(self):
        popup = Toplevel(self.root) 
        popup.title("Manage Tools")
        popup.geometry("300x200+400+300")
        popup.config(bg='#DEDEF6')

        tk.Label(popup, text="Tool ID").grid(row=0, column=0,sticky='E')
        id_entry = tk.Entry(popup)
        id_entry.grid(row=0, column=1)
        tk.Label(popup, text="Description").grid(row=1, column=0,sticky='E')
        name_entry = tk.Entry(popup)
        name_entry.grid(row=1,column=1)
        tk.Label(popup, text="Serial Number").grid(row=2,column=0,sticky='E')
        sn_entry = tk.Entry(popup)
        sn_entry.grid(row=2,column=1)
        
        def submit():
            try:
                tool_id = int(id_entry.get())
                desc = name_entry.get()
                sn = sn_entry.get()
                available = 1
                self.db.add_tool(tool_id, desc, sn, available)
                messagebox.showinfo("Success", "Tool added successfully!")
                self.query_available()
                self.query_unavailable()
                popup.destroy()
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {e}")

        tk.Button(popup, text="Submit", command=submit).grid(row=4, column=0,sticky='E',pady=10)
        tk.Button(popup, text="Cancel", command=popup.destroy).grid(row=4, column=1,sticky='W',pady=10)
        tk.Button(popup, text="Import from Template", command=lambda: self.import_csv
                  (table='tools', conn=self.conn)).grid(row=5, column=0,columnspan=2,sticky='EW',pady=10)



    def import_csv(self,table, conn):
        file = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        df = pd.read_csv(file)
        df.to_sql(table, conn, if_exists='append', index=False)
        self.query_available()
        self.query_unavailable()

    def create_widgets(self):
        # Add Button1
        button1 = tk.Button(self.root, text="Check Out", width=20, command=self.check_out)
        button1.grid(row=1,column=11,columnspan=3, padx=(10,10), pady=(5,5))

        # Add Button2
        button2 = tk.Button(self.root, text="Check In", width=20, command=self.check_in)
        button2.grid(row=2,column=11,columnspan=3, padx=(10,10), pady=(5,5))

        # Add Button3
        button3 = tk.Button(self.root, text="Manage Tools", width=20, command=self.manage_tools)
        button3.grid(row=25,column=11,columnspan=3, padx=(10,10), pady=(5,5))

        # Add Button4
        button4 = tk.Button(self.root, text="Manage People", width=20, command=self.manage_employees)
        button4.grid(row=26,column=11,columnspan=3, padx=(10,10), pady=(5,5))

        # Add Exit Button
        button5 = tk.Button(self.root, text="Exit", width=20, command=self.root.destroy)
        button5.grid(row=27,column=11,columnspan=3, padx=(10,10), pady=(5,5))

        # Add Out List Button
        button6 = tk.Button(self.root, text="Out List", width=20, command=self.open_out_list)
        button6.grid(row=24,column=11,columnspan=3, padx=(10,10), pady=(5,5))

        # Add a Label for Text Box
        label1 = tk.Label(self.root, text='Available', font=(24))
        label1.grid(row=1, column=1, columnspan=5)
        label1.config(bg='#1E1E78', fg='#F5F5F5')
        label2 = tk.Label(self.root, text='Checked Out', font=(24))
        label2.grid(row=1, column=6, columnspan=5)
        label2.config(bg='#1E1E78', fg='#F5F5F5')


        # Add a Text Box
        self.textbox1 = tk.Text(self.root, height=20, width=40)
        self.textbox1.grid(row=2,column=1,columnspan=5,rowspan=25, padx=(10,5), pady=(0,10))
        self.textbox1.config(bg='#D4D4F4')
        self.textbox2 = tk.Text(self.root, height=20, width=40)
        self.textbox2.grid(row=2,column=6,columnspan=5,rowspan=25, padx=(10,0), pady=(0,10))
        self.textbox2.config(bg='#D4D4F4')

        title = tk.Label(self.root,text="Tool Crib Asset Management",font=("calibri", 24, "bold"),anchor="center")
        title.grid(row=0,column=1,columnspan=13,sticky='nsew')
        title.config(bg='#1E1E78', fg='#F5F5F5')




