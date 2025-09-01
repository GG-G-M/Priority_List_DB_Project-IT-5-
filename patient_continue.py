import sqlite3
from tkinter import ttk, Toplevel
from center_window import center
from datetime import datetime


def connect_db(db):
    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    # Create table if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS patients (
            name TEXT NOT NULL,
            condition TEXT NOT NULL,
            severity INTEGER NOT NULL,
            date TEXT NOT NULL
        )
    ''')
    conn.commit()
    return conn

def update_db(db,instruction, rows):
    conn = connect_db(db)
    cursor = conn.cursor()
    cursor.execute(instruction, (rows))
    conn.commit()
    conn.close()

class discharged:
    def __init__(self, name, condition, severity):
        date = datetime.now().strftime("%d/%m/%Y | %H:/%M:/%S")
        connect_db("patient_discharged.db")
        update_db("patient_discharged.db", "INSERT INTO patients (name, condition, severity, date) VALUES (?, ?, ?, ?)",
                  (name, condition, severity, date))
        print("Discharge")


class dead:
    def __init__(self, name, condition, severity):
        date = datetime.now().strftime("%d/%m/%Y | %H:/%M:/%S")
        connect_db("patient_dead.db")
        update_db("patient_dead.db", "INSERT INTO patients (name, condition, severity, date) VALUES (?, ?, ?, ?)",
                  (name, condition, severity, date))
        print("Dead")

class view_data:
    def __init__(self, window, db):
        #make window
        update_window = Toplevel(window)
        update_window.title("Patient List")
        center(update_window, 420, 250)
        update_window.resizable(False, False)

        columns = ("Name", "Condition", "Severity", "Date")
        tree = ttk.Treeview(update_window, columns=columns, show="headings")
        for x in columns:
            tree.heading(x, text=x)  # Add column headings
            tree.column(x, width=100)  # Set column widths
        tree.column(1, width=50)
        tree.column(2, width=30)
        tree.place(x=10, y=10, width=410, height=240)

        #Show Tree
        for item in tree.get_children():
            tree.delete(item)
        order = 'DESC'
        conn = connect_db(db)
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM patients ORDER BY date {order}")
        rows = cursor.fetchall()
        conn.close()

        for row in rows:
            tree.insert('', 'end', values=row)