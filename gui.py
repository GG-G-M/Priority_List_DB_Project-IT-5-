import tkinter
import datetime
from pathlib import Path
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage

ASSETS_PATH = Path(r"C:\Users\PC\Desktop\build\assets\frame0")


# Functions
def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


def add_item():
    # Get values from all three entries
    item1 = entry_1.get()
    item2 = entry_2.get()
    item3 = entry_3.get()
    item4 = datetime.date.today()

    # Combine the items into a single string
    if item1 or item2 or item3:  # Only add if at least one entry is not empty
        combined_item = f"{item1},     {item2},      {item3},      {item4}"  # Combine the entries
        listbox.insert(tkinter.END, combined_item)  # Add to the end of the list
        entry_1.delete(0, tkinter.END)  # Clear the first entry field
        entry_2.delete(0, tkinter.END)  # Clear the second entry field
        entry_3.delete(0, tkinter.END)  # Clear the third entry field



def delete_item():
    selected_item_index = listbox.curselection()  # Get the selected item index
    if selected_item_index:
        listbox.delete(selected_item_index)  # Delete the selected item


window = Tk()
window.geometry("600x400")
window.configure(bg="#FFFFFF")

canvas = Canvas(
    window,
    bg="#FFFFFF",
    height=400,
    width=600,
    bd=0,
    highlightthickness=0,
    relief="ridge"
)

canvas.place(x=0, y=0)
canvas.create_rectangle(0.0, 0.0, 150.0, 400.0, fill="#FFFFFF", outline="")

canvas.create_rectangle(150.0, 0.0, 600.0, 400.0, fill="#81FF75", outline="")

image_image_1 = PhotoImage(
    file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(75.0, 366.0,
                              image=image_image_1)

###RECTANGLE###
canvas.create_rectangle(300.0, 0.0, 375.0, 400.0, fill="#FF7272", outline="")
canvas.create_rectangle(450.0, 0.0, 600.0, 400.0, fill="#00C2FF", outline="")

###LABEL###
canvas.create_text(19.0, 0.0, anchor="nw", text="Patient Priority List", fill="#000000", font=("Inter Bold", 12 * -1))
canvas.create_text(208.0, 0.0, anchor="nw", text="Name", fill="#000000", font=("Inter Bold", 12 * -1))
canvas.create_text(309.0, 0.0, anchor="nw", text="Condition", fill="#000000", font=("Inter Bold", 12 * -1))
canvas.create_text(390.0, 0.0, anchor="nw", text="Severity", fill="#000000", font=("Inter Bold", 12 * -1))
canvas.create_text(478.0, 0.0, anchor="nw", text="Admitted Date", fill="#000000", font=("Inter Bold", 12 * -1))
canvas.create_text(19.0, 185.0, anchor="nw", text="Name:", fill="#000000", font=("Inter Bold", 12 * -1))
canvas.create_text(19.0, 229.0, anchor="nw", text="Condition:", fill="#000000", font=("Inter Bold", 12 * -1))
canvas.create_text(19.0, 272.0, anchor="nw", text="Severity:", fill="#000000", font=("Inter Bold", 12 * -1))

###LIST###
listbox = tkinter.Listbox(window)
listbox.place(x=150, y=20, width=450, height=380)

###TextBox / ENTRY ###
entry_image_1 = PhotoImage(
    file=relative_to_assets("entry_1.png"))
entry_bg_1 = canvas.create_image(75.5, 214.0,
                                 image=entry_image_1)
entry_1 = Entry(bd=0, bg="#EBEBEB", fg="#000716", highlightthickness=0)
entry_1.place(x=19.0, y=199.0, width=113.0, height=28.0)

entry_image_2 = PhotoImage(
    file=relative_to_assets("entry_2.png"))
entry_bg_2 = canvas.create_image(75.5, 258.0, image=entry_image_2)
entry_2 = Entry(bd=0, bg="#EBEBEB", fg="#000716", highlightthickness=0)
entry_2.place(x=19.0, y=243.0, width=113.0, height=28.0)

entry_image_3 = PhotoImage(
    file=relative_to_assets("entry_3.png"))
entry_bg_3 = canvas.create_image(75.5, 301.0, image=entry_image_3)
entry_3 = Entry(bd=0, bg="#EBEBEB", fg="#000716", highlightthickness=0)
entry_3.place(x=19.0, y=286.0, width=113.0, height=28.0)

###Button###
button_image_1 = PhotoImage(
    file=relative_to_assets("button_1.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: add_item(),
    relief="flat"
)
button_1.place(x=19.0, y=153.0, width=113.0, height=30.0)

button_image_hover_1 = PhotoImage(
    file=relative_to_assets("button_hover_1.png"))


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

button_image_2 = PhotoImage(
    file=relative_to_assets("button_2.png"))
button_2 = Button(
    image=button_image_2,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("Button2"),
    relief="flat"
)
button_2.place(x=19.0, y=111.0, width=113.0, height=30.0)

button_image_hover_2 = PhotoImage(
    file=relative_to_assets("button_hover_2.png"))


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

button_image_3 = PhotoImage(
    file=relative_to_assets("button_3.png"))
button_3 = Button(
    image=button_image_3,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: delete_item(),
    relief="flat"
)
button_3.place(x=19.0, y=69.0, width=113.0, height=30.0)

button_image_hover_3 = PhotoImage(
    file=relative_to_assets("button_hover_3.png"))


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

button_image_4 = PhotoImage(
    file=relative_to_assets("button_4.png"))
button_4 = Button(
    image=button_image_4,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_4 clicked"),
    relief="flat"
)
button_4.place(x=19.0, y=27.0, width=113.0, height=30.0)

button_image_hover_4 = PhotoImage(
    file=relative_to_assets("button_hover_4.png"))


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
    file=relative_to_assets("button_5.png"))
button_5 = Button(
    image=button_image_5,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: window.destroy(),  # Close
    relief="flat"
)
button_5.place(x=42.0, y=356.0, width=66.0, height=20.0)

window.resizable(False, False)
window.mainloop()
