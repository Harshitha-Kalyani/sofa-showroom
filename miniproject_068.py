import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector


mydb = {
    "host": "localhost",        
    "user": "root",     
    "password": "root", 
    "database": "hardb"  
}


def initialize_database():
    conn = mysql.connector.connect(
        host=mydb["host"],
        user=mydb["user"],
        password=mydb["password"]
    )
    cursor = conn.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS hardb")
    conn.close()

    conn = mysql.connector.connect(**mydb)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sofa_items (
            sofa_id INT AUTO_INCREMENT PRIMARY KEY,
            sofa_name VARCHAR(255) NOT NULL,
            sofa_category VARCHAR(255) NOT NULL,
            sofa_price DECIMAL(10,2) NOT NULL,
            sofa_quantity INT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

initialize_database()


def get_connection():
    return mysql.connector.connect(**mydb)


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
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO sofa_items (sofa_name, sofa_category, sofa_price, sofa_quantity)
            VALUES (%s, %s, %s, %s)""",
            (name, category, price, quantity))
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Sofa added successfully!")
        display_sofas()
    except ValueError:
        messagebox.showerror("Error", "Price must be a number and Quantity must be an integer")


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
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE sofa_items 
            SET sofa_name=%s, sofa_category=%s, sofa_price=%s, sofa_quantity=%s
            WHERE sofa_id=%s""",
            (name, category, price, quantity, sofa_id))
        conn.commit()
        conn.close()
        display_sofas()
        messagebox.showinfo("Success", "Sofa updated successfully!")
    except ValueError:
        messagebox.showerror("Error", "Price must be a number and Quantity must be an integer")


def display_sofas():
    
    sofa_table.delete(*sofa_table.get_children())
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM sofa_items")
    items = cursor.fetchall()
    for item in items:
        sofa_table.insert("", tk.END, values=item)
    conn.close()
    calculate_total_price()
   

def remove_sofa():
    selected_item = sofa_table.selection()
    if not selected_item:
        messagebox.showerror("Error", "Select a sofa to delete")
        return

    sofa_id = sofa_table.item(selected_item, "values")[0]
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM sofa_items WHERE sofa_id = %s", (sofa_id,))
    conn.commit()
    conn.close()
    display_sofas()
    messagebox.showinfo("Success", "Sofa removed!")


def calculate_total_price():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT SUM(sofa_price * sofa_quantity) FROM sofa_items")
    total = cursor.fetchone()[0]
    conn.close()
    total_label.config(text=f"Total Price: Rs.{total:.2f}" if total else "Total Price: RS.0.00")


root = tk.Tk()
root.title("Sofa Showroom Management System")
root.geometry("600x500")
root.configure(bg="lavender")


input_frame = tk.Frame(root, bg="lavender")
input_frame.pack(pady=15, padx=20, fill=tk.X)

def create_label_entry(frame, text):
    tk.Label(frame, text=text, font=("Arial", 12), bg="white").pack(anchor="w", padx=10, pady=2)
    entry = tk.Entry(frame, font=("Arial", 12))
    entry.pack(padx=10, pady=2, fill=tk.X)
    return entry

name_entry = create_label_entry(input_frame, "Sofa Name:")
category_entry = create_label_entry(input_frame, "Category:")
price_entry = create_label_entry(input_frame, "Price:")
quantity_entry = create_label_entry(input_frame, "Quantity:")


button_frame = tk.Frame(root, bg="gray")
button_frame.pack(pady=10)

tk.Button(button_frame, text="Add Sofa", font=("Arial", 12), bg="lavender", fg="white", command=add_sofa).pack(padx=10, pady=5, fill=tk.X)
tk.Button(button_frame, text="Update Sofa", font=("Arial", 12), bg="red", fg="white", command=update_sofa).pack(padx=10, pady=5, fill=tk.X)
tk.Button(button_frame, text="Remove Sofa", font=("Arial", 12), bg="blue", fg="white", command=remove_sofa).pack(padx=10, pady=5, fill=tk.X)


total_label = tk.Label(root, text="Total Price: RS.0.00", font=("Arial", 14), bg="blue", fg="black")
total_label.pack(pady=10)


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
