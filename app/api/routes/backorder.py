from datetime import date
from flask import jsonify, request

from .. import bp
from ...schemas import PurchaseOrderItemSchema, Status
from ...schemas.product import Product
from ...schemas.purchase_order import PurchaseOrder
from ...schemas.supplier import Supplier


@bp.route('/backorder', methods=['POST'])
def backorder():
    """
    Places a backorder for a purchase order line item.

    Request JSON:
        {
            "product_id": 123,
            "quantity": 10,
            "unit_price": 15.0
        }
    Returns:
        Response: A JSON response containing the details of the placed purchase order if successful:
        {
            "message": "Backorder successfully placed",
            "purchase_order": {
                "id": 456,
                "supplier_id": 789,
                "order_date": "2025-04-07",
                "total_amount": 150.0,
                "payment_terms": "Net 30",
                "status": "APPROVED"
            }
        }
        Error: A JSON response with an error message if the operation fails.
    """
    try:
        schema = PurchaseOrderItemSchema()
        purchase_order_item = schema.load(request.json)

        # Calculate total amount
        total_amount = (purchase_order_item.quantity * purchase_order_item.unit_price)

        supplier_id = Product.get_supplier_id(purchase_order_item.product_id)
        supplier = Supplier.query.get(supplier_id)

        purchase_order = PurchaseOrder(
            order_date=date.today(),
            total_amount=total_amount,
            payment_terms=supplier.payment_terms,
            supplier_id=supplier_id,
            status=Status.PENDING.value,
            line_items=[purchase_order_item]
        )

        supplier_response = supplier.send_purchase_order(purchase_order)
        if supplier_response['status'] != Status.APPROVED.value:
            raise Exception("Supplier did not approve the order")

        purchase_order.status = supplier_response['status']
        purchase_order_response = PurchaseOrder.save_to_db(purchase_order)

        return jsonify({
            'message': 'Backorder successfully placed',
            'purchase_order': {
                'id': purchase_order_response['purchase_order_id'],
                'supplier_id': purchase_order.supplier_id,
                'order_date': purchase_order.order_date,
                'total_amount': purchase_order.total_amount,
                'payment_terms': purchase_order.payment_terms,
                'status': purchase_order.status
            }
        }), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500
