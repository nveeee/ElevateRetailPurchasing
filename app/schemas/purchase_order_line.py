from marshmallow import Schema, fields, post_load, validates, ValidationError


class PurchaseOrderLine:
    def __init__(self, product_id, quantity, unit_cost, purchase_order_id=None):
        self.product_id = product_id
        self.purchase_order_id = purchase_order_id
        self.quantity = quantity
        self.unit_cost = unit_cost

class PurchaseOrderLineSchema(Schema):
    purchase_order_id = fields.Int(dump_only=True)
    product_id = fields.Int(required=True)
    quantity = fields.Int(required=True)
    unit_cost = fields.Float(required=True)

    @validates("quantity")
    def validate_quantity(self, value):
        if value <= 0:
            raise ValidationError("Quantity must be greater than 0")

    @validates("unit_cost")
    def validate_unit_cost(self, value):
        if value <= 0:
            raise ValidationError("Unit cost must be greater than 0")

    @post_load
    def make_purchase_order_line(self, data, **kwargs):
        return PurchaseOrderLine(**data)
