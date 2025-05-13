import json
import os

STORAGE_FILE = 'storage.json'

# Load existing warehouse or create a new one
def load_storage():
    if os.path.exists(STORAGE_FILE):
        with open(STORAGE_FILE, 'r') as f:
            return json.load(f)
    return []

# Save warehouse to file
def save_storage(storage):
    with open(STORAGE_FILE, 'w') as f:
        json.dump(storage, f, indent=4)

# Add a new product
def add_product():
    name = input("Product name: ")
    quantity = int(input("Quantity: "))
    price = float(input("Price per unit: "))

    product = {
        "name": name,
        "quantity": quantity,
        "price": price
    }

    storage = load_storage()
    storage.append(product)
    save_storage(storage)
    print(f"{name} was added to the storage.")

def delete_product():
    name = input("Enter the name of the product to delete: ").strip()

    storage = load_storage()
    original_length = len(storage)

    storage = [product for product in storage if product['name'].lower() != name.lower()]

    if len(storage) < original_length:
        save_storage(storage)
        print(f"{name} was deleted from the storage")
    else:
        print(f"No product named '{name}' was found.")

def show_storage():
    storage = load_storage()

    if not storage:
        print("Storage is currently empty")
        return
    
    print("\n--- Current Storage ---")
    for i, product in enumerate(storage, start=1):
        print(f"{i}. Name: {product['name']}, Quantity: {product['quantity']}, Price: ${product['price']:.2f}")

def search_product():
    search_term = input("Enter product name to search for: ").strip().lower()
    storage = load_storage()
    matches = [product for product in storage if search_term in product['name'].lower()]

    if matches:
        print(f"\n--- Search Results for '{search_term}' ---")
        for i, product in enumerate(matches, start=1):
            print(f"{i}. Name: {product['name']}, Quantity: {product['quantity']}, Price: ${product['price']:.2f}")
    else:
        print(f"No products found matching '{search_term}'.")


# Main menu
def main_menu():
    while True:
        print("\n--- Storage System ---")
        print("1. Add product")
        print("2. Delete product")
        print("3. Search for product")
        print("4. Show storage")
        print("5. Exit")
        choice = input("Choose an option: ")

        if choice == '1':
            add_product()
        elif choice == '2':
            delete_product()
        elif choice == '3':
            search_product()
        elif choice == '4':
            show_storage()
        elif choice == '5':
            print("Exiting program.")
            break
        else:
            print("Invalid")

main_menu()