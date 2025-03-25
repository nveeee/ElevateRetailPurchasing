import pytest
from datetime import date
from marshmallow import ValidationError
from app.schemas.purchase_order import (
    PurchaseOrder,
    PurchaseOrderSchema,
    PaymentTerms,
    Status
)

class TestPurchaseOrderClass:
    @pytest.fixture
    def valid_po_data(self):
        return {
            "purchase_order_id": 1001,
            "order_date": date(2023, 1, 15),
            "total_amount": 1500.00,
            "payment_terms": PaymentTerms.NET_30.value,
            "supplier_id": 501,
            "status": Status.PENDING.value
        }

    def test_purchase_order_creation(self, valid_po_data):
        po = PurchaseOrder(**valid_po_data)
        
        assert po.purchase_order_id == 1001
        assert po.order_date == date(2023, 1, 15)
        assert po.total_amount == 1500.00
        assert po.payment_terms == PaymentTerms.NET_30.value
        assert po.supplier_id == 501
        assert po.status == Status.PENDING.value

class TestPurchaseOrderSchema:
    @pytest.fixture
    def schema(self):
        return PurchaseOrderSchema()

    @pytest.fixture
    def valid_data(self):
        return {
            "purchase_order_id": 1002,
            "order_date": "2023-01-20",
            "total_amount": 2000.50,
            "payment_terms": "NET_60",
            "supplier_id": 502,
            "status": "APPROVED"
        }

    def test_valid_data_loading(self, schema, valid_data):
        po = schema.load(valid_data)
        assert isinstance(po, PurchaseOrder)
        assert po.purchase_order_id == 1002
        assert po.order_date == date(2023, 1, 20)
        assert po.total_amount == 2000.50

    def test_invalid_payment_terms(self, schema, valid_data):
        invalid_data = valid_data.copy()
        invalid_data["payment_terms"] = "INVALID_TERM"
        
        with pytest.raises(ValidationError) as exc:
            schema.load(invalid_data)
        assert "Invalid payment terms" in str(exc.value)

    def test_invalid_status_value(self, schema, valid_data):
        invalid_data = valid_data.copy()
        invalid_data["status"] = "INVALID_STATUS"
        
        with pytest.raises(ValidationError) as exc:
            schema.load(invalid_data)
        assert "Invalid status" in str(exc.value)

    def test_missing_required_fields(self, schema):
        incomplete_data = {
            "order_date": "2023-01-20",
            "total_amount": 2000.50
        }
        
        with pytest.raises(ValidationError) as exc:
            schema.load(incomplete_data)
        errors = exc.value.messages
        assert "purchase_order_id" in errors
        assert "payment_terms" in errors
        assert "supplier_id" in errors
        assert "status" in errors

    def test_data_types_validation(self, schema, valid_data):
        # Test invalid ID type
        invalid_data = valid_data.copy()
        invalid_data["purchase_order_id"] = "invalid_id"
        
        with pytest.raises(ValidationError) as exc:
            schema.load(invalid_data)
        assert "Not a valid integer" in str(exc.value)

        # Test invalid date format
        invalid_data = valid_data.copy()
        invalid_data["order_date"] = "20-01-2023"
        
        with pytest.raises(ValidationError) as exc:
            schema.load(invalid_data)
        assert "Not a valid date" in str(exc.value)

    def test_negative_total_amount(self, schema, valid_data):
        invalid_data = valid_data.copy()
        invalid_data["total_amount"] = -100.00
        
        with pytest.raises(ValidationError) as exc:
            schema.load(invalid_data)
        assert "greater than or equal to 0" in str(exc.value) 