import json

FILE_NAME = "inventory.json"
inventory = []


# ==============================
# FILE HANDLING
# ==============================

def load_inventory():
    """Load inventory data from the JSON file."""
    global inventory

    try:
        with open(FILE_NAME, "r") as file:
            inventory = json.load(file)

        print("Inventory data loaded successfully.")

    except FileNotFoundError:
        inventory = []
        print("No existing inventory file found. Starting with an empty inventory.")

    except json.JSONDecodeError:
        inventory = []
        print("Error: Inventory file contains invalid data.")

    except OSError as error:
        inventory = []
        print(f"Error reading inventory file: {error}")


def save_inventory():
    """Save inventory data to the JSON file."""
    try:
        with open(FILE_NAME, "w") as file:
            json.dump(inventory, file, indent=4)

    except OSError as error:
        print(f"Error saving inventory: {error}")


# ==============================
# ADD ITEM
# ==============================

def add_item():
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

    item = {
        "name": name,
        "quantity": quantity,
        "price": price
    }

    inventory.append(item)
    save_inventory()

    print("\nItem added successfully!")


# ==============================
# VIEW ITEMS
# ==============================

def view_items():
    if not inventory:
        print("\nInventory is empty.")
        return

    print("\n========== INVENTORY ==========")

    for i, item in enumerate(inventory, start=1):
        print(
            f"{i}. {item['name']} | "
            f"Quantity: {item['quantity']} | "
            f"Price: ₱{item['price']:.2f}"
        )

    print("===============================")


# ==============================
# UPDATE ITEM
# ==============================

def update_item():
    view_items()

    if not inventory:
        return

    try:
        number = int(input("\nEnter item number to update: "))
        index = number - 1

        if index < 0 or index >= len(inventory):
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

        inventory[index]["name"] = name
        inventory[index]["quantity"] = quantity
        inventory[index]["price"] = price

        save_inventory()

        print("\nItem updated successfully!")

    except ValueError:
        print("Please enter valid numbers.")


# ==============================
# DELETE ITEM
# ==============================

def delete_item():
    view_items()

    if not inventory:
        return

    try:
        number = int(input("\nEnter item number to delete: "))
        index = number - 1

        if index < 0 or index >= len(inventory):
            print("Invalid item number.")
            return

        deleted = inventory.pop(index)
        save_inventory()

        print(f"\n{deleted['name']} deleted successfully!")

    except ValueError:
        print("Please enter a valid number.")


# ==============================
# MAIN PROGRAM
# ==============================

def main():
    load_inventory()

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
            add_item()

        elif choice == "2":
            view_items()

        elif choice == "3":
            update_item()

        elif choice == "4":
            delete_item()

        elif choice == "5":
            save_inventory()
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