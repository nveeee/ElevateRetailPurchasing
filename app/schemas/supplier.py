from flask import jsonify
from marshmallow import Schema, fields, post_load, validate, ValidationError, validates
from .enums import PaymentTerms

from app.schemas.purchase_order import PurchaseOrder

class Supplier:
    def __init__(self, supplier_id, supplier_name, contact_name, contact_email, contact_phone, payment_terms=PaymentTerms.NET_30.value):
        self.supplier_id = supplier_id
        self.supplier_name = supplier_name
        self.contact_name = contact_name
        self.contact_email = contact_email
        self.contact_phone = contact_phone
        self.payment_terms = payment_terms # Potential Addition, Ask Database

    def send_purchase_order(self, purchase_order: PurchaseOrder):
        try:
            # TODO: Implement supplier communication logic
            fake_supplier_response = {
                "order_id": "12345",
                "status": "APPROVED",
                "estimated_delivery": "2025-12-31",
                "message": "Purchase order received and approved."
            }

            return fake_supplier_response
        except Exception as e:
            # TODO: Log the error
            raise Exception("Error while sending purchase order to supplier") from e

    @classmethod
    def save_to_db(cls, supplier):
        try:
            # TODO: Save supplier to database

            fake_db_response = {
                "supplier_id": "12345",
                "supplier_name": "Supplier 1",
                "contact_name": "aaa@sdkndn",
                "contact_email": "bbb@sdkndn",
                "contact_phone": "1234567890",
                "payment_terms": "NET_30"
            }

            return fake_db_response
        except Exception as e:
            # TODO: Log the error saving to database
            raise Exception("Error while saving supplier to database") from e

    @classmethod
    def get_supplier_by_id(cls, supplier_id):
        # TODO: Implement the logic to get a supplier instance based on the supplier_id
        # This is a placeholder and should be replaced with the actual implementation
        return Supplier(1, 'Supplier 1', '1234567890', "NET30")


class SupplierSchema(Schema):
    supplier_id = fields.Int(required=True)
    supplier_name = fields.Str(required=True, validate=validate.Length(min=1, max=100))
    contact_name = fields.Str(required=True, validate=validate.Length(max=255))
    contact_email = fields.Str(required=True, validate=validate.Length(max=255))
    contact_phone = fields.Str(required=True, validate=validate.Length(max=255))
    payment_terms = fields.Str(required=True, validate=validate.Length(max=255))

    @validates("payment_terms")
    def validate_payment_terms(self, value):
        valid_terms = [e.value for e in PaymentTerms]
        if value not in valid_terms:
            raise ValidationError(f"Invalid payment terms. Valid options are: {', '.join(valid_terms)}")

    @post_load
    def make_supplier(self, data, **kwargs):
        return Supplier(**data)
