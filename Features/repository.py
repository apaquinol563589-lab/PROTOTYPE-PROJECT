from Features.model import Item, Category
from Database.database import (
    load_inventory,
    save_inventory,
    load_categories,
    save_categories
)

class InventoryRepository:

    def __init__(self):
        self.items = []
        self.categories = []
        self.load_data()

    # LOAD DATA

    def load_data(self):
        inventory_data = load_inventory()
        category_data = load_categories()

        self.items = []
        self.categories = []

        # Load items
        for data in inventory_data:
            try:
                self.items.append(Item.from_dict(data))
            except (KeyError, TypeError, ValueError):
                print("Warning: An invalid inventory item was skipped.")

        # Load categories
        for data in category_data:
            try:
                self.categories.append(Category.from_dict(data))
            except (KeyError, TypeError, ValueError):
                print("Warning: An invalid category was skipped.")

        ## Always make sure General exists
        if not self.category_exists("General"):
            self.categories.insert(0, Category("General"))
            self.save_categories()

        ## Fix missing categories
        changed = False

        for item in self.items:
            if not item.category:
                item.category = "General"
                changed = True

            category = self.get_category(item.category)

            if category is None:
                item.category = "General"
                changed = True
            else:
                # Use the actual category capitalization
                if item.category != category.name:
                    item.category = category.name
                    changed = True

        if changed:
            self.save_items()

    # SAVE DATA

    def save_items(self):
        data = []

        for item in self.items:
            data.append(item.to_dict())

        save_inventory(data)

    def save_categories(self):
        data = []

        for category in self.categories:
            data.append(category.to_dict())

        save_categories(data)

    # ITEM METHODS

    def get_items(self):
        return self.items

    def get_item(self, index):
        if index < 0 or index >= len(self.items):
            return None

        return self.items[index]

    def add_item(self, name, quantity, price, category):
        item = Item(
            name=name,
            quantity=quantity,
            price=price,
            category=category
        )

        self.items.append(item)
        self.save_items()

        return item

    def update_item(self, index, name, quantity, price, category):
        if index < 0 or index >= len(self.items):
            return False

        item = self.items[index]

        item.name = name
        item.quantity = quantity
        item.price = price
        item.category = category

        self.save_items()

        return True

    def delete_item(self, index):
        if index < 0 or index >= len(self.items):
            return False

        self.items.pop(index)
        self.save_items()

        return True

    # CATEGORY METHODS

    def get_categories(self):
        return self.categories

    def get_category(self, name):
        if name is None:
            return None

        for category in self.categories:
            if category.name.lower() == name.strip().lower():
                return category

        return None

    def category_exists(self, name):
        return self.get_category(name) is not None

    def add_category(self, name):
        if self.category_exists(name):
            return False

        self.categories.append(Category(name.strip()))
        self.save_categories()

        return True

    def delete_category(self, name):
        category = self.get_category(name)

        if category is None:
            return False, "Category does not exist."

        if category.name.lower() == "general":
            return False, "The General category cannot be deleted."

        # Check if category contains items
        for item in self.items:
            if item.category.lower() == category.name.lower():
                return False, (
                    f"Cannot delete '{category.name}' because "
                    f"it contains inventory items."
                )

        self.categories.remove(category)
        self.save_categories()

        return True, f"Category '{category.name}' deleted successfully."

    # CATEGORY ITEM METHODS

    def get_items_by_category(self, category_name):
        category = self.get_category(category_name)

        if category is None:
            return []

        return [
            item
            for item in self.items
            if item.category.lower() == category.name.lower()
        ]

    def get_category_total_quantity(self, category_name):
        items = self.get_items_by_category(category_name)

        total = 0

        for item in items:
            total += item.quantity

        return total

    def get_category_total_value(self, category_name):
        items = self.get_items_by_category(category_name)

        total = 0

        for item in items:
            total += item.quantity * item.price

        return total

    # TOTALS

    def get_total_quantity(self):
        total = 0

        for item in self.items:
            total += item.quantity

        return total

    def get_total_value(self):
        total = 0

        for item in self.items:
            total += item.quantity * item.price

        return total