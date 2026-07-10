import requests

OPENFOODDFACTS_URL = "https://world.openfoodfacts.org/api/v0/product"

def fetch_product_from_api(barcode):
    try:
        url = f"{OPENFOODDFACTS_URL}/{barcode}.json"
        response = requests.get(url, timeout=5)
        data = response.json()

        if data.get("status") != 1: # status 1 means product found
            return None
        
        product = data.get("product", {})

        return {
            "product_name": product.get("product_name", "Unknown"),
            "brands":       product.get("brands", "Unknown"),
            "barcode":      barcode,
            "category":     product.get("categories", "General"),
            "ingredients":  product.get("ingredients_text", ""),
            "image_url":    product.get("image_url", "")
        }
    except requests.exceptions.RequestException as e:
        print(f"API Error: {e}")
        return None