from datetime import date
from flask import jsonify, request, current_app as app

from .. import bp
from ...schemas import Status
from ...schemas.audit_trail import AuditTrail
from ...schemas.product import Product
from ...schemas.purchase_order import PurchaseOrder
from ...schemas.purchase_order_line import PurchaseOrderLine
from ...schemas.supplier import Supplier

@bp.route('/order', methods=['POST'])
def place_order():
    try:
        data = request.form.to_dict()

        # Transform form data
        order_data = transform_order_data(data)
        app.logger.info(f'Order data received: {order_data}')

        if data.get('employee_id'):
            # Create audit trail
            audit_trail = AuditTrail(int(data['employee_id']), "Purchase Order Placed")
            audit_trail.save_to_db()
            app.logger.info(f'Created audit trail for employee {data['employee_id']}')

        suppliers = {}
        create_po_line_items(order_data, suppliers)

        purchase_orders = []
        create_purchase_orders(purchase_orders, suppliers)
        app.logger.info(f'Created {len(purchase_orders)} purchase orders')

        try:
            send_purchase_orders(purchase_orders)
            app.logger.info('Successfully sent all purchase orders to suppliers')
            
            return jsonify({
                'message': 'Order(s) has been placed'
            }), 201
        except Exception as e:
            app.logger.error(f'Error processing order: {str(e)}')
            return jsonify({'error': str(e)}), 400
            
    except Exception as e:
        app.logger.error(f'Error in place_order: {str(e)}')
        return jsonify({'error': 'Invalid request data'}), 400


def send_purchase_orders(purchase_orders):
    for purchase_order in purchase_orders:
        supplier = Supplier.get_supplier_by_id(purchase_order.supplier_id)
        supplier_response = supplier.send_purchase_order(purchase_order)
        
        if supplier_response['status'] != Status.APPROVED.value:
            raise Exception("Supplier did not approve the order")

        purchase_order.status = supplier_response['status']
        PurchaseOrder.save_to_db(purchase_order)


def create_purchase_orders(purchase_orders, suppliers):
    for supplier_id, line_items in suppliers.items():
        total_amount = sum(item.unit_total for item in line_items)

        purchase_order = PurchaseOrder(
            order_date=date.today(),
            total_amount=total_amount,
            payment_terms="NET_30",
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
            
        if product['supplier_id'] not in suppliers:
            suppliers[product['supplier_id']] = []

        line_item = PurchaseOrderLine(
            product_id=product['product_id'],
            unit_price=details['unit_price'],
            quantity=details['quantity'],
            unit_total=int(details['quantity']) * float(details['unit_price'])
        )
        suppliers[product['supplier_id']].append(line_item)


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