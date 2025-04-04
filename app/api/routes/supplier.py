from flask import jsonify, request
from marshmallow import ValidationError

from .. import bp
from ...schemas import SupplierSchema
from ...schemas.supplier import Supplier

@bp.route('/create_supplier', methods=['POST'])
def create_supplier():
    try:
        schema = SupplierSchema()
        data = request.json

        supplier = schema.load(data)

        Supplier.save_to_db(supplier)

        # TODO: Redirect to homepage
    except ValidationError as err:
        return jsonify({'errors': err.messages}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500 