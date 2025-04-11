import os
from marshmallow import Schema, fields, post_load, validates, ValidationError
from .enums import PaymentTerms, Status
from datetime import datetime

if (os.getenv('FLASK_ENV') == 'pos'):
    from database import db
else:
    from ..database import db

from flask import current_app as app


class PurchaseOrder(db.Model):
    __tablename__ = 'Purchase_Order'

    id = db.Column('Purchase_Order_ID', db.Integer, primary_key=True)
    order_date = db.Column('Order_Date', db.Date, nullable=False, default=datetime.utcnow)
    supplier_id = db.Column(db.Integer, db.ForeignKey('Supplier.Supplier_ID'), nullable=False)
    status = db.Column('Status', db.String(20), nullable=False, default=Status.PENDING.value)

    line_items = db.relationship(
        'PurchaseOrderItem', back_populates='purchase_order', cascade='all, delete-orphan'
    )

    @classmethod
    def save_to_db(cls, purchase_order):
        try:
            db.session.add(purchase_order)
            db.session.commit()
            return purchase_order
        except Exception as e:
            db.session.rollback()
            app.logger.error(f"Error saving purchase order: {e}")


class PurchaseOrderSchema(Schema):
    id = fields.Int(dump_only=True)
    purchase_order_id = fields.Str(dump_only=True)
    order_date = fields.Date(required=True)
    total_amount = fields.Float(required=True)
    payment_terms = fields.Str(required=True)
    supplier_id = fields.Int(required=True)
    status = fields.Str(required=True)
    line_items = fields.List(fields.Nested('PurchaseOrderItemSchema'), required=False)

    @validates("status")
    def validate_status(self, value):
        valid_statuses = [e.value for e in Status]
        if value not in valid_statuses:
            raise ValidationError(f"Invalid status. Valid options are: {', '.join(valid_statuses)}")

    @validates("payment_terms")
    def validate_payment_terms(self, value):
        valid_terms = [e.value for e in PaymentTerms]
        if value not in valid_terms:
            raise ValidationError(
                f"Invalid payment terms. Valid options are: {', '.join(valid_terms)}"
            )

    @post_load
    def make_purchase_order(self, data, **kwargs):
        return PurchaseOrder(**data)
