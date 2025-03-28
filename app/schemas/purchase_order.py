from marshmallow import Schema, fields, post_load, validates, ValidationError
from enum import Enum

class PaymentTerms(Enum):
    NET_30 = "NET_30"
    NET_60 = "NET_60"
    NET_90 = "NET_90"
    COD = "COD" # Cash On Delivery

class Status(Enum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    COMPLETED = "COMPLETED"

class PurchaseOrder:
    def __init__(self, purchase_order_id, order_date, total_amount, payment_terms, supplier_id, status):
        self.purchase_order_id = purchase_order_id
        self.order_date = order_date
        self.total_amount = total_amount
        self.payment_terms = payment_terms
        self.supplier_id = supplier_id
        self.status = status

class PurchaseOrderSchema(Schema):
    purchase_order_id = fields.Int(required=True)
    order_date = fields.Date(required=True)
    total_amount = fields.Float(required=True)
    payment_terms = fields.Str(required=True)
    supplier_id = fields.Int(required=True)
    status = fields.Str(required=True)

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

    @post_load
    def make_purchase_order(self, data, **kwargs):
        return PurchaseOrder(**data)
