import json


# ==============================
# INVENTORY ITEM CLASS
# ==============================

class InventoryItem:

    def __init__(self, name, quantity, price):
        self.name = name
        self.quantity = quantity
        self.price = price

    def to_dict(self):
        return {
            "name": self.name,
            "quantity": self.quantity,
            "price": self.price
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            data["name"],
            data["quantity"],
            data["price"]
        )


# ==============================
# INVENTORY CLASS
# ==============================

class Inventory:

    def __init__(self, file_name):
        self.file_name = file_name
        self.items = []

    # ==========================
    # FILE HANDLING
    # ==========================

    def load_inventory(self):
        """Load inventory data from the JSON file."""

        try:
            with open(self.file_name, "r") as file:
                data = json.load(file)

                self.items = [
                    InventoryItem.from_dict(item)
                    for item in data
                ]

            print("Inventory data loaded successfully.")

        except FileNotFoundError:
            self.items = []
            print(
                "No existing inventory file found. "
                "Starting with an empty inventory."
            )

        except json.JSONDecodeError:
            self.items = []
            print("Error: Inventory file contains invalid data.")

        except OSError as error:
            self.items = []
            print(f"Error reading inventory file: {error}")

    def save_inventory(self):
        """Save inventory data to the JSON file."""

        try:
            data = [
                item.to_dict()
                for item in self.items
            ]

            with open(self.file_name, "w") as file:
                json.dump(data, file, indent=4)

        except OSError as error:
            print(f"Error saving inventory: {error}")

    # ==========================
    # ADD ITEM
    # ==========================

    def add_item(self):

        name = input("Enter item name: ").strip()

        if not name:
            print("Item name cannot be empty.")
            return

        try:
            quantity = int(input("Enter quantity: "))

            if quantity < 0:
                print("Quantity cannot be negative.")
                return

            price = float(input("Enter price: ₱"))

            if price < 0:
                print("Price cannot be negative.")
                return

        except ValueError:
            print("Please enter valid numbers for quantity and price.")
            return

        item = InventoryItem(name, quantity, price)

        self.items.append(item)
        self.save_inventory()

        print("\nItem added successfully!")

    # ==========================
    # VIEW ITEMS
    # ==========================

    def view_items(self):

        if not self.items:
            print("\nInventory is empty.")
            return

        print("\n========== INVENTORY ==========")

        for i, item in enumerate(self.items, start=1):
            print(
                f"{i}. {item.name} | "
                f"Quantity: {item.quantity} | "
                f"Price: ₱{item.price:.2f}"
            )

        print("===============================")

    # ==========================
    # UPDATE ITEM
    # ==========================

    def update_item(self):

        self.view_items()

        if not self.items:
            return

        try:
            number = int(input("\nEnter item number to update: "))
            index = number - 1

            if index < 0 or index >= len(self.items):
                print("Invalid item number.")
                return

            name = input("New item name: ").strip()

            if not name:
                print("Item name cannot be empty.")
                return

            quantity = int(input("New quantity: "))

            if quantity < 0:
                print("Quantity cannot be negative.")
                return

            price = float(input("New price: ₱"))

            if price < 0:
                print("Price cannot be negative.")
                return

            self.items[index].name = name
            self.items[index].quantity = quantity
            self.items[index].price = price

            self.save_inventory()

            print("\nItem updated successfully!")

        except ValueError:
            print("Please enter valid numbers.")

    # ==========================
    # DELETE ITEM
    # ==========================

    def delete_item(self):

        self.view_items()

        if not self.items:
            return

        try:
            number = int(input("\nEnter item number to delete: "))
            index = number - 1

            if index < 0 or index >= len(self.items):
                print("Invalid item number.")
                return

            deleted = self.items.pop(index)
            self.save_inventory()

            print(f"\n{deleted.name} deleted successfully!")

        except ValueError:
            print("Please enter a valid number.")


# ==============================
# MAIN PROGRAM
# ==============================

def main():

    file_name = "inventory.json"

    inventory = Inventory(file_name)

    inventory.load_inventory()

    while True:

        print("\n==============================")
        print("   PERSONAL INVENTORY SYSTEM")
        print("==============================")
        print("1. Add Item")
        print("2. View Items")
        print("3. Update Item")
        print("4. Delete Item")
        print("5. Exit")
        print("==============================")

        choice = input("Enter choice: ").strip()

        if choice == "1":
            inventory.add_item()

        elif choice == "2":
            inventory.view_items()

        elif choice == "3":
            inventory.update_item()

        elif choice == "4":
            inventory.delete_item()

        elif choice == "5":
            inventory.save_inventory()
            print("\nInventory saved.")
            print("Goodbye!")
            break

        else:
            print("\nInvalid choice. Please try again.")


# ==============================
# START PROGRAM
# ==============================

if __name__ == "__main__":
    main()
