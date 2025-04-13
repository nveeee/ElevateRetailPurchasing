import os
from marshmallow import Schema, fields, post_load, validate

if (os.getenv('FLASK_ENV') == 'pos'):
    from src.utils.db_utils import db
else:
    from ..database import db


class Supplier(db.Model):
    __tablename__ = 'Supplier'

    id = db.Column('Supplier_ID', db.Integer, primary_key=True)
    supplier_name = db.Column('Supplier_Name', db.String(100), nullable=False)
    contact_name = db.Column('Contact_Name', db.String(255), nullable=False)
    contact_email = db.Column('Contact_Email', db.String(255), nullable=False)
    contact_phone = db.Column('Contact_Phone', db.String(255), nullable=False)

    purchase_orders = db.relationship('PurchaseOrder', backref='supplier', lazy=True)

    def send_purchase_order(self, purchase_order):
        try:
            # TODO: Implement supplier communication logic
            fake_supplier_response = {
                "order_id": "12345",
                "status": "Received",
                "estimated_delivery": "2025-12-31",
                "message": "Purchase order received and approved."
            }

            return fake_supplier_response
        except Exception as e:
            # TODO: Log the error
            raise Exception("Error while sending purchase order to supplier") from e

    @classmethod
    def save_to_db(cls, supplier):
        try:
            db.session.add(supplier)
            db.session.commit()
            return supplier
        except Exception as e:
            db.session.rollback()
            # TODO: Log the error saving to database
            raise Exception("Error while saving supplier to database") from e


class SupplierSchema(Schema):
    id = fields.Int(dump_only=True)
    supplier_name = fields.Str(required=True, validate=validate.Length(min=1, max=100))
    contact_name = fields.Str(required=True, validate=validate.Length(max=255))
    contact_email = fields.Str(required=True, validate=validate.Length(max=255))
    contact_phone = fields.Str(required=True, validate=validate.Length(max=255))

    @post_load
    def make_supplier(self, data, **kwargs):
        return Supplier(**data)
