from marshmallow import Schema, fields, post_load, validates, ValidationError
from app.database import db


class Product(db.Model):
    __tablename__ = 'Product'

    id = db.Column('Product_ID', db.Integer, primary_key=True)
    product_name = db.Column('Name', db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    category_id = db.Column(db.Integer, nullable=True)
    supplier_id = db.Column(db.Integer, db.ForeignKey('Supplier.Supplier_ID'), nullable=False)

    supplier = db.relationship('Supplier', backref='products')

    
    @classmethod
    def get_supplier_id(cls, product_id):
        try:
            product = cls.query.filter_by(id=product_id).first()
            if product:
                return product.supplier_id
            return None
        except Exception as e:
            raise e

    @classmethod
    def get_product_by_id(cls, pid):
        return cls.query.filter_by(id=pid).first()


class ProductSchema(Schema):
    id = fields.Int(dump_only=True)
    product_id = fields.Int(required=True)
    product_name = fields.Str(required=True)
    description = fields.Str(required=True)
    category_id = fields.Int(required=True)
    supplier_id = fields.Int(required=True)

    @post_load
    def make_product(self, data, **kwargs):
        return Product(**data)
