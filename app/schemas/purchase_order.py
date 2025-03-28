from marshmallow import Schema, fields, post_load, validates, ValidationError
from .enums import PaymentTerms, Status

class PurchaseOrder:
    def __init__(self, order_date, total_amount, payment_terms, supplier_id, status, line_items):
        self.order_date = order_date
        self.total_amount = total_amount
        self.payment_terms = payment_terms
        self.supplier_id = supplier_id
        self.status = status
        self.line_items = line_items


    @classmethod
    def save_to_db(cls, purchase_order):
        try:
            # TODO: Save purchase order to database

            fake_db_response = {
                "purchase_order_id": "12345",
                "order_date": "2025-12-31",
                "total_amount": 1000.00,
                "payment_terms": "Net_30",
                "supplier_id": 1,
                "status": "APPROVED"
            }

            return fake_db_response
        except Exception as e:
            # TODO: Log the error saving to database
            # Do NOT raise error. Purchase Order was successfully placed.
            pass


class PurchaseOrderSchema(Schema):
    order_date = fields.Date(required=True)
    total_amount = fields.Float(required=True)
    payment_terms = fields.Str(required=True)
    supplier_id = fields.Int(required=True)
    status = fields.Str(required=True)
    line_items = fields.Nested('PurchaseOrderLineSchema', many=True, required=True)

    @validates("payment_terms")
    def validate_payment_terms(self, value):
        valid_terms = [e.value for e in PaymentTerms]
        if value not in valid_terms:
            raise ValidationError(f"Invalid payment terms. Valid options are: {', '.join(valid_terms)}")

    @validates("status")
    def validate_status(self, value):
        valid_statuses = [e.value for e in Status]
        if value not in valid_statuses:
            raise ValidationError(f"Invalid status. Valid options are: {', '.join(valid_statuses)}")

    @validates("total_amount")
    def validate_total_amount(self, value):
        if value < 0:
            raise ValidationError("Must be greater than or equal to 0")

    @validates('line_items')
    def validate_line_items(self, value):
        if not value:
            raise ValidationError("At least one line item is required")

    @post_load
    def make_purchase_order(self, data, **kwargs):
        return PurchaseOrder(**data)
