import pytest
from app import app, inventory


@pytest.fixture
def client():
    app.config["TESTING"] = True

    with app.test_client() as client:
        yield client


def test_get_all_inventory(client):
    response = client.get("/inventory")

    assert response.status_code == 200

    data = response.get_json()

    assert data["status"] == "success"
    assert len(data["inventory"]) > 0


def test_get_single_item(client):
    response = client.get("/inventory/1")

    assert response.status_code == 200

    data = response.get_json()

    assert data["item"]["id"] == 1


def test_get_missing_item(client):
    response = client.get("/inventory/999")

    assert response.status_code == 404

    data = response.get_json()

    assert data["status"] == "error"


def test_add_inventory_item(client):

    payload = {
        "product_name": "Test Juice",
        "brands": "Test Brand",
        "barcode": "111111",
        "price": 5.0,
        "stock": 10,
        "category": "Drinks",
        "ingredients": "Water"
    }

    response = client.post(
        "/inventory",
        json=payload
    )

    assert response.status_code == 201

    data = response.get_json()

    assert data["item"]["product_name"] == "Test Juice"


def test_update_inventory_item(client):

    response = client.patch(
        "/inventory/1",
        json={
            "price": 9.99
        }
    )

    assert response.status_code == 200

    data = response.get_json()

    assert data["item"]["price"] == 9.99


def test_delete_inventory_item(client):

    response = client.delete("/inventory/5")

    assert response.status_code == 200

    data = response.get_json()

    assert data["status"] == "success"