from marshmallow import Schema, fields, post_load, validates, ValidationError
from app.database import db


class PurchaseOrderItem(db.Model):
    __tablename__ = 'purchase_order_items'

    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    purchase_order_id = db.Column(db.Integer, db.ForeignKey('purchase_orders.id'), nullable=True)
    quantity = db.Column(db.Integer, nullable=False)
    unit_cost = db.Column(db.Float, nullable=False)

    purchase_order = db.relationship('PurchaseOrder', back_populates='line_items')
    product = db.relationship('Product', backref='purchase_order_items')


class PurchaseOrderItemSchema(Schema):
    id = fields.Int(dump_only=True)
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
        return PurchaseOrderItem(**data)
