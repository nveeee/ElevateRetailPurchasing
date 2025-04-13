import os
from marshmallow import Schema, fields, post_load, validates, ValidationError

if (os.getenv('FLASK_ENV') == 'pos'):
    from src.utils.db_utils import db
else:
    from ..database import db


class PurchaseOrderItem(db.Model):
    __tablename__ = 'Purchase_Order_Item'

    id = db.Column('Purchase_Order_Item_ID', db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('Product.Product_ID'), nullable=False)
    purchase_order_id = db.Column(
        db.Integer, db.ForeignKey('Purchase_Order.Purchase_Order_ID'), nullable=True
    )
    quantity = db.Column('Quantity', db.Integer, nullable=False)

    purchase_order = db.relationship('PurchaseOrder', back_populates='line_items')
    product = db.relationship('Product', backref='purchase_order_items')


class PurchaseOrderItemSchema(Schema):
    id = fields.Int(dump_only=True)
    purchase_order_id = fields.Int(dump_only=True)
    product_id = fields.Int(required=True)
    quantity = fields.Int(required=True)

    @validates("quantity")
    def validate_quantity(self, value):
        if value <= 0:
            raise ValidationError("Quantity must be greater than 0")

    @post_load
    def make_purchase_order_line(self, data, **kwargs):
        return PurchaseOrderItem(**data)
