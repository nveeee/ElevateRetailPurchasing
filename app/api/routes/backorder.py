from datetime import date
from flask import jsonify, request

from .. import bp
from ...schemas import PurchaseOrderLineSchema, Status
from ...schemas.product import Product
from ...schemas.purchase_order import PurchaseOrder
from ...schemas.supplier import Supplier

@bp.route('/backorder', methods=['POST'])
def backorder():
    try:
        schema = PurchaseOrderLineSchema()
        purchase_order_line = schema.load(request.json)

        # Calculate total amount
        total_amount = (purchase_order_line.quantity * purchase_order_line.unit_price) * 1.07

        supplier_id = Product.get_supplier_id(purchase_order_line.product_id)
        supplier = Supplier.get_supplier_by_id(supplier_id)

        purchase_order = PurchaseOrder(
            order_date=date.today(),
            total_amount=total_amount,
            payment_terms=supplier.payment_terms,
            supplier_id=supplier_id,
            status=Status.PENDING.value,
            line_items=[purchase_order_line]
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