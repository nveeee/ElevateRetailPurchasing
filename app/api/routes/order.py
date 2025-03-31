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
        data = request.form.to_dict()
        
        # Transform form data
        order_data = transform_order_data(data)
        print(order_data)  # {'1': {'unit_price': '15.00', 'quantity': '10'}, ...}

        if data.get('employee_id'):
            # Create audit trail
            audit_trail = AuditTrail(int(data['employee_id']), "Purchase Order Placed")
            audit_trail.save_to_db()

        # TODO: Create PurchaseOrderLines from data. Query database for product price.

        # TODO: Create PurchaseOrder with newly created line items
        purchase_order = schema.load(data)

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

def transform_order_data(form_data):
    """
    Transforms form data into a structured dictionary by product ID.
    
    Args:
        form_data (dict): Raw form data with keys like 'unit_price-1', 'quantity-1', etc.
        
    Returns:
        dict: Structured data with product IDs as keys and their details as values
    """
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