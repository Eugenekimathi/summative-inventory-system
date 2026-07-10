from unittest.mock import patch

import cli


@patch("cli.requests.get")
def test_view_all_inventory(mock_get, capsys):

    mock_get.return_value.json.return_value = {
        "status": "success",
        "count": 1,
        "inventory": [
            {
                "id": 1,
                "product_name": "Test Product",
                "brands": "Brand",
                "barcode": "123",
                "price": 2.5,
                "stock": 5,
                "category": "Food",
                "ingredients": "Water"
            }
        ]
    }


    cli.view_all_inventory()


    output = capsys.readouterr().out

    assert "Test Product" in output
    assert "Total items: 1" in output