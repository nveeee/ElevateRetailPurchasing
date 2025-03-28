import pytest
from marshmallow import ValidationError
from app.schemas.supplier import (
    Supplier,
    SupplierSchema,
    PaymentTerms
)
import json
from unittest.mock import patch

class TestSupplierClass:
    @pytest.fixture
    def valid_supplier_data(self):
        return {
            "supplier_id": 501,
            "supplier_name": "Acme Corp",
            "contact_info": "contact@acme.com",
            "payment_terms": PaymentTerms.NET_30.value
        }

    def test_supplier_creation(self, valid_supplier_data):
        supplier = Supplier(**valid_supplier_data)
        
        assert supplier.supplier_id == 501
        assert supplier.supplier_name == "Acme Corp"
        assert supplier.contact_info == "contact@acme.com"
        assert supplier.payment_terms == PaymentTerms.NET_30.value

class TestSupplierSchema:
    @pytest.fixture
    def schema(self):
        return SupplierSchema()

    @pytest.fixture
    def valid_data(self):
        return {
            "supplier_id": 502,
            "supplier_name": "Global Supplies",
            "contact_info": "support@globalsupplies.com",
            "payment_terms": "NET_60"
        }

    def test_valid_data_loading(self, schema, valid_data):
        supplier = schema.load(valid_data)
        assert isinstance(supplier, Supplier)
        assert supplier.supplier_id == 502
        assert supplier.contact_info == "support@globalsupplies.com"

    def test_invalid_payment_terms(self, schema, valid_data):
        invalid_data = valid_data.copy()
        invalid_data["payment_terms"] = "INVALID_TERM"

        with pytest.raises(ValidationError) as exc:
            schema.load(invalid_data)
        assert "Invalid payment terms" in str(exc.value)

    def test_missing_required_fields(self, schema):
        incomplete_data = {
            "supplier_name": "Missing Fields Inc."
        }
        
        with pytest.raises(ValidationError) as exc:
            schema.load(incomplete_data)
        errors = exc.value.messages
        assert "supplier_id" in errors
        assert "contact_info" in errors
        assert "payment_terms" in errors

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

class TestSupplierEndpoint:
    @pytest.fixture
    def client(self):
        from app import create_app
        app = create_app()
        app.config['TESTING'] = True
        with app.test_client() as client:
            yield client

    @pytest.fixture
    def valid_supplier_data(self):
        return {
            "supplier_id": 503,
            "supplier_name": "Test Supplier",
            "contact_info": "test@example.com"
        }

    def test_successful_supplier_creation(self, client, valid_supplier_data):
        response = client.post(
            '/api/create_supplier',
            data=json.dumps(valid_supplier_data),
            content_type='application/json'
        )
        
        assert response.status_code == 201
        data = json.loads(response.data)
        assert data['message'] == 'Supplier created'
        assert data['supplier']['id'] == 503
        assert data['supplier']['name'] == "Test Supplier"
        # Add database assertion here when implemented

    def test_create_supplier_missing_required_fields(self, client, valid_supplier_data):
        test_cases = [
            ({'supplier_name': 'Missing ID', 'contact_info': 'test@test.com'}, 'supplier_id'),
            ({'supplier_id': 504, 'contact_info': 'test@test.com'}, 'supplier_name'),
            ({'supplier_id': 505, 'supplier_name': 'Missing Contact'}, 'contact_info')
        ]
        
        for data, missing_field in test_cases:
            response = client.post(
                '/api/create_supplier',
                data=json.dumps(data),
                content_type='application/json'
            )
            assert response.status_code == 400
            errors = json.loads(response.data)['errors']
            assert missing_field in errors
            assert 'Missing data for required field' in errors[missing_field][0]

    def test_create_supplier_invalid_data_types(self, client, valid_supplier_data):
        invalid_data = valid_supplier_data.copy()
        invalid_data['supplier_id'] = "not-an-integer"
        
        response = client.post(
            '/api/create_supplier',
            data=json.dumps(invalid_data),
            content_type='application/json'
        )
        
        assert response.status_code == 400
        errors = json.loads(response.data)['errors']
        assert 'supplier_id' in errors
        assert 'Not a valid integer' in errors['supplier_id'][0]

    def test_create_supplier_length_validations(self, client, valid_supplier_data):
        # Test empty supplier_name
        invalid_data = valid_supplier_data.copy()
        invalid_data['supplier_name'] = ""
        
        response = client.post(
            '/api/create_supplier',
            data=json.dumps(invalid_data),
            content_type='application/json'
        )
        assert response.status_code == 400
        errors = json.loads(response.data)['errors']
        assert 'supplier_name' in errors
        assert 'Length must be between' in errors['supplier_name'][0]

        # Test long contact_info
        invalid_data = valid_supplier_data.copy()
        invalid_data['contact_info'] = 'a' * 256
        
        response = client.post(
            '/api/create_supplier',
            data=json.dumps(invalid_data),
            content_type='application/json'
        )
        assert response.status_code == 400
        errors = json.loads(response.data)['errors']
        assert 'contact_info' in errors
        assert 'Longer than maximum length' in errors['contact_info'][0]

    def test_server_error_handling(self, client, valid_supplier_data):
        with patch('app.api.routes.SupplierSchema.load') as mock_load:
            mock_load.side_effect = Exception('DB error')
            
            response = client.post(
                '/api/create_supplier',
                data=json.dumps(valid_supplier_data),
                content_type='application/json'
            )
            
            assert response.status_code == 500
            data = json.loads(response.data)
            assert 'error' in data
            assert 'DB error' in data['error'] 