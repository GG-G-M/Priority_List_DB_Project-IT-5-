import tkinter as tk
from tkinter import messagebox

def new_file():
    messagebox.showinfo("New File", "Create a new file.")

def open_file():
    messagebox.showinfo("Open File", "Open an existing file.")

def save_file():
    messagebox.showinfo("Save File", "Save the current file.")

def exit_app():
    root.quit()

# Create the main window
root = tk.Tk()
root.title("Dropdown Menu Example")
root.geometry("400x300")

# Create a menu bar
menu_bar = tk.Menu(root)

# Create a File menu
file_menu = tk.Menu(menu_bar, tearoff=0)
file_menu.add_command(label="New", command=new_file)
file_menu.add_command(label="Open", command=open_file)
file_menu.add_command(label="Save", command=save_file)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=exit_app)

# Add the File menu to the menu bar
menu_bar.add_cascade(label="File", menu=file_menu)

# Display the menu bar in the window
root.config(menu=menu_bar)

# Run the application
root.mainloop()
