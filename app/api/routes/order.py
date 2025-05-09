from datetime import date
from flask import jsonify, request, current_app as app

from ...schemas.inventory import Inventory

from .. import bp
from ...schemas import Status
from ...schemas.product import Product
from ...schemas.purchase_order import PurchaseOrder
from ...schemas.purchase_order_item import PurchaseOrderItemSchema
from ...schemas.supplier import Supplier


@bp.route('/order', methods=['POST'])
def place_order():
    """
    Places one or more orders based on submitted form data.

    Request Form Data:
        {
            "123": {
                "unit_price": 15.0,
                "quantity": 10
            },
            "456": {
                "unit_price": 20.0,
                "quantity": 5
        }
    Returns:
        Response: A JSON response indicating the success of the order placement:
        {
            "message": "Order(s) Placed"
        }
        Error: A JSON response with an error message if the operation fails.
    """
    try:
        data = request.form.to_dict()

        # Transform form data
        order_data = transform_order_data(data)
        app.logger.info(f'Order data received: {order_data}')

        suppliers = {}
        create_po_line_items(order_data, suppliers)

        purchase_orders = []
        create_purchase_orders(purchase_orders, suppliers)
        app.logger.info(f'Created {len(purchase_orders)} purchase orders')

        try:
            send_purchase_orders(purchase_orders)
            app.logger.info('Successfully sent all purchase orders to suppliers')

            return app.redirect('/purchasing/order_success')
        except Exception as e:
            app.logger.error(f'Error processing order: {str(e)}')
            return jsonify({'error': str(e)}), 400

    except Exception as e:
        app.logger.error(f'Error in place_order: {str(e)}')
        return jsonify({'error': 'Invalid request data'}), 400


def send_purchase_orders(purchase_orders):
    for purchase_order in purchase_orders:
        supplier = Supplier.query.get(purchase_order.supplier_id)
        supplier_response = supplier.send_purchase_order(purchase_order)

        if supplier_response['status'] != Status.RECEIVED.value:
            raise Exception("Supplier did not approve the order")

        purchase_order.status = supplier_response['status']
        PurchaseOrder.save_to_db(purchase_order)


def create_purchase_orders(purchase_orders, suppliers):
    for supplier_id, line_items in suppliers.items():
        total_amount = 0
        for item in line_items:
            inventory = Inventory.query.filter_by(product_id=item.product_id).first()
            total_amount += inventory.unit_price * item.quantity

        # TODO: Figure out solution for missing Purchase Order Information

        purchase_order = PurchaseOrder(
            order_date=date.today(),
            supplier_id=supplier_id,
            status=Status.PENDING.value,
            line_items=line_items
        )
        purchase_orders.append(purchase_order)


def create_po_line_items(order_data, suppliers):
    for pid, details in order_data.items():
        product = Product.get_product_by_id(pid)
        if not product:
            raise Exception(f"Product with ID {pid} not found")

        if product.supplier_id not in suppliers:
            suppliers[product.supplier_id] = []

        schema = PurchaseOrderItemSchema()
        line_item = schema.load({
            'product_id': product.id,
            'quantity': details['quantity'],
        })

        suppliers[product.supplier_id].append(line_item)


def transform_order_data(form_data):
    transformed = {}

    # Find all unique product IDs
    product_ids = set(
        key.split('-')[-1]
        for key in form_data.keys()
        if key.startswith('product_id-')
    )

    # Build structured data
    for pid in product_ids:
        transformed[pid] = {
            'unit_price': form_data.get(f'unit_price-{pid}'),
            'quantity': form_data.get(f'quantity-{pid}')
        }

    return transformed
