from flask import Flask, jsonify, request

app = Flask(__name__)

# Task 2: Mock database initialized as a list containing OpenFoodFacts-like data
inventory_db = [
    {
        "id": "1",
        "code": "301",
        "product_name": "Nutella 400g",
        "price": 5.99,
        "quantity": 50,
        "brands": "Ferrero"
    },
    {
        "id": "2",
        "code": "544",
        "product_name": "CocaCola Zero 330ml",
        "price": 1.49,
        "quantity": 120,
        "brands": "Coca-Cola"
    }
]

# --- Helper Function for External API Integration (Task 3) ---
import requests  # Ensure requests is imported at the very top of app.py

def fetch_from_openfoodfacts(barcode_or_name):
    """
    Task 3: Queries the official live OpenFoodFacts API to fetch real product details.
    """
    # Clean up the input string
    search_query = str(barcode_or_name).strip()
    
    # Check if the query is a purely numeric barcode string
    if search_query.isdigit():
        # OpenFoodFacts Product Endpoint v3 standard URL structure
        url = f"https://world.openfoodfacts.org/api/v3/product/{search_query}.json"
        try:
            response = requests.get(url, headers={'User-Agent': 'InventoryAdminPortal - Web - Version 1.0'})
            if response.status_code == 200:
                data = response.json()
                if data.get("status") == "success" and "product" in data:
                    product = data["product"]
                    return {
                        "code": search_query,
                        "product_name": product.get("product_name", "Unknown Product"),
                        "brands": product.get("brands", "Unknown Brand")
                    }
        except requests.exceptions.RequestException:
            pass # Gracefully return None on network connection drops
            
    else:
        # Text string fallback: Search for matching items using text querying
        url = "https://world.openfoodfacts.org/cgi/search.pl"
        params = {
            "search_terms": search_query,
            "json": 1,
            "page_size": 1
        }
        try:
            response = requests.get(url, params=params, headers={'User-Agent': 'InventoryAdminPortal - Web - Version 1.0'})
            if response.status_code == 200:
                data = response.json()
                products = data.get("products", [])
                if products:
                    product = products[0]
                    return {
                        "code": product.get("code", "N/A"),
                        "product_name": product.get("product_name", "Unknown Product"),
                        "brands": product.get("brands", "Unknown Brand")
                    }
        except requests.exceptions.RequestException:
            pass

    return None
    

# --- API Routes (Task 3: API Design) ---

# GET /inventory -> Fetch all items
@app.route('/inventory', methods=['GET'])
def get_all_items():
    return jsonify(inventory_db), 200

# GET /inventory/<id> -> Fetch a single item
@app.route('/inventory/<string:item_id>', methods=['GET'])
def get_item(item_id):
    item = next((i for i in inventory_db if i["id"] == item_id), None)
    if item:
        return jsonify(item), 200
    return jsonify({"error": "Item not found"}), 404

# POST /inventory -> Add a new item
@app.route('/inventory', methods=['POST'])
def add_item():
    data = request.get_json() or {}
    
    # Validation
    if not data.get("product_name"):
        return jsonify({"error": "Missing required field: product_name"}), 400
        
    # Auto-generate incremental ID based on your schema
    new_id = str(max([int(item["id"]) for item in inventory_db]) + 1) if inventory_db else "1"
    
    new_item = {
        "id": new_id,
        "code": data.get("code", "N/A"),
        "product_name": data.get("product_name"),
        "price": float(data.get("price", 0.0)),
        "quantity": int(data.get("quantity", 0)),
        "brands": data.get("brands", "Unknown")
    }
    
    inventory_db.append(new_item)
    return jsonify(new_item), 201

# PATCH /inventory/<id> -> Update an item
@app.route('/inventory/<string:item_id>', methods=['PATCH'])
def update_item(item_id):
    item = next((i for i in inventory_db if i["id"] == item_id), None)
    if not item:
        return jsonify({"error": "Item not found"}), 404
        
    data = request.get_json() or {}
    
    # Selective updates
    if "price" in data:
        item["price"] = float(data["price"])
    if "quantity" in data:
        item["quantity"] = int(data["quantity"])
    if "product_name" in data:
        item["product_name"] = data["product_name"]
        
    return jsonify(item), 200

# DELETE /inventory/<id> -> Remove an item
@app.route('/inventory/<string:item_id>', methods=['DELETE'])
def delete_item(item_id):
    global inventory_db
    item = next((i for i in inventory_db if i["id"] == item_id), None)
    if not item:
        return jsonify({"error": "Item not found"}), 404
        
    inventory_db = [i for i in inventory_db if i["id"] != item_id]
    return jsonify({"message": f"Item {item_id} deleted successfully"}), 200

# External API Proxy Endpoint for CLI usage
@app.route('/external-search', methods=['GET'])
def external_search():
    query = request.args.get('q')
    if not query:
        return jsonify({"error": "Missing search query parameter 'q'"}), 400
    
    result = fetch_from_openfoodfacts(query)
    if result:
        return jsonify(result), 200
    return jsonify({"error": "Product not found on external API"}), 404

if __name__ == '__main__':
    # Run server in debug mode as instructed in Task 4
    app.run(port=5000, debug=True)
