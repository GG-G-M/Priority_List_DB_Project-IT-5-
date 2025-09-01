import tkinter as tk


def add_item():
    # Get values from all three entries
    item1 = entry_1.get()
    item2 = entry_2.get()
    item3 = entry_3.get()

    # Combine the items into a single string
    if item1 or item2 or item3:  # Only add if at least one entry is not empty
        combined_item = f"{item1}, {item2}, {item3}"  # Combine the entries
        listbox.insert(tk.END, combined_item)  # Add to the end of the list
        entry_1.delete(0, tk.END)  # Clear the first entry field
        entry_2.delete(0, tk.END)  # Clear the second entry field
        entry_3.delete(0, tk.END)  # Clear the third entry field


def delete_item():
    selected_item_index = listbox.curselection()  # Get the selected item index
    if selected_item_index:
        listbox.delete(selected_item_index)  # Delete the selected item


# Create the main window
window = tk.Tk()
window.title("Simple List GUI")

# Entry fields for adding items
entry_1 = tk.Entry(window)
entry_1.pack(pady=5)

entry_2 = tk.Entry(window)
entry_2.pack(pady=5)

entry_3 = tk.Entry(window)
entry_3.pack(pady=5)

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
