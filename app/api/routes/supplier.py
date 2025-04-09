from flask import jsonify, request
from marshmallow import ValidationError

from .. import bp
from ...schemas import SupplierSchema
from ...schemas.supplier import Supplier


@bp.route('/create_supplier', methods=['POST'])
def create_supplier():
    """
    Creates a new supplier using the provided JSON data.

    Request JSON:
        {
            "supplier_id": "1234",
            "supplier_name": "Supplier Name",
            "contact_name": "Contact Name",
            "contact_email": "supplier@example.com",
            "contact_phone": "123-456-7890",
            "payment_terms": "Payment Terms"
        }

    Returns:
        Response: A JSON response confirming successful supplier creation:
        {
            "message": "Supplier created successfully"
        }
        Validation Error: A JSON response with validation error messages if input data is invalid:
        {
            "errors": {
                "field_name": ["Error message 1", "Error message 2"]
            }
        }
        Error: A JSON response with a generic error message if an unexpected failure occurs.
    """
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
