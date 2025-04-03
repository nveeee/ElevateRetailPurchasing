from marshmallow import Schema, fields, post_load, validates, ValidationError
from .enums import PaymentTerms, Status

class PurchaseOrder:
    def __init__(self, order_date, total_amount, payment_terms, supplier_id, status, line_items, purchase_order_id=None):
        self.purchase_order_id = purchase_order_id
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
    purchase_order_id = fields.Str(dump_only=True)
    order_date = fields.Date(required=True)
    supplier_id = fields.Int(required=True)
    status = fields.Str(required=True)

    @validates("status")
    def validate_status(self, value):
        valid_statuses = [e.value for e in Status]
        if value not in valid_statuses:
            raise ValidationError(f"Invalid status. Valid options are: {', '.join(valid_statuses)}")

    @post_load
    def make_purchase_order(self, data, **kwargs):
        return PurchaseOrder(**data)
