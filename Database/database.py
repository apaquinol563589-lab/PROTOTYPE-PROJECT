import json
import os

INVENTORY_FILE = "inventory.json"
CATEGORIES_FILE = "categories.json"

def load_inventory():
    if not os.path.exists(INVENTORY_FILE):
        return []

    try:
        with open(INVENTORY_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)

        if isinstance(data, list):
            return data

        return []

    except json.JSONDecodeError:
        print("Error: inventory.json contains invalid JSON.")
        return []

    except OSError as error:
        print(f"Error loading inventory: {error}")
        return []

def save_inventory(data):
    try:
        with open(INVENTORY_FILE, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)

    except OSError as error:
        print(f"Error saving inventory: {error}")


def load_categories():
    if not os.path.exists(CATEGORIES_FILE):
        return []

    try:
        with open(CATEGORIES_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)

        if isinstance(data, list):
            return data

        return []

    except json.JSONDecodeError:
        print("Error: categories.json contains invalid JSON.")
        return []

    except OSError as error:
        print(f"Error loading categories: {error}")
        return []

def save_categories(data):
    try:
        with open(CATEGORIES_FILE, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)

    except OSError as error:
        print(f"Error saving categories: {error}")