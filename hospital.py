import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

# Database setup
def create_db():
    conn = sqlite3.connect('hospital.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS patients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            dob TEXT,
            address TEXT,
            phone TEXT
        )
    ''')
    conn.commit()
    conn.close()

class HospitalManagementSystem:
    def __init__(self, master):
        self.master = master
        self.master.title("Hospital Management System")
        
        self.create_widgets()
        create_db()

    def create_widgets(self):
        # Patient Details Frame
        frame = ttk.LabelFrame(self.master, text="Patient Details")
        frame.grid(row=0, column=0, padx=10, pady=10)

        # Name
        ttk.Label(frame, text="Name:").grid(row=0, column=0, padx=5, pady=5)
        self.name_var = tk.StringVar()
        ttk.Entry(frame, textvariable=self.name_var).grid(row=0, column=1, padx=5, pady=5)

        # DOB
        ttk.Label(frame, text="Date of Birth:").grid(row=1, column=0, padx=5, pady=5)
        self.dob_var = tk.StringVar()
        ttk.Entry(frame, textvariable=self.dob_var).grid(row=1, column=1, padx=5, pady=5)

        # Address
        ttk.Label(frame, text="Address:").grid(row=2, column=0, padx=5, pady=5)
        self.address_var = tk.StringVar()
        ttk.Entry(frame, textvariable=self.address_var).grid(row=2, column=1, padx=5, pady=5)

        # Phone
        ttk.Label(frame, text="Phone:").grid(row=3, column=0, padx=5, pady=5)
        self.phone_var = tk.StringVar()
        ttk.Entry(frame, textvariable=self.phone_var).grid(row=3, column=1, padx=5, pady=5)

        # Buttons
        ttk.Button(frame, text="Add Patient", command=self.add_patient).grid(row=4, column=0, columnspan=2, pady=10)
        ttk.Button(frame, text="View Patients", command=self.view_patients).grid(row=5, column=0, columnspan=2, pady=10)

    def add_patient(self):
        name = self.name_var.get()
        dob = self.dob_var.get()
        address = self.address_var.get()
        phone = self.phone_var.get()

        if not name or not dob or not address or not phone:
            messagebox.showwarning("Input Error", "All fields are required.")
            return

        conn = sqlite3.connect('hospital.db')
        c = conn.cursor()
        c.execute("INSERT INTO patients (name, dob, address, phone) VALUES (?, ?, ?, ?)", 
                  (name, dob, address, phone))
        conn.commit()
        conn.close()

        messagebox.showinfo("Success", "Patient added successfully!")
        self.clear_fields()

    def view_patients(self):
        conn = sqlite3.connect('hospital.db')
        c = conn.cursor()
        c.execute("SELECT * FROM patients")
        records = c.fetchall()
        conn.close()

        # Display records
        record_window = tk.Toplevel(self.master)
        record_window.title("Patient Records")
        
        tree = ttk.Treeview(record_window, columns=("ID", "Name", "DOB", "Address", "Phone"), show='headings')
        tree.heading("ID", text="ID")
        tree.heading("Name", text="Name")
        tree.heading("DOB", text="DOB")
        tree.heading("Address", text="Address")
        tree.heading("Phone", text="Phone")
        
        for record in records:
            tree.insert("", "end", values=record)
        
        tree.pack(expand=True, fill='both')
        ttk.Button(record_window, text="Close", command=record_window.destroy).pack(pady=10)

    def clear_fields(self):
        self.name_var.set("")
        self.dob_var.set("")
        self.address_var.set("")
        self.phone_var.set("")

if __name__ == "__main__":
    root = tk.Tk()
    app = HospitalManagementSystem(root)
    root.mainloop()