from marshmallow import Schema, fields, post_load, validates, ValidationError


class PurchaseOrderLine:
    def __init__(self, product_id, quantity, unit_price, unit_total):
        self.product_id = product_id
        self.quantity = quantity
        self.unit_price = unit_price
        self.unit_total = unit_total

class PurchaseOrderLineSchema(Schema):
    product_id = fields.Int(required=True)
    quantity = fields.Int(required=True)
    unit_price = fields.Float(required=True)
    unit_total = fields.Float(required=True)

    @validates("quantity")
    def validate_quantity(self, value):
        if value <= 0:
            raise ValidationError("Quantity must be greater than 0")

    @validates("unit_price")
    def validate_unit_price(self, value):
        if value <= 0:
            raise ValidationError("Unit price must be greater than 0")

    @validates("unit_total")
    def validate_unit_total(self, value):
        if value <= 0:
            raise ValidationError("Unit total must be greater than 0")

    @post_load
    def make_purchase_order_line(self, data, **kwargs):
        return PurchaseOrderLine(**data)
