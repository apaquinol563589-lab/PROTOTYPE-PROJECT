import tkinter as tk
from tkinter import ttk, messagebox

class InventoryView:

    def __init__(self, root, service):

        self.root = root
        self.service = service

        self.selected_index = None

        self.root.title("Personal Inventory System")
        self.root.geometry("1000x700")
        self.root.resizable(False, False)

        self.create_main_window()

        self.refresh_categories()
        self.refresh_table()

    # MAIN WINDOW

    def create_main_window(self):

        title = tk.Label(
            self.root,
            text="PERSONAL INVENTORY SYSTEM",
            font=("Arial", 22, "bold")
        )

        title.pack(pady=15)

        # INPUT FRAME

        input_frame = tk.LabelFrame(
            self.root,
            text="Item Information",
            padx=15,
            pady=15
        )

        input_frame.pack(
            fill="x",
            padx=20,
            pady=10
        )

        # Item name
        tk.Label(
            input_frame,
            text="Item Name:"
        ).grid(
            row=0,
            column=0,
            padx=5,
            pady=5
        )

        self.name_entry = tk.Entry(
            input_frame,
            width=25
        )

        self.name_entry.grid(
            row=0, column=1, padx=5, pady=5
        )

        # Quantity
        tk.Label(
            input_frame, text="Quantity:"
        ).grid(
            row=0, column=2, padx=5, pady=5
        )

        self.quantity_entry = tk.Entry(
            input_frame,
            width=15
        )

        self.quantity_entry.grid(
            row=0, column=3, padx=5, pady=5
        )

        # Price
        tk.Label(
            input_frame,
            text="Price:"
        ).grid(
            row=0,
            column=4,
            padx=5,
            pady=5
        )

        self.price_entry = tk.Entry(
            input_frame,
            width=15
        )

        self.price_entry.grid(
            row=0,
            column=5,
            padx=5,
            pady=5
        )

        # Category
        tk.Label(
            input_frame,
            text="Category:"
        ).grid(
            row=1,
            column=0,
            padx=5,
            pady=5
        )

        self.category_combo = ttk.Combobox(
            input_frame,
            width=22,
            state="readonly"
        )

        self.category_combo.grid(
            row=1,
            column=1,
            padx=5,
            pady=5
        )

        # BUTTON FRAME

        button_frame = tk.Frame(self.root)

        button_frame.pack(pady=10)

        tk.Button(
            button_frame,
            text="Add Item",
            width=15,
            command=self.add_item
        ).grid(
            row=0,
            column=0,
            padx=5
        )

        tk.Button(
            button_frame,
            text="Update Item",
            width=15,
            command=self.update_item
        ).grid(
            row=0,
            column=1,
            padx=5
        )

        tk.Button(
            button_frame,
            text="Delete Item",
            width=15,
            command=self.delete_item
        ).grid(
            row=0,
            column=2,
            padx=5
        )

        tk.Button(
            button_frame,
            text="Clear",
            width=15,
            command=self.clear_fields
        ).grid(
            row=0,
            column=3,
            padx=5
        )

        tk.Button(
            button_frame,
            text="Manage Categories",
            width=18,
            command=self.open_category_manager
        ).grid(
            row=0,
            column=4,
            padx=5
        )

        tk.Button(
            button_frame,
            text="Category Viewer",
            width=18,
            command=self.open_category_viewer
        ).grid(
            row=0,
            column=5,
            padx=5
        )

        # TABLE

        table_frame = tk.Frame(self.root)

        table_frame.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=10
        )

        columns = (
            "number",
            "name",
            "category",
            "quantity",
            "price",
            "total"
        )

        self.tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            height=18
        )

        self.tree.heading(
            "number",
            text="#"
        )

        self.tree.heading(
            "name",
            text="Item Name"
        )

        self.tree.heading(
            "category",
            text="Category"
        )

        self.tree.heading(
            "quantity",
            text="Quantity"
        )

        self.tree.heading(
            "price",
            text="Price"
        )

        self.tree.heading(
            "total",
            text="Total Value"
        )

        self.tree.column(
            "number",
            width=50,
            anchor="center"
        )

        self.tree.column(
            "name",
            width=220
        )

        self.tree.column(
            "category",
            width=150
        )

        self.tree.column(
            "quantity",
            width=100,
            anchor="center"
        )

        self.tree.column(
            "price",
            width=120,
            anchor="center"
        )

        self.tree.column(
            "total",
            width=150,
            anchor="center"
        )

        scrollbar = ttk.Scrollbar(
            table_frame,
            orient="vertical",
            command=self.tree.yview
        )

        self.tree.configure(
            yscrollcommand=scrollbar.set
        )

        self.tree.pack(
            side="left",
            fill="both",
            expand=True
        )

        scrollbar.pack(
            side="right",
            fill="y"
        )

        self.tree.bind(
            "<<TreeviewSelect>>",
            self.select_item
        )

        # TOTALS

        totals_frame = tk.Frame(self.root)

        totals_frame.pack(
            fill="x",
            padx=20,
            pady=10
        )

        self.quantity_label = tk.Label(
            totals_frame,
            text="Total Quantity: 0",
            font=("Arial", 12, "bold")
        )

        self.quantity_label.pack(
            side="left"
        )

        self.value_label = tk.Label(
            totals_frame,
            text="Total Inventory Value: ₱0.00",
            font=("Arial", 12, "bold")
        )

        self.value_label.pack(
            side="right"
        )

    # CATEGORY REFRESH

    def refresh_categories(self):

        categories = self.service.get_categories()

        category_names = [
            category.name
            for category in categories
        ]

        self.category_combo["values"] = category_names

        if category_names:
            self.category_combo.current(0)

    # TABLE REFRESH

    def refresh_table(self):

        for row in self.tree.get_children():
            self.tree.delete(row)

        items = self.service.get_items()

        for index, item in enumerate(items):

            total = item.quantity * item.price

            self.tree.insert(
                "",
                "end",
                iid=str(index),
                values=(
                    index + 1,
                    item.name,
                    item.category,
                    item.quantity,
                    f"₱{item.price:.2f}",
                    f"₱{total:.2f}"
                )
            )

        total_quantity = self.service.get_total_quantity()
        total_value = self.service.get_total_value()

        self.quantity_label.config(
            text=f"Total Quantity: {total_quantity}"
        )

        self.value_label.config(
            text=f"Total Inventory Value: ₱{total_value:,.2f}"
        )

    # GET INPUTS

    def get_input_values(self):

        name = self.name_entry.get().strip()
        quantity_text = self.quantity_entry.get().strip()
        price_text = self.price_entry.get().strip()
        category = self.category_combo.get().strip()

        if not name:
            messagebox.showerror(
                "Invalid Input",
                "Item name cannot be empty."
            )
            return None

        if not quantity_text:
            messagebox.showerror(
                "Invalid Input",
                "Quantity cannot be empty."
            )
            return None

        if not price_text:
            messagebox.showerror(
                "Invalid Input",
                "Price cannot be empty."
            )
            return None

        if not category:
            messagebox.showerror(
                "Invalid Input",
                "Please select a category."
            )
            return None

        try:
            quantity = int(quantity_text)
        except ValueError:
            messagebox.showerror(
                "Invalid Input",
                "Quantity must be a whole number."
            )
            return None

        try:
            price = float(price_text)
        except ValueError:
            messagebox.showerror(
                "Invalid Input",
                "Price must be a number."
            )
            return None

        return name, quantity, price, category

    # ADD ITEM

    def add_item(self):

        values = self.get_input_values()

        if values is None:
            return

        name, quantity, price, category = values

        success, message = self.service.add_item(
            name,
            quantity,
            price,
            category
        )

        if success:

            messagebox.showinfo(
                "Success",
                message
            )

            self.clear_fields()
            self.refresh_table()

        else:

            messagebox.showerror(
                "Error",
                message
            )

    # SELECT ITEM

    def select_item(self, event=None):

        selection = self.tree.selection()

        if not selection:
            return

        try:
            index = int(selection[0])
        except ValueError:
            return

        item = self.service.get_item(index)

        if item is None:
            return

        self.selected_index = index
        self.name_entry.delete(0, tk.END)
        self.name_entry.insert(0, item.name)
        self.quantity_entry.delete(0, tk.END)
        self.quantity_entry.insert(0, str(item.quantity))
        self.price_entry.delete(0, tk.END)
        self.price_entry.insert(0, str(item.price))
        self.category_combo.set(item.category)

    # UPDATE ITEM

    def update_item(self):

        if self.selected_index is None:

            messagebox.showwarning(
                "No Selection",
                "Please select an item first."
            )

            return

        values = self.get_input_values()

        if values is None:
            return

        name, quantity, price, category = values

        success, message = self.service.update_item(
            self.selected_index,
            name,
            quantity,
            price,
            category
        )

        if success:

            messagebox.showinfo(
                "Success",
                message
            )

            self.clear_fields()
            self.refresh_table()

        else:

            messagebox.showerror(
                "Error",
                message
            )

    # DELETE ITEM

    def delete_item(self):

        if self.selected_index is None:

            messagebox.showwarning(
                "No Selection",
                "Please select an item first."
            )

            return

        item = self.service.get_item(
            self.selected_index
        )

        if item is None:
            return

        confirm = messagebox.askyesno(
            "Confirm Delete",
            f"Delete '{item.name}'?"
        )

        if not confirm:
            return

        success, message = self.service.delete_item(
            self.selected_index
        )

        if success:

            messagebox.showinfo(
                "Deleted",
                message
            )

            self.clear_fields()
            self.refresh_table()

        else:

            messagebox.showerror(
                "Error",
                message
            )

    # CLEAR

    def clear_fields(self):

        self.selected_index = None

        self.name_entry.delete(
            0,
            tk.END
        )

        self.quantity_entry.delete(
            0,
            tk.END
        )

        self.price_entry.delete(
            0,
            tk.END
        )

        self.refresh_categories()

        for item in self.tree.selection():
            self.tree.selection_remove(item)

    # CATEGORY MANAGER

    def open_category_manager(self):

        window = tk.Toplevel(self.root)

        window.title("Manage Categories")
        window.geometry("450x450")
        window.resizable(False, False)

        tk.Label(
            window,
            text="Category Manager",
            font=("Arial", 18, "bold")
        ).pack(pady=15)

        listbox = tk.Listbox(
            window,
            width=40,
            height=15
        )

        listbox.pack(
            padx=20,
            pady=10
        )

        def refresh_list():

            listbox.delete(
                0,
                tk.END
            )

            categories = self.service.get_categories()

            for category in categories:
                listbox.insert(
                    tk.END,
                    category.name
                )

        refresh_list()

        entry = tk.Entry(
            window,
            width=35
        )

        entry.pack(
            pady=5
        )

        def add_category():

            name = entry.get().strip()

            success, message = self.service.add_category(
                name
            )

            if success:

                messagebox.showinfo(
                    "Success",
                    message,
                    parent=window
                )

                entry.delete(
                    0,
                    tk.END
                )

                refresh_list()
                self.refresh_categories()

            else:

                messagebox.showerror(
                    "Error",
                    message,
                    parent=window
                )

        def delete_category():

            selection = listbox.curselection()

            if not selection:

                messagebox.showwarning(
                    "No Selection",
                    "Please select a category.",
                    parent=window
                )

                return

            name = listbox.get(
                selection[0]
            )

            confirm = messagebox.askyesno(
                "Confirm Delete",
                f"Delete category '{name}'?",
                parent=window
            )

            if not confirm:
                return

            success, message = self.service.delete_category(
                name
            )

            if success:

                messagebox.showinfo(
                    "Success",
                    message,
                    parent=window
                )

                refresh_list()
                self.refresh_categories()

            else:

                messagebox.showerror(
                    "Error",
                    message,
                    parent=window
                )

        button_frame = tk.Frame(window)

        button_frame.pack(
            pady=10
        )

        tk.Button(
            button_frame,
            text="Add Category",
            width=15,
            command=add_category
        ).grid(
            row=0,
            column=0,
            padx=5
        )

        tk.Button(
            button_frame,
            text="Delete Category",
            width=15,
            command=delete_category
        ).grid(
            row=0,
            column=1,
            padx=5
        )

    # CATEGORY VIEWER

    def open_category_viewer(self):

        window = tk.Toplevel(self.root)

        window.title("Category Viewer")
        window.geometry("800x600")
        window.resizable(False, False)

        tk.Label(
            window,
            text="CATEGORY VIEWER",
            font=("Arial", 20, "bold")
        ).pack(pady=15)

        top_frame = tk.Frame(window)

        top_frame.pack(
            pady=10
        )

        tk.Label(
            top_frame,
            text="Select Category:"
        ).pack(
            side="left",
            padx=5
        )

        category_combo = ttk.Combobox(
            top_frame,
            width=30,
            state="readonly"
        )

        category_combo.pack(
            side="left",
            padx=5
        )

        categories = self.service.get_categories()

        category_names = [
            category.name
            for category in categories
        ]

        category_combo["values"] = category_names

        if category_names:
            category_combo.current(0)

        summary_label = tk.Label(
            window,
            text="",
            font=("Arial", 12, "bold")
        )

        summary_label.pack(
            pady=10
        )

        # CATEGORY TABLE

        table_frame = tk.Frame(window)

        table_frame.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=10
        )

        columns = (
            "number",
            "name",
            "quantity",
            "price",
            "total"
        )

        tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            height=15
        )

        tree.heading(
            "number",
            text="#"
        )

        tree.heading(
            "name",
            text="Item Name"
        )

        tree.heading(
            "quantity",
            text="Quantity"
        )

        tree.heading(
            "price",
            text="Price"
        )

        tree.heading(
            "total",
            text="Total Value"
        )

        tree.column(
            "number",
            width=50,
            anchor="center"
        )

        tree.column(
            "name",
            width=250
        )

        tree.column(
            "quantity",
            width=100,
            anchor="center"
        )

        tree.column(
            "price",
            width=120,
            anchor="center"
        )

        tree.column(
            "total",
            width=150,
            anchor="center"
        )

        scrollbar = ttk.Scrollbar(
            table_frame,
            orient="vertical",
            command=tree.yview
        )

        tree.configure(
            yscrollcommand=scrollbar.set
        )

        tree.pack(
            side="left",
            fill="both",
            expand=True
        )

        scrollbar.pack(
            side="right",
            fill="y"
        )

        # REFRESH CATEGORY VIEW

        def refresh_category_view(event=None):

            for row in tree.get_children():
                tree.delete(row)

            category = category_combo.get()

            if not category:
                summary_label.config(text="")
                return

            items = self.service.get_items_by_category(
                category
            )

            total_quantity = self.service.get_category_total_quantity(
                category
            )

            total_value = self.service.get_category_total_value(
                category
            )

            for index, item in enumerate(items):

                total = item.quantity * item.price

                tree.insert(
                    "",
                    "end",
                    values=(
                        index + 1,
                        item.name,
                        item.quantity,
                        f"₱{item.price:.2f}",
                        f"₱{total:.2f}"
                    )
                )

            summary_label.config(
                text=(
                    f"Items: {len(items)}    |    "
                    f"Quantity: {total_quantity}    |    "
                    f"Value: ₱{total_value:,.2f}"
                )
            )

        category_combo.bind(
            "<<ComboboxSelected>>",
            refresh_category_view
        )

        refresh_category_view()