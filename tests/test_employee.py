import pytest
from marshmallow import ValidationError
from app.schemas.employee import Employee, EmployeeSchema


class TestEmployeeClass:
    @pytest.fixture
    def sample_employee(self):
        return Employee(
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com",
            password="SecurePass123!"
        )

    def test_employee_creation(self, sample_employee):
        assert sample_employee.first_name == "John"
        assert sample_employee.last_name == "Doe"
        assert sample_employee.email == "john.doe@example.com"
        assert isinstance(sample_employee.password_hash, bytes)

    def test_password_hashing(self, sample_employee):
        assert sample_employee.verify_password("SecurePass123!") is True
        assert sample_employee.verify_password("wrongpassword") is False


class TestEmployeeSchema:
    @pytest.fixture
    def schema(self):
        return EmployeeSchema()

    @pytest.fixture
    def valid_data(self):
        return {
            "first_name": "Alice",
            "last_name": "Smith",
            "email": "alice@example.com",
            "password": "ValidPass123!"
        }

    def test_valid_data_loading(self, schema, valid_data):
        employee = schema.load(valid_data)
        assert isinstance(employee, Employee)
        assert employee.first_name == "Alice"
        assert employee.last_name == "Smith"

    def test_password_validation_rules(self, schema, valid_data):
        # Test missing number
        with pytest.raises(ValidationError) as exc:
            invalid_data = valid_data.copy()
            invalid_data["password"] = "WeakPassword!"
            schema.load(invalid_data)
        assert "must contain at least one number" in str(exc.value)

        # Test missing uppercase
        with pytest.raises(ValidationError) as exc:
            invalid_data = valid_data.copy()
            invalid_data["password"] = "lowercase123!"
            schema.load(invalid_data)
        assert "uppercase letter" in str(exc.value)

        # Test missing lowercase
        with pytest.raises(ValidationError) as exc:
            invalid_data = valid_data.copy()
            invalid_data["password"] = "UPPERCASE123!"
            schema.load(invalid_data)
        assert "lowercase letter" in str(exc.value)

        # Test missing special character
        with pytest.raises(ValidationError) as exc:
            invalid_data = valid_data.copy()
            invalid_data["password"] = "NoSpecial123"
            schema.load(invalid_data)
        assert "special character" in str(exc.value)

    def test_password_field_not_in_output(self, schema, valid_data):
        employee = schema.load(valid_data)
        result = schema.dump(employee)
        assert "password" not in result
