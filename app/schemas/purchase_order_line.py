from marshmallow import Schema, fields, post_load


class PurchaseOrderLine:
    def __init__(self, line_id, purchase_order_id, product_id, quantity, unit_price, unit_total):
        self.line_id = line_id
        self.purchase_order_id = purchase_order_id
        self.product_id = product_id
        self.quantity = quantity
        self.unit_price = unit_price
        self.unit_total = unit_total

class PurchaseOrderLineSchema(Schema):
    line_id = fields.Int(required=True)
    purchase_order_id = fields.Int(required=True)
    product_id = fields.Int(required=True)
    quantity = fields.Int(required=True)
    unit_price = fields.Float(required=True)
    unit_total = fields.Float(required=True)


    @post_load
    def make_purchase_order_line(self, data, **kwargs):
        return PurchaseOrderLine(**data)
