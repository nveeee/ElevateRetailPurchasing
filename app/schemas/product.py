from marshmallow import Schema, fields, post_load, validates, ValidationError
from app.database import db


class Product(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, unique=True, nullable=False)
    product_name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    unit_price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=0)
    category_id = db.Column(db.Integer, nullable=True)
    supplier_id = db.Column(db.Integer, db.ForeignKey('suppliers.id'), nullable=False)

    supplier = db.relationship('Supplier', backref='products')

    
    @classmethod
    def get_supplier_id(cls, product_id):
        try:
            product = cls.query.filter_by(product_id=product_id).first()
            if product:
                return product.supplier_id
            return None
        except Exception as e:
            raise e

    @classmethod
    def get_product_by_id(cls, pid):
        return cls.query.filter_by(product_id=pid).first()


class ProductSchema(Schema):
    id = fields.Int(dump_only=True)
    product_id = fields.Int(required=True)
    product_name = fields.Str(required=True)
    description = fields.Str(required=True)
    unit_price = fields.Float(required=True)
    quantity = fields.Int(required=True)
    category_id = fields.Int(required=True)
    supplier_id = fields.Int(required=True)

    @validates("unit_price")
    def validate_unit_price(self, value):
        if value <= 0:
            raise ValidationError("Unit price must be greater than 0")


    @post_load
    def make_product(self, data, **kwargs):
        return Product(**data)
