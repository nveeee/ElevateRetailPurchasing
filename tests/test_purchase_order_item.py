import pytest
from marshmallow import ValidationError
from app.schemas.purchase_order_item import PurchaseOrderItem, PurchaseOrderItemSchema


class TestPurchaseOrderItemClass:
    @pytest.fixture
    def valid_line_data(self):
        return {
            "product_id": 501,
            "quantity": 10,
            "unit_price": 25.99,
            "unit_total": 259.90
        }

    def test_line_creation(self, valid_line_data):
        line = PurchaseOrderItem(**valid_line_data)

        assert line.product_id == 501
        assert line.quantity == 10
        assert line.unit_price == 25.99
        assert line.unit_total == 259.90


class TestPurchaseOrderItemSchema:
    @pytest.fixture
    def schema(self):
        return PurchaseOrderItemSchema()

    @pytest.fixture
    def valid_data(self):
        return {
            "product_id": 502,
            "quantity": 5,
            "unit_price": 19.99,
            "unit_total": 99.95
        }

    def test_valid_data_loading(self, schema, valid_data):
        line = schema.load(valid_data)
        assert isinstance(line, PurchaseOrderItem)
        assert line.quantity == 5
        assert line.unit_total == 99.95

    def test_quantity_validation(self, schema, valid_data):
        # Test zero quantity
        invalid_data = valid_data.copy()
        invalid_data["quantity"] = 0
        with pytest.raises(ValidationError) as exc:
            schema.load(invalid_data)
        assert "greater than 0" in str(exc.value)

        # Test negative quantity
        invalid_data["quantity"] = -5
        with pytest.raises(ValidationError) as exc:
            schema.load(invalid_data)
        assert "greater than 0" in str(exc.value)

    def test_unit_price_validation(self, schema, valid_data):
        # Test zero price
        invalid_data = valid_data.copy()
        invalid_data["unit_price"] = 0.0
        with pytest.raises(ValidationError) as exc:
            schema.load(invalid_data)
        assert "greater than 0" in str(exc.value)

        # Test negative price
        invalid_data["unit_price"] = -10.0
        with pytest.raises(ValidationError) as exc:
            schema.load(invalid_data)
        assert "greater than 0" in str(exc.value)

    def test_unit_total_validation(self, schema, valid_data):
        # Test zero total
        invalid_data = valid_data.copy()
        invalid_data["unit_total"] = 0.0
        with pytest.raises(ValidationError) as exc:
            schema.load(invalid_data)
        assert "greater than 0" in str(exc.value)

        # Test negative total
        invalid_data["unit_total"] = -50.0
        with pytest.raises(ValidationError) as exc:
            schema.load(invalid_data)
        assert "greater than 0" in str(exc.value)

    def test_missing_required_fields(self, schema):
        incomplete_data = {
            "line_id": 3,
            "purchase_order_id": 1003,
            "product_id": 503
        }

        with pytest.raises(ValidationError) as exc:
            schema.load(incomplete_data)
        errors = exc.value.messages
        assert "quantity" in errors
        assert "unit_price" in errors
        assert "unit_total" in errors

    def test_data_types_validation(self, schema, valid_data):
        # Test invalid quantity type
        invalid_data = valid_data.copy()
        invalid_data["quantity"] = "five"
        with pytest.raises(ValidationError) as exc:
            schema.load(invalid_data)
        assert "Not a valid integer" in str(exc.value)

        # Test invalid unit_price type
        invalid_data = valid_data.copy()
        invalid_data["unit_price"] = "twenty"
        with pytest.raises(ValidationError) as exc:
            schema.load(invalid_data)
        assert "Not a valid number" in str(exc.value)
