# summative-inventory-system
# Inventory Management System

## Project Overview

This project is a simple Inventory Management System built with **Flask**. It provides a REST API for managing inventory items and includes a command-line interface (CLI) for interacting with the application. The project also integrates with the **OpenFoodFacts API**, allowing users to search for products by barcode and add them to the inventory.

## Features

* View all inventory items
* View a single inventory item by ID
* Add new inventory items
* Update existing inventory items
* Delete inventory items
* Search products using the OpenFoodFacts API
* Simple command-line interface (CLI)
* Unit tests using Pytest

## Installation

Clone the repository:

```bash
git clone <your-repo-url>
```

Move into the project folder:

```bash
cd inventory-system
```

Create and activate a virtual environment (recommended):

```bash
python -m venv venv
```

Install the required packages:

```bash
pip install -r requirements.txt
```

## Running the Application

Start the Flask server:

```bash
python app.py
```

Open another terminal and run the CLI:

```bash
python cli.py
```

## Running the Tests

Run all tests with:

```bash
pytest
```

or run a specific test file:

```bash
pytest tests/test_app.py -v
```

## API Endpoints

## API Endpoints

### Get all inventory items

* **Method:** GET
* **Endpoint:** `/inventory`
* **Description:** Returns all inventory items.

### Get a single inventory item

* **Method:** GET
* **Endpoint:** `/inventory/<id>`
* **Description:** Returns the details of a specific inventory item.

### Add a new inventory item

* **Method:** POST
* **Endpoint:** `/inventory`
* **Description:** Adds a new item to the inventory.

### Update an inventory item

* **Method:** PATCH
* **Endpoint:** `/inventory/<id>`
* **Description:** Updates one or more fields of an existing inventory item.

### Delete an inventory item

* **Method:** DELETE
* **Endpoint:** `/inventory/<id>`
* **Description:** Removes an item from the inventory.

### Search for a product by barcode

* **Method:** GET
* **Endpoint:** `/inventory/search/<barcode>`
* **Description:** Searches the OpenFoodFacts API using a product barcode and returns the product information if found.

## Technologies Used

* Python
* Flask
* Requests
* Pytest
* OpenFoodFacts API

## Author

Created as part of a Flask and REST API learning project.
