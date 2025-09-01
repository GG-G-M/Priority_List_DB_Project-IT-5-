import sqlite3
import tkinter as tk
from tkinter import messagebox


# Connect to SQLite database (or create it if it doesn't exist)
def connect_db():
    conn = sqlite3.connect('my_database.db')
    cursor = conn.cursor()
    # Create table if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS person (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            age INTEGER
        )
    ''')
    conn.commit()
    return conn


# Insert data into the SQLite database
def insert_data():
    name = name_entry.get()
    age = age_entry.get()

    if name and age:
        try:
            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO person (name, age) VALUES (?, ?)", (name, age))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Data inserted successfully!")
            clear_entries()
        except Exception as e:
            messagebox.showerror("Error", f"Error inserting data: {e}")
    else:
        messagebox.showwarning("Input Error", "Please provide both name and age.")


# Retrieve and display data from the SQLite database
def show_data():
    listbox.delete(0, tk.END)  # Clear the listbox before showing data

    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM person")
    rows = cursor.fetchall()
    conn.close()

    for row in rows:
        listbox.insert(tk.END, f"ID: {row[0]}, Name: {row[1]}, Age: {row[2]}")


# Clear input fields
def clear_entries():
    name_entry.delete(0, tk.END)
    age_entry.delete(0, tk.END)


# Setup GUI with Tkinter
root = tk.Tk()
root.title("SQLite3 Database GUI")

# Labels and Entry Fields
tk.Label(root, text="Name:").grid(row=0, column=0)
name_entry = tk.Entry(root)
name_entry.grid(row=0, column=1)

tk.Label(root, text="Age:").grid(row=1, column=0)
age_entry = tk.Entry(root)
age_entry.grid(row=1, column=1)

# Buttons
insert_button = tk.Button(root, text="Insert", command=insert_data)
insert_button.grid(row=2, column=0, pady=10)

show_button = tk.Button(root, text="Show Data", command=show_data)
show_button.grid(row=2, column=1, pady=10)

# Listbox to display data
listbox = tk.Listbox(root, width=40, height=10)
listbox.grid(row=3, column=0, columnspan=2, pady=10)

root.mainloop()
