import customtkinter as ctk #gui library
import tkinter.messagebox as messagebox #to view errors but using tkinter bcz customtkinter doesn't have messagebox
import json #file where contacts will be saved
import os

# File to store contacts
CONTACTS_FILE = 'contacts.json'

# Load contacts from the file
def load_contacts():
    if os.path.exists(CONTACTS_FILE):
        with open(CONTACTS_FILE, 'r') as file:
            return json.load(file)
    return {}

# Save contacts to the file
def save_contacts(contacts):
    with open(CONTACTS_FILE, 'w') as file:
        json.dump(contacts, file)

# Add new contact
def add_contact():
    name = entry_name.get()
    phone = entry_phone.get()
    email = entry_email.get()

    if not name or not phone or not email:
        messagebox.showwarning("Input Error", "All fields are required.")
        return

    contacts[name] = {'phone': phone, 'email': email}
    save_contacts(contacts)
    update_contact_list()
    clear_entries()

# Update the contact list display
def update_contact_list():
    textbox_contacts.delete(1.0, ctk.END)
    for name, details in contacts.items():
        textbox_contacts.insert(ctk.END, f"Name: {name}, Phone: {details['phone']}, Email: {details['email']}\n")

# Clear entry fields
def clear_entries():
    entry_name.delete(0, ctk.END)
    entry_phone.delete(0, ctk.END)
    entry_email.delete(0, ctk.END)

# Edit selected contact
def edit_contact():
    selected = textbox_contacts.get("insert linestart", "insert lineend").strip()
    if not selected:
        messagebox.showwarning("Selection Error", "Select a contact to edit.")
        return

    # Extract name from the selected text
    name_part = selected.split(",")[0]  # Get the name part
    name = name_part.split(": ")[1]  # Extract the name

    entry_name.delete(0, ctk.END)
    entry_name.insert(0, name)
    entry_phone.delete(0, ctk.END)
    entry_phone.insert(0, contacts[name]['phone'])
    entry_email.delete(0, ctk.END)
    entry_email.insert(0, contacts[name]['email'])

# Delete selected contact
def delete_contact():
    selected = textbox_contacts.get("insert linestart", "insert lineend").strip()
    if not selected:
        messagebox.showwarning("Selection Error", "Select a contact to delete.")
        return

    name_part = selected.split(",")[0]  # Get the name part
    name = name_part.split(": ")[1]  # Extract the name

    del contacts[name]
    save_contacts(contacts)
    update_contact_list()
    clear_entries()

# Initialize the application
contacts = load_contacts()

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

root = ctk.CTk()
root.title("Contact Manager")
root.geometry("400x400")

frame = ctk.CTkFrame(root)
frame.pack(padx=10, pady=10, fill="both", expand=True)

# Entry fields
label_name = ctk.CTkLabel(frame, text="Name:")
label_name.grid(row=0, column=0, sticky="e", padx=5, pady=5)
entry_name = ctk.CTkEntry(frame)
entry_name.grid(row=0, column=1, padx=5, pady=5)

label_phone = ctk.CTkLabel(frame, text="Phone:")
label_phone.grid(row=1, column=0, sticky="e", padx=5, pady=5)
entry_phone = ctk.CTkEntry(frame)
entry_phone.grid(row=1, column=1, padx=5, pady=5)

label_email = ctk.CTkLabel(frame, text="Email:")
label_email.grid(row=2, column=0, sticky="e", padx=5, pady=5)
entry_email = ctk.CTkEntry(frame)
entry_email.grid(row=2, column=1, padx=5, pady=5)

# Buttons
button_add = ctk.CTkButton(frame, text="Add Contact", command=add_contact)
button_add.grid(row=3, columnspan=2, pady=(10, 5))

button_edit = ctk.CTkButton(frame, text="Edit Contact", command=edit_contact)
button_edit.grid(row=4, columnspan=2, pady=5)

button_delete = ctk.CTkButton(frame, text="Delete Contact", command=delete_contact)
button_delete.grid(row=5, columnspan=2, pady=5)

# Contact List
textbox_contacts = ctk.CTkTextbox(root, width=40, height=15)
textbox_contacts.pack(padx=10, pady=10, fill="both", expand=True)

update_contact_list()

root.mainloop()
