import pytest
from marshmallow import ValidationError
from app.schemas.supplier import Supplier, SupplierSchema

class TestSupplierClass:
    @pytest.fixture
    def valid_supplier_data(self):
        return {
            "supplier_id": 501,
            "supplier_name": "Acme Corp",
            "contact_info": "contact@acme.com"
        }

    def test_supplier_creation(self, valid_supplier_data):
        supplier = Supplier(**valid_supplier_data)
        
        assert supplier.supplier_id == 501
        assert supplier.supplier_name == "Acme Corp"
        assert supplier.contact_info == "contact@acme.com"

class TestSupplierSchema:
    @pytest.fixture
    def schema(self):
        return SupplierSchema()

    @pytest.fixture
    def valid_data(self):
        return {
            "supplier_id": 502,
            "supplier_name": "Global Supplies",
            "contact_info": "support@globalsupplies.com"
        }

    def test_valid_data_loading(self, schema, valid_data):
        supplier = schema.load(valid_data)
        assert isinstance(supplier, Supplier)
        assert supplier.supplier_id == 502
        assert supplier.contact_info == "support@globalsupplies.com"

    def test_missing_required_fields(self, schema):
        incomplete_data = {
            "supplier_name": "Missing Fields Inc."
        }
        
        with pytest.raises(ValidationError) as exc:
            schema.load(incomplete_data)
        errors = exc.value.messages
        assert "supplier_id" in errors
        assert "contact_info" in errors

    def test_data_types_validation(self, schema, valid_data):
        # Test invalid supplier_id type
        invalid_data = valid_data.copy()
        invalid_data["supplier_id"] = "five-oh-two"
        with pytest.raises(ValidationError) as exc:
            schema.load(invalid_data)
        assert "Not a valid integer" in str(exc.value)

        # Test invalid contact_info type
        invalid_data = valid_data.copy()
        invalid_data["contact_info"] = 12345
        with pytest.raises(ValidationError) as exc:
            schema.load(invalid_data)
        assert "Not a valid string" in str(exc.value)

    def test_string_length_validations(self, schema, valid_data):
        # Test empty supplier_name
        invalid_data = valid_data.copy()
        invalid_data["supplier_name"] = ""
        with pytest.raises(ValidationError) as exc:
            schema.load(invalid_data)
        assert "Length must be between 1 and" in str(exc.value)

        # Test long contact_info
        invalid_data = valid_data.copy()
        invalid_data["contact_info"] = "a" * 256
        with pytest.raises(ValidationError) as exc:
            schema.load(invalid_data)
        assert "Longer than maximum length" in str(exc.value) 