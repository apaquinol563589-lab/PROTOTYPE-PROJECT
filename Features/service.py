class InventoryService:

    def __init__(self, repository):
        self.repository = repository

    # ITEM VALIDATION

    def validate_item(self, name, quantity, price, category):

        name = name.strip()
        category = category.strip()

        if not name:
            return False, "Item name cannot be empty."

        if not category:
            return False, "Category cannot be empty."

        if quantity < 0:
            return False, "Quantity cannot be negative."

        if price < 0:
            return False, "Price cannot be negative."

        category_object = self.repository.get_category(category)

        if category_object is None:
            return False, "The selected category does not exist."

        return True, ""

    # ADD ITEM

    def add_item(self, name, quantity, price, category):

        name = name.strip()
        category = category.strip()

        valid, message = self.validate_item(
            name,
            quantity,
            price,
            category
        )

        if not valid:
            return False, message

        # Use the actual category name
        category_object = self.repository.get_category(category)
        category = category_object.name

        self.repository.add_item(
            name,
            quantity,
            price,
            category
        )

        return True, "Item added successfully!"

    # UPDATE ITEM

    def update_item(
        self,
        index,
        name,
        quantity,
        price,
        category
    ):

        name = name.strip()
        category = category.strip()

        valid, message = self.validate_item(
            name,
            quantity,
            price,
            category
        )

        if not valid:
            return False, message

        if self.repository.get_item(index) is None:
            return False, "Invalid item."

        category_object = self.repository.get_category(category)
        category = category_object.name

        success = self.repository.update_item(
            index,
            name,
            quantity,
            price,
            category
        )

        if not success:
            return False, "Unable to update item."

        return True, "Item updated successfully!"

    # DELETE ITEM

    def delete_item(self, index):

        item = self.repository.get_item(index)

        if item is None:
            return False, "Invalid item."

        item_name = item.name
        success = self.repository.delete_item(index)

        if not success:
            return False, "Unable to delete item."

        return True, f"{item_name} deleted successfully!"

    # CATEGORY METHODS

    def get_categories(self):
        return self.repository.get_categories()

    def add_category(self, name):

        name = name.strip()

        if not name:
            return False, "Category name cannot be empty."

        if len(name) > 50:
            return False, "Category name is too long."

        if self.repository.category_exists(name):
            return False, "That category already exists."

        self.repository.add_category(name)

        return True, f"Category '{name}' added successfully!"

    def delete_category(self, name):

        name = name.strip()

        if not name:
            return False, "Please select a category."

        return self.repository.delete_category(name)

    # GETTERS

    def get_items(self):
        return self.repository.get_items()

    def get_item(self, index):
        return self.repository.get_item(index)

    def get_items_by_category(self, category):
        return self.repository.get_items_by_category(category)

    # TOTALS

    def get_total_quantity(self):
        return self.repository.get_total_quantity()

    def get_total_value(self):
        return self.repository.get_total_value()

    def get_category_total_quantity(self, category):
        return self.repository.get_category_total_quantity(category)

    def get_category_total_value(self, category):
        return self.repository.get_category_total_value(category)