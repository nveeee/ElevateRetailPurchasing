from flask import jsonify
from marshmallow import Schema, fields, post_load, validate, ValidationError, validates
from enum import Enum

class PaymentTerms(Enum):
    NET_30 = "NET_30"
    NET_60 = "NET_60"
    NET_90 = "NET_90"
    COD = "COD" # Cash On Delivery

class Supplier:
    def __init__(self, supplier_id, supplier_name, contact_info, payment_terms):
        self.supplier_id = supplier_id
        self.supplier_name = supplier_name
        self.contact_info = contact_info
        self.payment_terms = payment_terms

    def send_purchase_order(self, purchase_order):
        # TODO: Implement supplier communication logic
        print("Sending fake purchase order..")  # Temporary  placeholder
        return jsonify({
            'message': "Purchase order sent successfully",
            'status': 'APPROVED'
        }), 201

class SupplierSchema(Schema):
    supplier_id = fields.Int(required=True)
    supplier_name = fields.Str(required=True, validate=validate.Length(min=1, max=100))
    contact_info = fields.Str(required=True, validate=validate.Length(max=255))
    payment_terms = fields.Str(required=True, validate=validate.Length(max=255))

    @validates("payment_terms")
    def validate_payment_terms(self, value):
        valid_terms = [e.value for e in PaymentTerms]
        if value not in valid_terms:
            raise ValidationError(f"Invalid payment terms. Valid options are: {', '.join(valid_terms)}")

    @post_load
    def make_supplier(self, data, **kwargs):
        return Supplier(**data)
