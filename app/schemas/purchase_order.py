from marshmallow import Schema, fields, post_load
from enum import Enum

class PaymentTerms(Enum):
    NET_30 = "NET_30"
    NET_60 = "NET_60"
    NET_90 = "NET_90"
    COD = "COD"

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
    payment_terms = fields.Str(required=True, validate=lambda x: x in [e.value for e in PaymentTerms])
    supplier_id = fields.Int(required=True)
    status = fields.Str(required=True, validate=lambda x: x in [e.value for e in Status])

    @post_load
    def make_purchase_order(self, data, **kwargs):
        return PurchaseOrder(**data)
