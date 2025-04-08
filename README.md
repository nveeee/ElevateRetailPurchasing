# Python Flask Project

The Elevate Retail Purchasing microservice processes orders by checking inventory, making shipping and payment requests, and returning order confirmation.

---

## Table of Contents

- [Installation](#installation)
- [How Flask Works](#how-flask-works)
- [Flask Schemas](#flask-schemas)
- [Usage](#usage)
- [Development Database Setup](#development-database-setup)

---

## Installation

### Prerequisites
- Python 3.6 or higher
- Git

### Cloning the Repository
To clone this repository, open your terminal and run:

```bash
git clone https://github.com/nveeee/ElevateRetailPurchasing.git
cd ElevateRetailPurchasing
```

### Installing Dependencies
Install the required packages using pip. It is recommended to use a virtual environment.

1. **Create a virtual environment (optional but recommended):**

   ```bash
   python -m venv venv
   ```

2. **Activate the virtual environment:**

   - **On Windows:**
     ```bash
     venv\Scripts\activate
     ```
   - **On macOS and Linux:**
     ```bash
     source venv/bin/activate
     ```

3. **Install the required packages:**

   ```bash
   pip install -r requirements.txt
   ```

---

## How Flask Works

Flask is a lightweight WSGI web application framework in Python that makes it easy to build web servers and handle HTTP requests. It provides a simple interface to map URLs to Python functions (view functions) using decorators, allowing you to define various endpoints to handle different HTTP methods like GET, POST, PUT, and DELETE.

### Key Concepts
- **Routes:** Flask uses decorators to map URLs to view functions.
- **HTTP Methods:** Each route can handle different HTTP methods (e.g., GET, POST, PUT, DELETE).
- **Request and Response:** Flask processes incoming HTTP requests and returns responses.
- **Templates:** Flask integrates with Jinja2 to render dynamic HTML content.

### Example of Flask Routing with Multiple HTTP Methods

Below is an example that demonstrates how to create routes that handle GET, POST, PUT, and DELETE methods:

```python
from flask import Flask, request, jsonify

app = Flask(__name__)

# GET: Retrieve a list of items
@app.route('/items', methods=['GET'])
def get_items():
    items = [
        {"id": 1, "name": "Item 1"},
        {"id": 2, "name": "Item 2"}
    ]
    return jsonify(items)

# POST: Create a new item
@app.route('/items', methods=['POST'])
def create_item():
    data = request.get_json()
    new_item = {"id": data.get("id"), "name": data.get("name")}
    return jsonify(new_item), 201

# PUT: Update an existing item by id
@app.route('/items/<int:item_id>', methods=['PUT'])
def update_item(item_id):
    data = request.get_json()
    updated_item = {"id": item_id, "name": data.get("name")}
    return jsonify(updated_item)

# DELETE: Delete an item by id
@app.route('/items/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    return jsonify({"result": f"Item {item_id} deleted"}), 200

if __name__ == '__main__':
    app.run(debug=True)
```

#### Explanation:
- **GET `/items`:** Retrieves a list of items. The function returns a JSON list of items.
- **POST `/items`:** Accepts JSON data to create a new item. The request body should contain the item's details, and the response returns the newly created item with a status code of 201 (Created).
- **PUT `/items/<item_id>`:** Updates an existing item by its `id`. The updated information is sent in the JSON request body.
- **DELETE `/items/<item_id>`:** Deletes an item by its `id` and returns a confirmation message.

This example illustrates how Flask can be used to create a RESTful API by defining routes that correspond to different HTTP methods. Each method handles specific operations on the resources, enabling you to build flexible and interactive web applications.

---

## Flask Schemas

In Flask projects, schemas are used to define the structure, validation, and serialization/deserialization rules for data. One popular library for handling schemas in Flask is **Marshmallow**. Marshmallow helps you ensure that data coming into your application meets expected formats and constraints, and it allows you to easily convert complex data types (like ORM objects) to and from Python dictionaries and JSON.

### Defining a Schema with Marshmallow

Below is an example that demonstrates how to define and use a schema in a Flask project.

```python
from flask import Flask, request, jsonify
from marshmallow import Schema, fields, validate, ValidationError

app = Flask(__name__)

# Define a schema for a User
class UserSchema(Schema):
    id = fields.Int(required=True)
    name = fields.Str(required=True, validate=validate.Length(min=1))
    email = fields.Email(required=True)

# Create schema instances for single and multiple users
user_schema = UserSchema()
users_schema = UserSchema(many=True)

# Endpoint to create a new user using the schema for validation
@app.route('/users', methods=['POST'])
def create_user():
    json_data = request.get_json()
    try:
        # Deserialize input data to validate and load into a Python dict
        data = user_schema.load(json_data)
    except ValidationError as err:
        # Return error messages if validation fails
        return jsonify(err.messages), 400

    # At this point, data is validated and can be processed (e.g., stored in a database)
    return jsonify(data), 201

if __name__ == '__main__':
    app.run(debug=True)
```

### Explanation

- **Defining the Schema:**
  - We create a `UserSchema` class that inherits from `Schema`. Each field (like `id`, `name`, and `email`) is defined using Marshmallow's field types (e.g., `fields.Int`, `fields.Str`, `fields.Email`).
  - Validation rules can be applied directly within the field definition, such as ensuring that the `name` field has at least one character.

- **Creating Schema Instances:**
  - `user_schema` is used for single user objects.
  - `users_schema` is set up with `many=True` for handling lists of users.

- **Using the Schema in an Endpoint:**
  - In the `/users` POST endpoint, the incoming JSON data is loaded and validated using `user_schema.load()`.
  - If the input data fails validation, Marshmallow raises a `ValidationError` which we catch and return as a JSON response with a 400 status code.
  - If the data is valid, it can be processed further (for example, saved to a database), and the validated data is returned in the response.

By integrating Marshmallow schemas into your Flask project, you can manage data consistency, reduce boilerplate code for input validation, and streamline the process of serializing and deserializing data for API endpoints.

---

## Usage

After installing the dependencies, run the application using:

```bash
python app.py
```

Then, open your web browser and navigate to [http://127.0.0.1:5000/](http://127.0.0.1:5000/) to see the application in action.

---

## Development Database Setup

### Docker Setup
Run the Docker command to install SQL Server in a container:

```bash
docker run -e "ACCEPT_EULA=Y" -e "MSSQL_SA_PASSWORD=<password>" \
   -p 1433:1433 --name sql1 --hostname sql1 \
   -d \
   mcr.microsoft.com/mssql/server:2022-latest
```

### Connect to the Database from Host Machine
Inside of the terminal you can run the following command to connect to the database and begin issuing commands"

```bash
sudo /opt/mssql-tools/bin/sqlcmd -S localhost,1433 -U sa -P "<password>"
```

### Create Database Tables and Insert Dummy Data
Use -i to execute SQL from files on your host machine:

```bash
sudo /opt/mssql-tools/bin/sqlcmd -S localhost,1433 -U sa -P "<password>" -i db/Elevate_Create_Table.sql 
sudo /opt/mssql-tools/bin/sqlcmd -S localhost,1433 -U sa -P "<password>" -i db/Elevate_Insert.sql 
```

---
