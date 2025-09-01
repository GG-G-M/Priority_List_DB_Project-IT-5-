import sqlite3
import tkinter as tk
from tkinter import messagebox


# Connect to SQLite database (or create it if it doesn't exist)
def connect_db():
    conn = sqlite3.connect('patient_severity.db')
    cursor = conn.cursor()
    # Create table if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS patients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            condition TEXT,
            severity INTEGER
        )
    ''')
    conn.commit()
    return conn


# Insert data into the SQLite database
def insert_data():
    name = name_entry.get()
    condition = condition_entry.get()
    severity = severity_entry.get()

    if name and condition and severity:
        try:
            severity = int(severity)  # Ensure severity is an integer
            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO patients (name, condition, severity) VALUES (?, ?, ?)",
                           (name, condition, severity))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Data inserted successfully!")
            clear_entries()
        except ValueError:
            messagebox.showerror("Error", "Severity must be a number.")
        except Exception as e:
            messagebox.showerror("Error", f"Error inserting data: {e}")
    else:
        messagebox.showwarning("Input Error", "Please provide all information (Name, Condition, Severity).")


# Retrieve and display data from the SQLite database, sorted by severity
def show_data(order='ASC'):
    listbox.delete(0, tk.END)  # Clear the listbox before showing data

    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(f"SELECT name, condition, severity FROM patients ORDER BY severity {order}")
    rows = cursor.fetchall()
    conn.close()

    for row in rows:
        listbox.insert(tk.END, f"Name: {row[0]}, Condition: {row[1]}, Severity: {row[2]}")


# Clear input fields
def clear_entries():
    name_entry.delete(0, tk.END)
    condition_entry.delete(0, tk.END)
    severity_entry.delete(0, tk.END)


# Setup GUI with Tkinter
root = tk.Tk()
root.title("Patient Severity Database")

# Labels and Entry Fields
tk.Label(root, text="Name:").grid(row=0, column=0)
name_entry = tk.Entry(root)
name_entry.grid(row=0, column=1)

tk.Label(root, text="Condition:").grid(row=1, column=0)
condition_entry = tk.Entry(root)
condition_entry.grid(row=1, column=1)

tk.Label(root, text="Severity (1-10):").grid(row=2, column=0)
severity_entry = tk.Entry(root)
severity_entry.grid(row=2, column=1)

# Buttons for inserting data and showing sorted data
insert_button = tk.Button(root, text="Insert", command=insert_data)
insert_button.grid(row=3, column=0, pady=10)

asc_button = tk.Button(root, text="Show (Severity Ascending)", command=lambda: show_data('ASC'))
asc_button.grid(row=3, column=1, pady=10)

desc_button = tk.Button(root, text="Show (Severity Descending)", command=lambda: show_data('DESC'))
desc_button.grid(row=4, column=1, pady=10)

# Listbox to display data
listbox = tk.Listbox(root, width=50, height=10)
listbox.grid(row=5, column=0, columnspan=2, pady=10)

root.mainloop()