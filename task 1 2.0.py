import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import os

# Check if database file exists; if so, delete it to avoid schema conflicts
if os.path.exists('music_store_management.db'):
    os.remove('music_store_management.db')

# Connect to SQLite Database
conn = sqlite3.connect('music_store_management.db')
cursor = conn.cursor()

# Create tables for products, customers, orders, and inventory
cursor.execute(''' 
    CREATE TABLE IF NOT EXISTS products (
        product_id INTEGER PRIMARY KEY AUTOINCREMENT,
        product_name TEXT,
        category TEXT,
        price REAL,
        description TEXT
    )
''')
cursor.execute(''' 
    CREATE TABLE IF NOT EXISTS customers (
        customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        email TEXT,
        phone TEXT
    )
''')
cursor.execute(''' 
    CREATE TABLE IF NOT EXISTS orders (
        order_id INTEGER PRIMARY KEY AUTOINCREMENT,
        customer_id INTEGER,
        order_date TEXT,
        total_price REAL,
        status TEXT,
        FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
    )
''')
cursor.execute(''' 
    CREATE TABLE IF NOT EXISTS inventory (
        inventory_id INTEGER PRIMARY KEY AUTOINCREMENT,
        product_id INTEGER,
        quantity INTEGER,
        FOREIGN KEY (product_id) REFERENCES products(product_id)
    )
''')
cursor.execute(''' 
    CREATE TABLE IF NOT EXISTS suppliers (
        supplier_id INTEGER PRIMARY KEY AUTOINCREMENT,
        supplier_name TEXT,
        contact_info TEXT
    )
''')

# Create indexes on frequently queried fields (e.g., product_name and category)
cursor.execute("CREATE INDEX IF NOT EXISTS idx_product_name ON products (product_name)")
cursor.execute("CREATE INDEX IF NOT EXISTS idx_category ON products (category)")
conn.commit()

class MusicStoreManagementSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Music Store Management System")
        self.root.geometry("1200x700")
        self.root.config(bg="black")  # Set the background to black

        self.create_widgets()

        self.tree_frame = tk.Frame(self.root, bg="black")
        self.tree_frame.grid(row=6, column=0, columnspan=4, padx=10, pady=10)
        
        self.columns = ("product_id", "product_name", "category", "price", "description")
        self.tree = ttk.Treeview(self.tree_frame, columns=self.columns, show="headings")
        for col in self.columns:
            self.tree.heading(col, text=col.replace("_", " ").capitalize())
            self.tree.column(col, anchor="center", width=120)
        self.tree.grid(row=0, column=0, columnspan=4, padx=10, pady=10)
        
        self.load_data()

    def create_widgets(self):
        """Create Entry widgets for Product and Order details"""
        labels = ["Product ID", "Product Name", "Category", "Price", "Description"]
        self.entries = {}

        entry_frame = tk.Frame(self.root, bg="black")
        entry_frame.grid(row=0, column=0, padx=10, pady=5)

        for idx, label in enumerate(labels):
            tk.Label(entry_frame, text=label, bg="black", fg="white", font=("Arial", 12)).grid(row=idx, column=0, padx=10, pady=5)
            entry = tk.Entry(entry_frame, font=("Arial", 12))
            entry.grid(row=idx, column=1, padx=10, pady=5)
            self.entries[label] = entry

        self.add_buttons()

    def add_buttons(self):
        """Add buttons for adding, updating, deleting, and searching products"""
        button_frame = tk.Frame(self.root, bg="black")
        button_frame.grid(row=5, column=0, columnspan=4, padx=10, pady=10)

        # Add Buttons
        tk.Button(button_frame, text="Add Product", bg="#4CAF50", fg="white", command=self.add_product, width=20, height=2, font=("Arial", 12)).grid(row=0, column=0, padx=10)
        tk.Button(button_frame, text="Update Product", bg="#FF9800", fg="white", command=self.update_product, width=20, height=2, font=("Arial", 12)).grid(row=0, column=1, padx=10)
        tk.Button(button_frame, text="Delete Product", bg="#F44336", fg="white", command=self.delete_product, width=20, height=2, font=("Arial", 12)).grid(row=0, column=2, padx=10)
        tk.Button(button_frame, text="Search Product", bg="#2196F3", fg="white", command=self.search_product, width=20, height=2, font=("Arial", 12)).grid(row=0, column=3, padx=10)

    def load_data(self, limit=50):
        """Load product data from the database to the table with a limit for efficiency"""
        for row in self.tree.get_children():
            self.tree.delete(row)

        # Limit the number of rows loaded to improve performance
        cursor.execute("SELECT * FROM products LIMIT ?", (limit,))
        rows = cursor.fetchall()
        for row in rows:
            self.tree.insert("", tk.END, values=row)

    def add_product(self):
        """Add a new product to the database"""
        try:
            product_name = self.entries["Product Name"].get()
            category = self.entries["Category"].get()
            price = float(self.entries["Price"].get())
            description = self.entries["Description"].get()

            cursor.execute(''' 
                INSERT INTO products (product_name, category, price, description)
                VALUES (?, ?, ?, ?)
            ''', (product_name, category, price, description))
            conn.commit()
            self.clear_entries()
            self.load_data()
            messagebox.showinfo("Success", "Product added successfully")
        except ValueError as e:
            messagebox.showerror("Error", f"Invalid input: {e}")

    def update_product(self):
        """Update an existing product's details in the database"""
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Selection Error", "Select a product to update")
            return

        product_id = self.tree.item(selected_item)['values'][0]
        product_name = self.entries["Product Name"].get()
        category = self.entries["Category"].get()
        price = float(self.entries["Price"].get())
        description = self.entries["Description"].get()

        cursor.execute(''' 
            UPDATE products 
            SET product_name=?, category=?, price=?, description=? 
            WHERE product_id=?
        ''', (product_name, category, price, description, product_id))
        conn.commit()
        self.clear_entries()
        self.load_data()
        messagebox.showinfo("Success", "Product updated successfully")

    def delete_product(self):
        """Delete a selected product from the database"""
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Selection Error", "Select a product to delete")
            return

        product_id = self.tree.item(selected_item)['values'][0]
        cursor.execute("DELETE FROM products WHERE product_id=?", (product_id,))
        conn.commit()
        self.load_data()
        messagebox.showinfo("Success", "Product deleted successfully")

    def search_product(self):
        """Search products by Name or Category"""
        product_name = self.entries["Product Name"].get()
        category = self.entries["Category"].get()

        if not product_name and not category:
            messagebox.showwarning("Search Error", "Enter Product Name or Category to search")
            return

        for row in self.tree.get_children():
            self.tree.delete(row)

        query = "SELECT * FROM products WHERE 1=1"
        params = []

        if product_name:
            query += " AND product_name LIKE ?"
            params.append('%' + product_name + '%')
        if category:
            query += " AND category LIKE ?"
            params.append('%' + category + '%')

        cursor.execute(query, tuple(params))
        rows = cursor.fetchall()

        if rows:
            for row in rows:
                self.tree.insert("", tk.END, values=row)
            messagebox.showinfo("Search Result", f"Found {len(rows)} matching product(s).")
        else:
            messagebox.showinfo("No Results", "No products found for the given criteria.")

    def clear_entries(self):
        """Clear all the entry fields after an operation"""
        for entry in self.entries.values():
            entry.delete(0, tk.END)

root = tk.Tk()
app = MusicStoreManagementSystem(root)
root.mainloop()
