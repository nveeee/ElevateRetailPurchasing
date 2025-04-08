from marshmallow import Schema, fields, post_load, validates, ValidationError
from app.database import db

class Inventory(db.Model):
    __tablename__ = 'Inventory'

    id = db.Column('Inventory_ID', db.Integer, primary_key=True)
    product_id = db.Column('Product_ID', db.Integer, db.ForeignKey('Product.Product_ID'), nullable=False)
    quantity = db.Column('Quantity', db.Integer, nullable=False)
    unit_price = db.Column('Unit_Price', db.Numeric(8, 2), nullable=False)
    deleted_at = db.Column('Deleted_At', db.DateTime, nullable=True)

    product = db.relationship('Product', backref='inventory_items', lazy=True)


class InventorySchema(Schema):
    id = fields.Int(dump_only=True)
    product_id = fields.Int(required=True)
    quantity = fields.Int(required=True)
    unit_price = fields.Decimal(required=True, places=2)
    deleted_at = fields.DateTime(required=False, allow_none=True)

    @validates("quantity")
    def validate_quantity(self, value):
        if value < 0:
            raise ValidationError("Quantity must be greater than or equal to 0.")

    @validates("unit_price")
    def validate_unit_price(self, value):
        if value < 0:
             raise ValidationError("Unit price must be greater than or equal to 0.")

    @post_load
    def make_inventory(self, data, **kwargs):
        return Inventory(**data)
