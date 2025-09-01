import tkinter as tk

def add_item():
    item = entry.get()
    if item:  # Only add if the entry is not empty
        listbox.insert(tk.END, item)  # Add item to the end of the list
        entry.delete(0, tk.END)  # Clear the entry field

def delete_item():
    selected_item_index = listbox.curselection()  # Get the selected item index
    if selected_item_index:
        listbox.delete(selected_item_index)  # Delete the selected item

# Create the main window
window = tk.Tk()
window.title("Simple List GUI")

# Entry field for adding items
entry = tk.Entry(window)
entry.pack(pady=10)

# Button to add items
add_button = tk.Button(window, text="Add Item", command=add_item)
add_button.pack(pady=5)

# Listbox to display items
listbox = tk.Listbox(window)
listbox.pack(pady=10)

# Button to delete selected items
delete_button = tk.Button(window, text="Delete Selected", command=delete_item)
delete_button.pack(pady=5)

# Run the main loop
window.mainloop()
