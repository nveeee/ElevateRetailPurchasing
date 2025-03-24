from flask import jsonify, request
from marshmallow import ValidationError

from . import bp
from app.schemas.supplier import SupplierSchema

@bp.route('/order', methods=['POST'])
def place_order():
    return jsonify({'message': 'Order placed'})

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
                'contact': supplier.contact_info
            }
        }), 201
    except ValidationError as err:
        return jsonify({'errors': err.messages}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500
