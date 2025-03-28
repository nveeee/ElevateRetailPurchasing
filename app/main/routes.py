from flask import render_template
from . import bp

@bp.route('/')
def index():
    # TODO: Get products from database
    fake_products = [
        {
            "product_id": 1,
            "product_name": "Product 1",
            "description": "This is product 1",
            "unit_price": "10.00",
            "quantity": "50",
            "supplier_id": 100,
        },
        {
            "product_id": 2,
            "product_name": "Product 2",
            "description": "This is product 2",
            "unit_price": "12.00",
            "quantity": "500",
            "supplier_id": 200,
        },
        {
            "product_id": 3,
            "product_name": "Product 3",
            "description": "This is product 3",
            "unit_price": "30.00",
            "quantity": "50",
            "supplier_id": 100,
        }
    ]

    return render_template('index.html', products=fake_products)
