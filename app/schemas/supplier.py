from marshmallow import Schema, fields, post_load, validate, ValidationError, validates
from .enums import PaymentTerms

from app.database import db

class Supplier(db.Model):
    __tablename__ = 'suppliers'
    
    id = db.Column(db.Integer, primary_key=True)
    supplier_id = db.Column(db.Integer, unique=True, nullable=False)
    supplier_name = db.Column(db.String(100), nullable=False)
    contact_name = db.Column(db.String(255), nullable=False)
    contact_email = db.Column(db.String(255), nullable=False)
    contact_phone = db.Column(db.String(255), nullable=False)
    payment_terms = db.Column(db.String(255), default=PaymentTerms.NET_30.value)

    purchase_orders = db.relationship('PurchaseOrder', backref='supplier', lazy=True)

    def send_purchase_order(self, purchase_order):
        try:
            # TODO: Implement supplier communication logic
            fake_supplier_response = {
                "order_id": "12345",
                "status": "APPROVED",
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
    supplier_id = fields.Int(required=True)
    supplier_name = fields.Str(required=True, validate=validate.Length(min=1, max=100))
    contact_name = fields.Str(required=True, validate=validate.Length(max=255))
    contact_email = fields.Str(required=True, validate=validate.Length(max=255))
    contact_phone = fields.Str(required=True, validate=validate.Length(max=255))
    payment_terms = fields.Str(required=True, validate=validate.Length(max=255))

    @validates("payment_terms")
    def validate_payment_terms(self, value):
        valid_terms = [e.value for e in PaymentTerms]
        if value not in valid_terms:
            raise ValidationError(f"Invalid payment terms. Valid options are: {', '.join(valid_terms)}")

    @post_load
    def make_supplier(self, data, **kwargs):
        return Supplier(**data)