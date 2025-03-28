from flask import jsonify, request
from marshmallow import ValidationError

from . import bp
from ..schemas import PurchaseOrderSchema, SupplierSchema
from ..schemas.audit_trail import AuditTrail
from ..schemas.employee import Employee
import logging

from ..schemas.supplier import Supplier


@bp.route('/order', methods=['POST'])
def place_order():
    try:
        schema = PurchaseOrderSchema()
        data = request.json

        employee_id = data.pop('employee_id', None)
        purchase_order = schema.load(data)

        if employee_id:
            # Create audit trail
            audit_trail = AuditTrail(employee_id, "Purchase Order Created")

            # TODO: Send to database


        # Get supplier instance (you'll need to implement this)
        supplier = get_supplier(purchase_order.supplier_id)
        supplier_response = supplier.send_purchase_order(purchase_order)

        # TODO: Check if supplier purchase order succeeded

        # TODO: Insert Purchase Order into Database here

        return jsonify({
            'message': 'Order placed',
            'purchase_order': {
                'id': purchase_order.purchase_order_id,
                'supplier_id': purchase_order.supplier_id,
                'order_date': purchase_order.order_date,
                'total_amount': purchase_order.total_amount,
                'payment_terms': purchase_order.payment_terms,
                'status': purchase_order.status
            }
        }), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@bp.route('/auto_order', methods=['POST'])
def auto_order():
    try:
        data = request.json
        supplier_id = data.get('supplier_id')
        order_date = data.get('order_date')
        line_items = data.get('line_items',[])
        payment_terms = data.get('payment_terms')

        if not supplier_id or not order_date or not line_items:
            return jsonify({'error': 'Missing required fields'}),400

        purchase_order = {
            'supplier_id': supplier_id,
            'order_date': order_date,
            'line_items': line_items,
            'payment_terms': payment_terms,
            'status': 'Pending'
        }

        # Get supplier
        supplier = get_supplier(supplier_id)
        supplier.send_purchase_order(purchase_order)

        #TODO: insert purchase order into Database here.

        response = {
            'message': 'Automatic Order placed',
            'purchase_order': purchase_order
        }

        logging.info(f'Auto order response: {response}')

        return jsonify(response), 201
    except Exception as e:
        logging.error(f'Error in auto order: {e}')
        return jsonify({'error': str(e)}), 500



@bp.route('/create_supplier', methods=['POST'])
def create_supplier():
    try:
        schema = SupplierSchema()
        supplier = schema.load(request.json)

        # TODO: Insert Supplier into Database here

        return jsonify({
            'message': 'Supplier created',
            'supplier': {
                'id': supplier.supplier_id,
                'name': supplier.supplier_name,
                'contact': supplier.contact_info,
                'payment_terms': supplier.payment_terms
            }
        }), 201
    except ValidationError as err:
        return jsonify({'errors': err.messages}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/backorder', methods=['POST'])
def backorder():
    try:
        schema = PurchaseOrderSchema()
        purchase_order = schema.load(request.json)

        # Get supplier instance (you'll need to implement this)
        supplier = get_supplier(purchase_order.supplier_id)
        supplier.send_purchase_order(purchase_order)

        # Placeholder for Database operations

        return jsonify({
            'message': 'Backorder successfully placed',
            'purchase_order': {
                'id': purchase_order.purchase_order_id,
                'supplier_id': purchase_order.supplier_id,
                'order_date': purchase_order.order_date,
                'total_amount': purchase_order.total_amount,
                'payment_terms': purchase_order.payment_terms,
                'status': purchase_order.status
            }
        }), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500


def get_supplier(supplier_id):
    # TODO: Implement the logic to get a supplier instance based on the supplier_id
    # This is a placeholder and should be replaced with the actual implementation
    return Supplier(1, 'Supplier 1', '1234567890', "NET30")



"""
endpoint: /employee
method: GET
parameters: employee_id
response:

"""
def get_employee():
    try:
        employee_id = request.args.get('employee_id')
        if employee_id is None:
            raise ValueError('Employee ID is required')
        return Employee.get_employee_by_id(employee_id)
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

