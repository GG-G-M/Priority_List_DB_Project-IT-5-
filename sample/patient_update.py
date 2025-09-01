from main import connect_db, update_db, show_data, messagebox
from center_window import center

class update_gui:
    def __init__(self, window, tree ):
        print("yes")
        selected_item = tree.selection()
        if selected_item:
            item = tree.item(selected_item)
            patient_id, name, condition, severity = item['values']

            # Open a new window to update data
            update_window = window.Toplevel(window)
            update_window.title("Update Patient")
            center(update_window, 400, 250)

            # Labels and Entry Fields for update
            window.Label(update_window, text="Name:").grid(row=0, column=0, padx=10, pady=10, sticky='e')
            update_name_entry = window.Entry(update_window)
            update_name_entry.grid(row=0, column=1, padx=10, pady=10)
            update_name_entry.insert(0, name)

            window.Label(update_window, text="Condition:").grid(row=1, column=0, padx=10, pady=10, sticky='e')
            update_condition_entry = window.Entry(update_window)
            update_condition_entry.grid(row=1, column=1, padx=10, pady=10)
            update_condition_entry.insert(0, condition)

            window.Label(update_window, text="Severity (1-10):").grid(row=2, column=0, padx=10, pady=10, sticky='e')
            update_severity_entry = window.Entry(update_window)
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
                        if not (1 <= new_severity <= 5):
                            raise ValueError("Severity must be between 1 and 10.")
                        conn = connect_db()
                        cursor = conn.cursor()
                        cursor.execute("""
                            UPDATE patients 
                            SET name = ?, condition = ?, severity = ?
                            WHERE id = ?
                        """, (new_name, new_condition, new_severity, patient_id))
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
            save_button = window.Button(update_window, text="Save", command=save_updates)
            save_button.grid(row=3, column=0, columnspan=2, pady=20)
        else:
            messagebox.showwarning("Selection Error", "Please select a patient to update.")