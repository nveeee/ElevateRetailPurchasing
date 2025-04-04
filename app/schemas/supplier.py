from marshmallow import Schema, fields, post_load, validate, ValidationError, validates
from sqlalchemy import Column, Integer, String, Enum
from .enums import PaymentTerms
from app.schemas.purchase_order import PurchaseOrder
from app.database import Base, SessionLocal

class Supplier(Base):
    __tablename__ = 'suppliers'

    supplier_id = Column(Integer, primary_key=True)
    supplier_name = Column(String(100), nullable=False)
    contact_name = Column(String(255), nullable=False)
    contact_email = Column(String(255), nullable=False)
    contact_phone = Column(String(255), nullable=False)
    payment_terms = Column(Enum(PaymentTerms), nullable=False, default=PaymentTerms.NET_30.value)

    def __init__(self, supplier_name, contact_name, contact_email, contact_phone, payment_terms=PaymentTerms.NET_30.value, supplier_id=None):
        self.supplier_id = supplier_id
        self.supplier_name = supplier_name
        self.contact_name = contact_name
        self.contact_email = contact_email
        self.contact_phone = contact_phone
        self.payment_terms = payment_terms

    def send_purchase_order(self, purchase_order: PurchaseOrder):
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
            raise Exception("Error while sending purchase order to supplier") from e

    @classmethod
    def save_to_db(cls, supplier):
        try:
            db = SessionLocal()
            db.add(supplier)
            db.commit()
            db.refresh(supplier)
            return supplier
        except Exception as e:
            db.rollback()
            raise Exception("Error while saving supplier to database") from e
        finally:
            db.close()

    @classmethod
    def get_supplier_by_id(cls, supplier_id):
        db = SessionLocal()
        try:
            return db.query(cls).filter(cls.supplier_id == supplier_id).first()
        except Exception as e:
            raise Exception("Error while fetching supplier from database") from e
        finally:
            db.close()

class SupplierSchema(Schema):
    supplier_id = fields.Int(dump_only=True)  # read-only field
    supplier_name = fields.Str(required=True, validate=validate.Length(min=1, max=100))
    contact_name = fields.Str(required=True, validate=validate.Length(max=255))
    contact_email = fields.Str(required=True, validate=validate.Length(max=255))
    contact_phone = fields.Str(required=True, validate=validate.Length(max=255))
    payment_terms = fields.Str(required=True, validate=validate.Length(max=50))

    @validates('payment_terms')
    def validate_payment_terms(self, value):
        try:
            PaymentTerms(value)
        except ValueError as e:
            raise ValidationError(f"Invalid payment terms: {value}")

    @post_load
    def make_supplier(self, data, **kwargs):
        return Supplier(**data)
