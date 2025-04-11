from ..schemas.product import Product
from ..schemas.inventory import Inventory

from sqlalchemy import asc


def get_products(limit=None):
    """ Get all products from the database with their supplier names. """
    products = []

    # Query all products with their suppliers, sorted by quantity
    query = Product.query.join(
        Inventory, Product.id == Inventory.product_id
    ).order_by(asc(Inventory.quantity))

    if limit is not None:
        query = query.limit(limit)

    product_list = query.all()

    for product in product_list:
        # Get the inventory record associated with this product
        inventory = Inventory.query.filter_by(product_id=product.id).first()

        # Get the supplier name
        supplier_name = product.supplier.supplier_name if product.supplier else "Unknown Supplier"

        products.append({
            "product_id": product.id,
            "product_name": product.product_name,
            "unit_price": f"{inventory.unit_price:.2f}" if inventory else "0.00",
            "quantity": inventory.quantity if inventory else 0,
            "supplier_name": supplier_name,
        })

    return products
