from flask import jsonify, request
from marshmallow import ValidationError

from .. import bp
from ...schemas import SupplierSchema
from ...schemas.audit_trail import AuditTrail
from ...schemas.supplier import Supplier

@bp.route('/create_supplier', methods=['POST'])
def create_supplier():
    try:
        schema = SupplierSchema()
        data = request.json

        employee_id = data.pop('employee_id', None)
        supplier = schema.load(data)

        if employee_id:
            # Create audit trail
            audit_trail = AuditTrail(employee_id, "Supplier created")
            audit_trail.save_to_db()

        Supplier.save_to_db(supplier)

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