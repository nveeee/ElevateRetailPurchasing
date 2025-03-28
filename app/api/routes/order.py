from flask import jsonify, request

from .. import bp
from ...schemas import PurchaseOrderSchema, Status
from ...schemas.audit_trail import AuditTrail
from ...schemas.purchase_order import PurchaseOrder
from ...schemas.supplier import Supplier

@bp.route('/order', methods=['POST'])
def place_order():
    try:
        schema = PurchaseOrderSchema()
        data = request.json

        employee_id = data.pop('employee_id', None)
        purchase_order = schema.load(data)

        if employee_id:
            # Create audit trail
            audit_trail = AuditTrail(employee_id, "Purchase Order Placed")
            audit_trail.save_to_db()

        # Get supplier instance
        supplier = Supplier.get_supplier_by_id(purchase_order.supplier_id)
        supplier_response = supplier.send_purchase_order(purchase_order)
        if supplier_response['status'] != Status.APPROVED.value:
            raise Exception("Supplier did not approve the order")

        purchase_order.status = supplier_response['status']
        purchase_order_response = PurchaseOrder.save_to_db(purchase_order)

        return jsonify({
            'message': 'Order placed',
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