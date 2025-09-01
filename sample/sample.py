import sqlite3
import tkinter as tk
from tkinter import messagebox, ttk


# Connect to SQLite database (or create it if it doesn't exist)
def connect_db():
    conn = sqlite3.connect('patient_severity.db')
    cursor = conn.cursor()
    # Create table if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS patients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            condition TEXT NOT NULL,
            severity INTEGER NOT NULL CHECK(severity BETWEEN 1 AND 10)
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
            severity = int(severity)
            if not (1 <= severity <= 10):
                raise ValueError("Severity must be between 1 and 10.")
            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO patients (name, condition, severity) VALUES (?, ?, ?)",
                           (name, condition, severity))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Patient added successfully!")
            clear_entries()
            show_data()
        except ValueError as ve:
            messagebox.showerror("Input Error", f"Invalid input: {ve}")
        except Exception as e:
            messagebox.showerror("Error", f"Error inserting data: {e}")
    else:
        messagebox.showwarning("Input Error", "Please provide all information (Name, Condition, Severity).")


# Retrieve and display data from the SQLite database, sorted by severity
def show_data(order='ASC'):
    for item in tree.get_children():
        tree.delete(item)

    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM patients ORDER BY severity {order}")
    rows = cursor.fetchall()
    conn.close()

    for row in rows:
        tree.insert('', tk.END, values=row)


# Clear input fields
def clear_entries():
    name_entry.delete(0, tk.END)
    condition_entry.delete(0, tk.END)
    severity_entry.delete(0, tk.END)


# Delete selected patient
def delete_data():
    selected_item = tree.selection()
    if selected_item:
        confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete the selected patient?")
        if confirm:
            item = tree.item(selected_item)
            patient_id = item['values'][0]
            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM patients WHERE id=?", (patient_id,))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Patient deleted successfully!")
            show_data()
    else:
        messagebox.showwarning("Selection Error", "Please select a patient to delete.")


# Update selected patient
def update_data():
    selected_item = tree.selection()
    if selected_item:
        item = tree.item(selected_item)
        name, condition, severity = item['values']

        # Open a new window to update data
        update_window = tk.Toplevel(root)
        update_window.title("Update Patient")
        center_window(update_window, 400, 250)

        # Labels and Entry Fields for update
        tk.Label(update_window, text="Name:").grid(row=0, column=0, padx=10, pady=10, sticky='e')
        update_name_entry = tk.Entry(update_window)
        update_name_entry.grid(row=0, column=1, padx=10, pady=10)
        update_name_entry.insert(0, name)

        tk.Label(update_window, text="Condition:").grid(row=1, column=0, padx=10, pady=10, sticky='e')
        update_condition_entry = tk.Entry(update_window)
        update_condition_entry.grid(row=1, column=1, padx=10, pady=10)
        update_condition_entry.insert(0, condition)

        tk.Label(update_window, text="Severity (1-10):").grid(row=2, column=0, padx=10, pady=10, sticky='e')
        update_severity_entry = tk.Entry(update_window)
        update_severity_entry.grid(row=2, column=1, padx=10, pady=10)
        update_severity_entry.insert(0, severity)

        # Function to save updates
        def save_updates():
            new_name = update_name_entry.get().strip()
            new_condition = update_condition_entry.get().strip()
            new_severity = update_severity_entry.get().strip()

            if new_name and new_condition and new_severity:
                try:
                    new_severity = int(new_severity)
                    if not (1 <= new_severity <= 10):
                        raise ValueError("Severity must be between 1 and 10.")
                    conn = connect_db()
                    cursor = conn.cursor()
                    cursor.execute("""
                        UPDATE patients 
                        SET name = ?, condition = ?, severity = ?
                        WHERE name = ?
                    """, (new_name, new_condition, new_severity, name))
                    conn.commit()
                    conn.close()
                    messagebox.showinfo("Success", "Patient updated successfully!")
                    update_window.destroy()
                    show_data()
                except ValueError as ve:
                    messagebox.showerror("Input Error", f"Invalid input: {ve}")
                except Exception as e:
                    messagebox.showerror("Error", f"Error updating data: {e}")
            else:
                messagebox.showwarning("Input Error", "Please provide all information (Name, Condition, Severity).")

        # Save Button
        save_button = tk.Button(update_window, text="Save", command=save_updates)
        save_button.grid(row=3, column=0, columnspan=2, pady=20)
    else:
        messagebox.showwarning("Selection Error", "Please select a patient to update.")


# Search patients by name
def search_data():
    search_name = search_entry.get().strip()

    for item in tree.get_children():
        tree.delete(item)

    if search_name:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM patients WHERE name LIKE ?", ('%' + search_name + '%',))
        rows = cursor.fetchall()
        conn.close()

        if rows:
            for row in rows:
                tree.insert('', tk.END, values=row)
        else:
            messagebox.showinfo("No Results", "No patient found with the given name.")
    else:
        messagebox.showwarning("Input Error", "Please enter a name to search.")


# Function to center the window
def center_window(window, width=600, height=500):
    window.update_idletasks()
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)

    window.geometry(f'{width}x{height}+{x}+{y}')


# Create Tkinter window
root = tk.Tk()
root.title("Patient Severity Database")

# Center the window
center_window(root, 800, 600)

# Configure grid layout
root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=3)

# Labels and Entry Fields
tk.Label(root, text="Name:").grid(row=0, column=0, padx=10, pady=10, sticky='e')
name_entry = tk.Entry(root)
name_entry.grid(row=0, column=1, padx=10, pady=10, sticky='w')

tk.Label(root, text="Condition:").grid(row=1, column=0, padx=10, pady=10, sticky='e')
condition_entry = tk.Entry(root)
condition_entry.grid(row=1, column=1, padx=10, pady=10, sticky='w')

tk.Label(root, text="Severity (1-10):").grid(row=2, column=0, padx=10, pady=10, sticky='e')
severity_entry = tk.Entry(root)
severity_entry.grid(row=2, column=1, padx=10, pady=10, sticky='w')

# Insert Button
insert_button = tk.Button(root, text="Insert", width=15, command=insert_data)
insert_button.grid(row=3, column=0, padx=10, pady=10)

# Show Data Buttons
show_asc_button = tk.Button(root, text="Show Severity Asc", width=20, command=lambda: show_data('ASC'))
show_asc_button.grid(row=3, column=1, padx=10, pady=10, sticky='w')

show_desc_button = tk.Button(root, text="Show Severity Desc", width=20, command=lambda: show_data('DESC'))
show_desc_button.grid(row=3, column=1, padx=10, pady=10, sticky='e')

# Search Field and Button
tk.Label(root, text="Search by Name:").grid(row=4, column=0, padx=10, pady=10, sticky='e')
search_entry = tk.Entry(root)
search_entry.grid(row=4, column=1, padx=10, pady=10, sticky='w')

search_button = tk.Button(root, text="Search", width=15, command=search_data)
search_button.grid(row=4, column=1, padx=10, pady=10, sticky='e')

# Treeview to display data
columns = ("ID", "Name", "Condition", "Severity")
tree = ttk.Treeview(root, columns=columns, show='headings', selectmode='browse')
for col in columns:
    tree.heading(col, text=col)
    if col == "Name":
        tree.column(col, width=200)
    elif col == "Condition":
        tree.column(col, width=200)
    else:
        tree.column(col, width=100)

tree.grid(row=5, column=0, columnspan=1, padx=10, pady=10, sticky='nsew')
# tree.place(x=150, y=20, width=450, height=380)

# Add scrollbar to the Treeview
scrollbar = ttk.Scrollbar(root, orient=tk.VERTICAL, command=tree.yview)
tree.configure(yscroll=scrollbar.set)
scrollbar.grid(row=5, column=2, sticky='ns')

# Configure grid weights for Treeview resizing
root.rowconfigure(5, weight=1)
root.columnconfigure(1, weight=1)

# Buttons for Delete and Update
delete_button = tk.Button(root, text="Delete Selected", width=15, command=delete_data)
delete_button.grid(row=6, column=0, padx=10, pady=10, sticky='w')

update_button = tk.Button(root, text="Update Selected", width=15, command=update_data)
update_button.grid(row=6, column=1, padx=10, pady=10, sticky='e')

# Populate the initial data
show_data()

# Run the application
root.mainloop()
