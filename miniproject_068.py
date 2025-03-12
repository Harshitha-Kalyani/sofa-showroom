import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

# Database Initialization
def initialize_database():
    conn = sqlite3.connect("sofa_showroom.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sofa_items (
            sofa_id INTEGER PRIMARY KEY AUTOINCREMENT,
            sofa_name TEXT NOT NULL,
            sofa_category TEXT NOT NULL,
            sofa_price REAL NOT NULL,
            sofa_quantity INTEGER NOT NULL
        )
    """)
    conn.commit()
    conn.close()

initialize_database()

# Function to Add Sofa Item
def add_sofa():
    name = name_entry.get()
    category = category_entry.get()
    price = price_entry.get()
    quantity = quantity_entry.get()

    if not (name and category and price and quantity):
        messagebox.showerror("Error", "All fields must be filled")
        return

    try:
        price = float(price)
        quantity = int(quantity)
        conn = sqlite3.connect("sofa_showroom.db")
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO sofa_items (sofa_name, sofa_category, sofa_price, sofa_quantity)
            VALUES (?, ?, ?, ?)""",
            (name, category, price, quantity))
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Sofa added successfully!")
        display_sofas()
    except ValueError:
        messagebox.showerror("Error", "Price must be a number and Quantity must be an integer")

# Function to Update Sofa Item
def update_sofa():
    selected_item = sofa_table.selection()
    if not selected_item:
        messagebox.showerror("Error", "Select a sofa to update")
        return

    sofa_id = sofa_table.item(selected_item, "values")[0]
    name = name_entry.get()
    category = category_entry.get()
    price = price_entry.get()
    quantity = quantity_entry.get()

    if not (name and category and price and quantity):
        messagebox.showerror("Error", "All fields must be filled")
        return

    try:
        price = float(price)
        quantity = int(quantity)
        conn = sqlite3.connect("sofa_showroom.db")
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE sofa_items 
            SET sofa_name=?, sofa_category=?, sofa_price=?, sofa_quantity=? 
            WHERE sofa_id=?""",
            (name, category, price, quantity, sofa_id))
        conn.commit()
        conn.close()
        display_sofas()
        messagebox.showinfo("Success", "Sofa updated successfully!")
    except ValueError:
        messagebox.showerror("Error", "Price must be a number and Quantity must be an integer")

# Function to Display Sofa Items
def display_sofas():
    sofa_table.delete(*sofa_table.get_children())
    conn = sqlite3.connect("sofa_showroom.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM sofa_items")
    items = cursor.fetchall()
    for item in items:
        sofa_table.insert("", tk.END, values=item)
    conn.close()
    calculate_total_price()

# Function to Remove Selected Sofa Item
def remove_sofa():
    selected_item = sofa_table.selection()
    if not selected_item:
        messagebox.showerror("Error", "Select a sofa to delete")
        return

    sofa_id = sofa_table.item(selected_item, "values")[0]
    conn = sqlite3.connect("sofa_showroom.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM sofa_items WHERE sofa_id = ?", (sofa_id,))
    conn.commit()
    conn.close()
    display_sofas()
    messagebox.showinfo("Success", "Sofa removed!")

# Function to Calculate Total Price
def calculate_total_price():
    conn = sqlite3.connect("sofa_showroom.db")
    cursor = conn.cursor()
    cursor.execute("SELECT SUM(sofa_price * sofa_quantity) FROM sofa_items")
    total = cursor.fetchone()[0]
    conn.close()
    total_label.config(text=f"Total Price: ${total:.2f}" if total else "Total Price: $0.00")

# GUI Setup
root = tk.Tk()
root.title("Sofa Showroom Management System")
root.geometry("600x500")
root.configure(bg="#E8DAEF")

# Frame for Input Fields
input_frame = tk.Frame(root, bg="#D2B4DE")
input_frame.pack(pady=15, padx=20, fill=tk.X)

def create_label_entry(frame, text):
    tk.Label(frame, text=text, font=("Arial", 12), bg="#D2B4DE").pack(anchor="w", padx=10, pady=2)
    entry = tk.Entry(frame, font=("Arial", 12))
    entry.pack(padx=10, pady=2, fill=tk.X)
    return entry

name_entry = create_label_entry(input_frame, "Sofa Name:")
category_entry = create_label_entry(input_frame, "Category:")
price_entry = create_label_entry(input_frame, "Price:")
quantity_entry = create_label_entry(input_frame, "Quantity:")

# Buttons
button_frame = tk.Frame(root, bg="#E8DAEF")
button_frame.pack(pady=10)

tk.Button(button_frame, text="Add Sofa", font=("Arial", 12), bg="#27AE60", fg="white", command=add_sofa).pack(padx=10, pady=5, fill=tk.X)
tk.Button(button_frame, text="Update Sofa", font=("Arial", 12), bg="#2980B9", fg="white", command=update_sofa).pack(padx=10, pady=5, fill=tk.X)
tk.Button(button_frame, text="Remove Sofa", font=("Arial", 12), bg="#C0392B", fg="white", command=remove_sofa).pack(padx=10, pady=5, fill=tk.X)

# Total Price Label
total_label = tk.Label(root, text="Total Price: $0.00", font=("Arial", 14), bg="#E8DAEF", fg="black")
total_label.pack(pady=10)

# Sofa List Table
table_frame = tk.Frame(root)
table_frame.pack(pady=15, fill=tk.BOTH, expand=True)

columns = ("ID", "Name", "Category", "Price", "Quantity")
sofa_table = ttk.Treeview(table_frame, columns=columns, show="headings")

for col in columns:
    sofa_table.heading(col, text=col)
    sofa_table.column(col, width=100)

sofa_table.pack(fill=tk.BOTH, expand=True)
display_sofas()

root.mainloop()

