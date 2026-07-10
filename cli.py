import requests
import json

BASE_URL = "http://127.0.0.1:5000"


def print_divider():
    print("\n" + "=" * 50)


def print_item(item):
    """Print a single inventory item cleanly"""
    print(f"""
  ID:          {item['id']}
  Name:        {item['product_name']}
  Brand:       {item['brands']}
  Barcode:     {item['barcode']}
  Price:       ${item['price']}
  Stock:       {item['stock']} units
  Category:    {item['category']}
  Ingredients: {item['ingredients']}
    """)


def view_all_inventory():
    """GET /inventory — view all items"""
    print_divider()
    print("ALL INVENTORY ITEMS")
    print_divider()

    try:
        response = requests.get(f"{BASE_URL}/inventory")
        data = response.json()

        if data["status"] == "success":
            print(f"Total items: {data['count']}\n")
            for item in data["inventory"]:
                print_item(item)
        else:
            print("Failed to fetch inventory.")

    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to the server. Is Flask running?")


def view_single_item():
    """GET /inventory/<id> — view one item"""
    print_divider()
    item_id = input("Enter item ID: ").strip()

    try:
        response = requests.get(f"{BASE_URL}/inventory/{item_id}")
        data = response.json()

        if data["status"] == "success":
            print_item(data["item"])
        else:
            print(f"{data['message']}")

    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to server.")


def add_inventory_item():
    """POST /inventory — add new item"""
    print_divider()
    print("ADD NEW INVENTORY ITEM")
    print_divider()

    product_name = input("Product name: ").strip()
    brands       = input("Brand: ").strip()
    barcode      = input("Barcode: ").strip()
    category     = input("Category: ").strip()
    ingredients  = input("Ingredients: ").strip()

    # validate price input
    try:
        price = float(input("Price: $").strip())
    except ValueError:
        print("Invalid price. Please enter a number.")
        return

    # validate stock input
    try:
        stock = int(input("Stock quantity: ").strip())
    except ValueError:
        print("Invalid stock. Please enter a whole number.")
        return

    payload = {
        "product_name": product_name,
        "brands":       brands,
        "barcode":      barcode,
        "category":     category,
        "ingredients":  ingredients,
        "price":        price,
        "stock":        stock
    }

    try:
        response = requests.post(
            f"{BASE_URL}/inventory",
            json=payload
        )
        data = response.json()

        if data["status"] == "success":
            print(f"\n{data['message']}")
            print_item(data["item"])
        else:
            print(f"{data['message']}")

    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to server.")


def update_inventory_item():
    """PATCH /inventory/<id> — update price or stock"""
    print_divider()
    print("UPDATE INVENTORY ITEM")
    print_divider()

    item_id = input("Enter item ID to update: ").strip()

    print("\nWhat would you like to update?")
    print("1. Price")
    print("2. Stock")
    print("3. Both")

    choice = input("Choice: ").strip()
    payload = {}

    if choice in ["1", "3"]:
        try:
            price = float(input("New price: $").strip())
            payload["price"] = price
        except ValueError:
            print("Invalid price.")
            return

    if choice in ["2", "3"]:
        try:
            stock = int(input("New stock quantity: ").strip())
            payload["stock"] = stock
        except ValueError:
            print("Invalid stock.")
            return

    if not payload:
        print("No valid updates provided.")
        return

    try:
        response = requests.patch(
            f"{BASE_URL}/inventory/{item_id}",
            json=payload
        )
        data = response.json()

        if data["status"] == "success":
            print(f"\n{data['message']}")
            print_item(data["item"])
        else:
            print(f"{data['message']}")

    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to server.")


def delete_inventory_item():
    """DELETE /inventory/<id> — remove an item"""
    print_divider()
    print("DELETE INVENTORY ITEM")
    print_divider()

    item_id = input("Enter item ID to delete: ").strip()
    confirm = input(f"Are you sure you want to delete item {item_id}? (yes/no): ").strip().lower()

    if confirm != "yes":
        print("Cancelled.")
        return

    try:
        response = requests.delete(f"{BASE_URL}/inventory/{item_id}")
        data = response.json()

        if data["status"] == "success":
            print(f"\n{data['message']}")
        else:
            print(f"{data['message']}")

    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to server.")


def search_external_api():
    """GET /inventory/search/<barcode> — find on OpenFoodFacts"""
    print_divider()
    print("SEARCH OPENFOODFACTS API")
    print_divider()

    barcode = input("Enter product barcode: ").strip()

    try:
        response = requests.get(f"{BASE_URL}/inventory/search/{barcode}")
        data = response.json()

        if data["status"] == "success":
            product = data["product"]
            print(f"""
  Name:        {product['product_name']}
  Brand:       {product['brands']}
  Barcode:     {product['barcode']}
  Category:    {product['category']}
  Ingredients: {product['ingredients']}
            """)

            # offer to add to inventory
            add = input("Add this product to inventory? (yes/no): ").strip().lower()
            if add == "yes":
                try:
                    price = float(input("Enter price: $").strip())
                    stock = int(input("Enter stock quantity: ").strip())
                except ValueError:
                    print("Invalid price or stock.")
                    return

                product["price"] = price
                product["stock"] = stock

                add_response = requests.post(
                    f"{BASE_URL}/inventory",
                    json=product
                )
                add_data = add_response.json()
                if add_data["status"] == "success":
                    print(f"\n{add_data['message']}")
                else:
                    print(f"{add_data['message']}")
        else:
            print(f"{data['message']}")

    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to server.")


def main_menu():
    """Main CLI menu"""
    while True:
        print_divider()
        print("INVENTORY MANAGEMENT SYSTEM")
        print_divider()
        print("1. View all inventory")
        print("2. View single item")
        print("3. Add new item")
        print("4. Update item")
        print("5. Delete item")
        print("6. Search product by barcode (OpenFoodFacts)")
        print("7. Exit")
        print_divider()

        choice = input("Enter choice (1-7): ").strip()

        if choice == "1":
            view_all_inventory()
        elif choice == "2":
            view_single_item()
        elif choice == "3":
            add_inventory_item()
        elif choice == "4":
            update_inventory_item()
        elif choice == "5":
            delete_inventory_item()
        elif choice == "6":
            search_external_api()
        elif choice == "7":
            print("\nGoodbye!")
            break
        else:
            print("Invalid choice. Please enter 1-7.")


if __name__ == "__main__":
    main_menu()
