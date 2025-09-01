import sqlite3  # DataBase
import tkinter, os
from pathlib import Path
from tkinter import Tk, ttk, Canvas, Entry, Button, PhotoImage, messagebox, Toplevel  # GUI
from datetime import datetime
# Other Class
from center_window import center  # import center Class
from patient_continue import discharged, dead, view_data # import both Class
ASSETS_PATH = Path(r"D:\build\assets\frame0")
def asset_file(path: str) -> Path:  # Get the File Asset for Image
    return ASSETS_PATH / Path(path)


# Initialize Window
window = Tk()
window.title("Patient Priority")
center(window, 650, 450)
window.configure(bg="#FFFFFF")
window.resizable(False, False)

# Initialize Menu_bar
menu_bar = tkinter.Menu(window)
option_menu = tkinter.Menu(menu_bar, tearoff=0)
patient_menu = tkinter.Menu(menu_bar, tearoff=0)
reset_menu = tkinter.Menu(menu_bar, tearoff=0)

menu_bar.add_cascade(label="Info", menu=option_menu)  # Add the info menu to the menu bar || The following add Command under this Bar
option_menu.add_command(label="Help", command=lambda:
messagebox.showinfo("Info", "Continue Patient: Put the Patient either at Discharge|Dead List\n"
                            "Remove Patient: Remove Patient from List\n"
                            "Update Patient: update the Patient's Information\n"
                            "Add Patient: Add a new Patient\n"
                            "Exit: Exit the Program"))
option_menu.add_command(label="About", command=lambda:
messagebox.showinfo("About", "This Program keep tracks the priority of Patient and it's severity...\n"
                             "It also use DataBase from SQLite3, making it easy to run everywhere"))
option_menu.add_command(label="Creator", command=lambda:
messagebox.showinfo("Creator", "This Progam was Created by Gilgre Gene G. Mantilla for the Project for IT-5"))

menu_bar.add_cascade(label="Patient", menu=patient_menu) # Add the patient menu to the menu bar || The following add Command under this Bar
patient_menu.add_command(label="Discharged", command=lambda: view_data(window, "patient_discharged.db"))
patient_menu.add_command(label="Dead", command=lambda: view_data(window, "patient_dead.db"))
patient_menu.add_command(label="Reset Data", command=lambda: reset_data())
window.config(menu=menu_bar)  # Display the menu bar in the window


# Create DataBase
def connect_db():
    conn = sqlite3.connect('patient_severity.db')
    cursor = conn.cursor()
    # Create table if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS patients (
            name TEXT NOT NULL,
            condition TEXT NOT NULL,
            severity INTEGER NOT NULL,
            date TEXT NOT NULL,
            id INTEGER PRIMARY KEY AUTOINCREMENT
        )
    ''')
    conn.commit()
    return conn

# Change DataBase
def update_db(instruction, rows, message):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(instruction, (rows))  # Give Instruction to the Rows(Data)
    conn.commit()
    conn.close()
    messagebox.showinfo("Success", message)
    clear_input()
    show_data()

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
        tree.insert('', 'end', values=row)

# Continue Patient
def continue_patient():
    selected_item = tree.selection()
    if selected_item:
        item = tree.item(selected_item)
        name, condition, severity, date, id = item['values']
        def dellell():
            patient_id = item['values'][4]
            update_db("DELETE FROM patients WHERE id = ?", (patient_id,), "Patient Completed")
            update_window.destroy()

        # Open a new window to update data
        update_window = Toplevel(window)
        update_window.title("Update Patient")
        center(update_window, 350, 160)
        update_window.resizable(False, False)

        ttk.Label(update_window, text="Select what happened to the Patient", font=("Inter Bold", 20 * -1)).grid(row=0, column=0, padx=10, pady=10, sticky='e')
        save_button = ttk.Button(update_window, text="Discharge", command=lambda: discharged(name, condition, severity) and dellell())
        save_button.grid(row=1, column=0, columnspan=1, pady=10)
        save_button = ttk.Button(update_window, text="Dead", command=lambda: dead(name, condition, severity) and dellell())
        save_button.grid(row=2, column=0, columnspan=1, pady=10)
    else:
        messagebox.showwarning("Selection Error", "Please select a patient to continue.")

# delete Patient
def delete_patient():
    selected_item = tree.selection()
    if selected_item:
        confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete the selected patient?")
        if confirm:
            item = tree.item(selected_item)
            patient_id = item['values'][4]
            update_db("DELETE FROM patients WHERE id = ?", (patient_id,), "Patient deleted successfully!")
    else:
        messagebox.showwarning("Selection Error", "Please select a patient to delete.")

# Update Patient
def update_patient():
    selected_item = tree.selection()
    if selected_item:
        item = tree.item(selected_item)
        name, condition, severity, date, id = item['values']

        # Open a new window to update data
        update_window = Toplevel(window)
        update_window.title("Update Patient")
        center(update_window, 250, 225)
        update_window.resizable(False, False)

        # Labels and Entry Fields for update
        ttk.Label(update_window, text="Name:").grid(row=0, column=0, padx=10, pady=10, sticky='e')
        update_name_entry = ttk.Entry(update_window)
        update_name_entry.grid(row=0, column=1, padx=10, pady=10)
        update_name_entry.insert(0, name)

        ttk.Label(update_window, text="Condition:").grid(row=1, column=0, padx=10, pady=10, sticky='e')
        update_condition_entry = ttk.Entry(update_window)
        update_condition_entry.grid(row=1, column=1, padx=10, pady=10)
        update_condition_entry.insert(0, condition)

        ttk.Label(update_window, text="Severity (1-5):").grid(row=2, column=0, padx=10, pady=10, sticky='e')
        update_severity_entry = ttk.Entry(update_window)
        update_severity_entry.grid(row=2, column=1, padx=10, pady=10)
        update_severity_entry.insert(0, severity)

        # Function to save updates
        def save_updates():
            new_name = update_name_entry.get()
            new_condition = update_condition_entry.get()
            new_severity = update_severity_entry.get()

            if new_name and new_condition and new_severity:
                try:
                    new_severity = int(new_severity)
                    if not (1 <= new_severity <= 5):
                        raise ValueError("Severity must be between 1 and 5.")
                    conn = connect_db()
                    cursor = conn.cursor()
                    cursor.execute("""
                            UPDATE patients
                            SET name = ?, condition = ?, severity = ?
                            WHERE id = ?
                        """, (new_name, new_condition, new_severity, id))
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
        save_button = ttk.Button(update_window, text="Save", command=save_updates)
        save_button.grid(row=3, column=0, columnspan=2, pady=20)
    else:
        messagebox.showwarning("Selection Error", "Please select a patient to update.")

# Add Patient
def add_patient():
    # Get values from all three entries
    name = entry_1.get()
    condition = entry_2.get().lower()
    severity = entry_3.get()
    date = datetime.now().strftime("%d/%m/%Y | %H:/%M:/%S")

    if name and condition:
        normal = ["flu", "cold", "fever", "sprain", "sore throat", "chickenpox", "swelling", "diarrhea", "bruise", "dysmenorrhoea", "cramps"]
        mild = ["allergies", "allergy", "hiv", "sti", "diabetes", "malaria", "uti", "chlamydia", "gallstones", "herpes"]
        moderate = ["cripple", "cancer", "pneumonia", "tuberculosis", "infection", "monkeypox"]
        severe = ["co-vid", "epilepsy", "seizure", "tumor"]
        critical = ["heart attack", "bleeding", "stab", "shot", "stroke"]

        if severity == "?":
            if condition in normal:
                severity = int(5)
            if condition in mild:
                severity = int(4)
            if condition in moderate:
                severity = int(3)
            if condition in severe:
                severity = int(2)
            if condition in critical:
                severity = int(1)

        try:
            severity = int(severity)
            if not (1 <= severity <= 5):
                raise ValueError("Severity must be between 1 and 5.")

            update_db("INSERT INTO patients (name, condition, severity, date) VALUES (?, ?, ?, ?)",
                      (name, condition, severity, date), "Patient added successfully!")
        except ValueError as ve:
            messagebox.showerror("Input Error", f"Invalid input: accept only (1-5) or (?)")
        except Exception as e:
            messagebox.showerror("Error", f"Error inserting data: {e}")
    else:
        messagebox.showwarning("Input Error", "Please provide all information (Name, Condition, Severity).")

# reset database
def reset_data():
    confirm = messagebox.askyesno("Delete", "Are you sure you want to reset the file")
    if confirm:
        files = ["patient_severity.db", "patient_discharged.db", "patient_dead.db"]
        for x in files:
            os.remove(x)
        show_data()

# clear input/entry
def clear_input():
    entry_1.delete(0, 'end')
    entry_2.delete(0, 'end')
    entry_3.delete(0, 'end')

# Layout
canvas = Canvas(
    window,
    bg="#FFFFFF",
    height=400,
    width=650,
    bd=0,
    highlightthickness=0,
    relief="ridge"
)

canvas.place(x=0, y=0)
canvas.create_rectangle(0.0, 0.0, 150.0, 400.0, fill="#FFFFFF", outline="")
canvas.create_rectangle(150.0, 0.0, 600.0, 400.0, fill="#81FF75", outline="")

# RECTANGLE #
canvas.create_rectangle(300.0, 0.0, 375.0, 400.0, fill="#FF7272", outline="")  # red
canvas.create_rectangle(450.0, 0.0, 375.0, 400.0, fill="#00C2FF", outline="")  # blue
canvas.create_rectangle(650.0, 0.0, 600.0, 400.0, fill="#FF17E8", outline="")  # purple

image_image_1 = PhotoImage(
    file=asset_file("image_1.png"))
image_1 = canvas.create_image(75.0, 366.0,
                              image=image_image_1)

# LABEL #
canvas.create_text(19.0, 0.0, anchor="nw", text="Patient Priority List", fill="#000000", font=("Inter Bold", 12 * -1))
canvas.create_text(208.0, 0.0, anchor="nw", text="Name", fill="#000000", font=("Inter Bold", 12 * -1))
canvas.create_text(309.0, 0.0, anchor="nw", text="Condition", fill="#000000", font=("Inter Bold", 12 * -1))
canvas.create_text(390.0, 0.0, anchor="nw", text="Severity", fill="#000000", font=("Inter Bold", 12 * -1))
canvas.create_text(478.0, 0.0, anchor="nw", text="Admitted Date", fill="#000000", font=("Inter Bold", 12 * -1))
canvas.create_text(618.0, 0.0, anchor="nw", text="ID", fill="#000000", font=("Inter Bold", 12 * -1))
canvas.create_text(19.0, 185.0, anchor="nw", text="Name:", fill="#000000", font=("Inter Bold", 12 * -1))
canvas.create_text(19.0, 229.0, anchor="nw", text="Condition:", fill="#000000", font=("Inter Bold", 12 * -1))
canvas.create_text(19.0, 272.0, anchor="nw", text="Severity:", fill="#000000", font=("Inter Bold", 12 * -1))

# LIST #
columns = ("Name", "Condition", "Severity", "Date", "ID")
tree = ttk.Treeview(window, columns=columns, show="headings")
tree.column(0, width=150)
tree.column(1, width=75)
tree.column(2, width=75)
tree.column(3, width=150)
tree.column(4, width=50)
tree.place(x=150, y=20, width=500, height=380)

# TextBox / ENTRY #
entry_image_1 = PhotoImage(
    file=asset_file("entry_1.png"))
entry_bg_1 = canvas.create_image(75.5, 214.0,
                                 image=entry_image_1)
entry_1 = Entry(bd=0, bg="#EBEBEB", fg="#000716", highlightthickness=0)
entry_1.place(x=19.0, y=199.0, width=113.0, height=28.0)

entry_image_2 = PhotoImage(
    file=asset_file("entry_2.png"))
entry_bg_2 = canvas.create_image(75.5, 258.0, image=entry_image_2)
entry_2 = Entry(bd=0, bg="#EBEBEB", fg="#000716", highlightthickness=0)
entry_2.place(x=19.0, y=243.0, width=113.0, height=28.0)

entry_image_3 = PhotoImage(
    file=asset_file("entry_3.png"))
entry_bg_3 = canvas.create_image(75.5, 301.0, image=entry_image_3)
entry_3 = Entry(bd=0, bg="#EBEBEB", fg="#000716", highlightthickness=0)
entry_3.place(x=19.0, y=286.0, width=113.0, height=28.0)

# Add Button #
button_image_1 = PhotoImage(
    file=asset_file("button_1.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: add_patient(),  # Call Function
    relief="flat"
)
button_1.place(x=19.0, y=153.0, width=113.0, height=30.0)

button_image_hover_1 = PhotoImage(
    file=asset_file("button_hover_1.png"))


def button_1_hover(e):
    button_1.config(
        image=button_image_hover_1
    )


def button_1_leave(e):
    button_1.config(
        image=button_image_1
    )


button_1.bind('<Enter>', button_1_hover)
button_1.bind('<Leave>', button_1_leave)

# Update Button
button_image_2 = PhotoImage(
    file=asset_file("button_2.png"))
button_2 = Button(
    image=button_image_2,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: update_patient(),
    relief="flat"
)
button_2.place(x=19.0, y=111.0, width=113.0, height=30.0)

button_image_hover_2 = PhotoImage(
    file=asset_file("button_hover_2.png"))


def button_2_hover(e):
    button_2.config(
        image=button_image_hover_2
    )


def button_2_leave(e):
    button_2.config(
        image=button_image_2
    )


button_2.bind('<Enter>', button_2_hover)
button_2.bind('<Leave>', button_2_leave)

# Delete Button
button_image_3 = PhotoImage(
    file=asset_file("button_3.png"))
button_3 = Button(
    image=button_image_3,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: delete_patient(),
    relief="flat"
)
button_3.place(x=19.0, y=69.0, width=113.0, height=30.0)

button_image_hover_3 = PhotoImage(
    file=asset_file("button_hover_3.png"))


def button_3_hover(e):
    button_3.config(
        image=button_image_hover_3
    )


def button_3_leave(e):
    button_3.config(
        image=button_image_3
    )


button_3.bind('<Enter>', button_3_hover)
button_3.bind('<Leave>', button_3_leave)

# Continue Button
button_image_4 = PhotoImage(
    file=asset_file("button_4.png"))
button_4 = Button(
    image=button_image_4,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: continue_patient(),
    relief="flat"
)
button_4.place(x=19.0, y=27.0, width=113.0, height=30.0)

button_image_hover_4 = PhotoImage(
    file=asset_file("button_hover_4.png"))


def button_4_hover(e):
    button_4.config(
        image=button_image_hover_4
    )


def button_4_leave(e):
    button_4.config(
        image=button_image_4
    )


button_4.bind('<Enter>', button_4_hover)
button_4.bind('<Leave>', button_4_leave)

# Exit Button
button_image_5 = PhotoImage(
    file=asset_file("button_5.png"))
button_5 = Button(
    image=button_image_5,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: window.destroy(),  # Close
    relief="flat"
)
button_5.place(x=42.0, y=356.0, width=66.0, height=20.0)

show_data()
if __name__ == "__main__":
    window.mainloop()
