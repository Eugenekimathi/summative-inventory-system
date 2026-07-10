from unittest.mock import patch

from external_api import fetch_product_from_api


@patch("external_api.requests.get")
def test_fetch_product_from_api(mock_get):

    mock_get.return_value.json.return_value = {
        "status": 1,
        "product": {
            "product_name": "Mock Product",
            "brands": "Mock Brand",
            "categories": "Snacks",
            "ingredients_text": "Sugar",
            "image_url": "image.jpg"
        }
    }


    result = fetch_product_from_api("123456789")


    assert result["product_name"] == "Mock Product"
    assert result["brands"] == "Mock Brand"
    assert result["barcode"] == "123456789"