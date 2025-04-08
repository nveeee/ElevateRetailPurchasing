# Import necessary functions
from flask import render_template
from . import bp
from ..schemas.product import Product


# Function to get products from the database, ordered by quantity in ascending order
def get_products(limit=None):
    products = []


    query = Product.query.order_by(Product.quantity.asc())
    if limit is not None:
        query = query.limit(limit)

    product_list = query.all()

    # Prepare a list of products with the necessary attributes
    for product in product_list:
        products.append({
            "product_id": product.product_id,
            "product_name": product.product_name,
            "quantity": product.quantity,
            "supplier_name": product.supplier_name,
        })

    return products


# Add a new route for the inventory alerts
@bp.route('/inventory_alerts')
def inventory_alerts():
    # Get the products, (or change this limit as needed)
    products = get_products(limit=10)

    return render_template('includes/alerts-table.html', products=products)
