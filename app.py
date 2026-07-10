from flask import Flask, jsonify , request 
from external_api  import fetch_product_from_api

app = Flask(__name__)

inventory = [
    {
      "id": 1,
        "product_name": "Organic Almond Milk",
        "brands": "Silk",
        "barcode": "0025293004269",
        "price": 3.99,
        "stock": 50,
        "category": "Beverages",
        "ingredients": "Filtered water, almonds, cane sugar, sea salt"  
    },
    {
      "id": 2,
        "product_name": "Whole Grain Bread",
        "brands": "Nature's Own",
        "barcode": "0072250007123",
        "price": 2.49,
        "stock": 30,
        "category": "Bakery",
        "ingredients": "Whole wheat flour, water, yeast, salt"  
    },
    {
      "id": 3,
        "product_name": "Greek Yogurt",
        "brands": "Chobani",
        "barcode": "0818290001002",
        "price": 1.99,
        "stock": 75,
        "category": "Dairy",
        "ingredients": "Cultured nonfat milk, evaporated cane juice"  
    },
    {
        "id": 4,
        "product_name": "Orange Juice",
        "brands": "Tropicana",
        "barcode": "0048500002506",
        "price": 4.29,
        "stock": 40,
        "category": "Beverages",
        "ingredients": "100% pure squeezed pasteurized orange juice"
    },
    {
        "id": 5,
        "product_name": "Dark Chocolate Bar",
        "brands": "Lindt",
        "barcode": "0009542007834",
        "price": 2.99,
        "stock": 60,
        "category": "Snacks",
        "ingredients": "Cocoa mass, sugar, cocoa butter, vanilla"
    }
]

def get_next_id():
    if not inventory:
        return 1
    return max(item["id"] for item in inventory) + 1

# GET - Fetch all items 
@app.route("/inventory", methods=["GET"])
def get_all_inventory():
    return jsonify({
        "status":"success",
        "count": len(inventory),
        "inventory": inventory
    }), 200

# GET - fetch single item/<id>
@app.route("/inventory/<int:item_id>", methods=["GET"])
def get_inventory_item(item_id):
    item = next((i for i in inventory if i["id"] == item_id), None)

    if not item:
        return jsonify({"status": "error", "message": "item not found"}), 404
    return jsonify({"status": "success", "item": item}), 200

# POST - add new item 
@app.route("/inventory", methods=["POST"])
def add_inventory_item():
    data = request.get_json()
    if not data or "product_name" not in data: # validate required fields
        return jsonify({
            "status": "error",
            "message": "product_name is required"
        }), 400
    
    new_item = {
        "id":           get_next_id(),
        "product_name": data.get("product_name"),
        "brands":       data.get("brands", "Unknown"),
        "barcode":      data.get("barcode", ""),
        "price":        data.get("price", 0.0),
        "stock":        data.get("stock", 0),
        "category":     data.get("category", "General"),
        "ingredients":  data.get("ingredients", "")
    }

    inventory.append(new_item)
    return jsonify({
        "status": "success",
        "message": "Item added successfully",
        "item": new_item
    }), 201

# PATCH - update item/<id>
@app.route("/inventory/<int:item_id>", methods=["PATCH"])
def update_inventory_item(item_id):
    item = next((i for i in inventory if i["id"] == item_id), None)

    if not item:
        return jsonify({"status": "error", "message": "Item not found"}), 404
    data = request.get_json()
    if not data:
        return jsonify({
            "status": "error",
            "message": "No data provided"
        }), 400
    
    allowed_fields = ["product_name", "brands", "barcode",
                      "price", "stock", "category", "ingredients"]
    for field in allowed_fields: # update only provided fields
        if field in data:
            item[field] = data[field]

    return jsonify({
        "status": "success",
        "message": "Item updated successfully",
        "item": item
    }), 200

# DELETE - remove item/<id>
@app.route("/inventory/<int:item_id>", methods=["DELETE"])
def delete_inventory_item(item_id):
    item = next((i for i in inventory if i["id"] == item_id), None)

    if not item:
        return jsonify({"status": "error", "message": "Item not found"}), 404
    inventory.remove(item)

    return jsonify({
        "status": "success",
        "message": f"Item {item_id} deleted successfully"
    }), 200

# GET - fetch by <barcode>
@app.route("/inventory/search/<barcode>", methods=["GET"])
def search_external_api(barcode):
    product = fetch_product_from_api(barcode)

    if not product:
        return jsonify({
            "status": "error",
            "message": "Product not found in external API"
        }), 404
    return jsonify({"status": "success", "product": product}), 200

if __name__ == "__main__":
    app.run(debug=True)
    
