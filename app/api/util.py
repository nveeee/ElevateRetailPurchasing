from ..schemas.product import Product
from ..schemas.supplier import Supplier

def get_products(limit=None):
    """Get all products from the database with their supplier names"""
    products = []

    # Query all products with their suppliers, sorted by quantity
    query = Product.query.order_by(Product.quantity.asc())
    if limit is not None:
        query = query.limit(limit)

    product_list = query.all()

    for product in product_list:
        # Get the supplier name for each product
        supplier = Supplier.query.get(product.supplier_id)
        supplier_name = supplier.supplier_name if supplier else "Unknown Supplier"

        products.append({
            "product_id": product.product_id,
            "product_name": product.product_name,
            "unit_price": f"{product.unit_price:.2f}",
            "quantity": product.quantity,
            "supplier_name": supplier_name,
        })

    return products
