import tkinter as tk
from tkinter import ttk, messagebox

app = tk.Tk()
app.title("Contact Management System")
app.geometry("500x400")

tk.Label(app, text="Name").grid(row=0, column=0, padx=10, pady=5)
entry_name = tk.Entry(app)
entry_name.grid(row=0, column=1, padx=10, pady=5)

tk.Label(app, text="Phone").grid(row=1, column=0, padx=10, pady=5)
entry_phone = tk.Entry(app)
entry_phone.grid(row=1, column=1, padx=10, pady=5)

tk.Label(app, text="Email").grid(row=2, column=0, padx=10, pady=5)
entry_email = tk.Entry(app)
entry_email.grid(row=2, column=1, padx=10, pady=5)

tree = ttk.Treeview(app, columns=("Name", "Phone", "Email"), show="headings")
tree.heading("Name", text="Name")
tree.heading("Phone", text="Phone")
tree.heading("Email", text="Email")
tree.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

tk.Button(app, text="Add Contact", command=lambda: add_contact()).grid(row=4, column=0, padx=10, pady=10)
tk.Button(app, text="Delete Contact", command=lambda: delete_contact()).grid(row=4, column=1, padx=10, pady=10)

def add_contact():
    name = entry_name.get()
    phone = entry_phone.get()
    email = entry_email.get()
    
    if name and phone and email:
        tree.insert("", "end", values=(name, phone, email))
        entry_name.delete(0, tk.END)
        entry_phone.delete(0, tk.END)
        entry_email.delete(0, tk.END)
    else:
        messagebox.showwarning("Input Error", "All fields are required!")

def delete_contact():
    selected_item = tree.selection()
    if selected_item:
        for item in selected_item:
            tree.delete(item)
    else:
        messagebox.showwarning("Selection Error", "No contact selected!")

def edit_contact():
    selected_item = tree.selection()
    if selected_item:
        item = selected_item[0]
        name, phone, email = tree.item(item, "values")
        entry_name.delete(0, tk.END)
        entry_phone.delete(0, tk.END)
        entry_email.delete(0, tk.END)
        entry_name.insert(0, name)
        entry_phone.insert(0, phone)
        entry_email.insert(0, email)

        def save_changes():
            new_name = entry_name.get()
            new_phone = entry_phone.get()
            new_email = entry_email.get()
            tree.item(item, values=(new_name, new_phone, new_email))
            edit_window.destroy()

        edit_window = tk.Toplevel(app)
        edit_window.title("Edit Contact")
        tk.Button(edit_window, text="Save Changes", command=save_changes).pack()
    else:
        messagebox.showwarning("Selection Error", "No contact selected!")

def save_to_file():
    with open("contacts.csv", "w") as file:
        for row in tree.get_children():
            values = tree.item(row, "values")
            file.write(",".join(values) + "\n")

def load_from_file():
    try:
        with open("contacts.csv", "r") as file:
            for line in file:
                name, phone, email = line.strip().split(",")
                tree.insert("", "end", values=(name, phone, email))
    except FileNotFoundError:
        pass

load_from_file()

app.mainloop()
