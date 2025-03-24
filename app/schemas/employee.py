from typing import ClassVar

from marshmallow import Schema, fields, post_load, validates, ValidationError
import bcrypt
import uuid

class Employee:
    employee_db: ClassVar[dict] = {} #simulated in- memory user store, I hope it works.

#  the id is automatically generated.

    def __init__(self, first_name, last_name, email, password: str):
        self.employee_id = str(uuid.uuid4())
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password_hash = self._hash_password(password)
        Employee.employee_db[self.employee_id] = self

    @staticmethod
    def _hash_password(password: str) -> bytes:
        return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

    def verify_password(self, password: str) -> bool:
        return bcrypt.checkpw(password.encode("utf-8"), self.password_hash)

    @classmethod
    def get_employee_by_id(cls, employee_id: str) -> "Employee":
        return cls.employee_db.get(employee_id)


class EmployeeSchema(Schema):
    employee_id = fields.UUID(required=False, dump_only=True)
    first_name = fields.Str(required=True)
    last_name = fields.Str(required=True)
    email = fields.Email(required=True)
    password = fields.Str(required=True, load_only=True)

    @post_load
    def create_employee(self, data, **kwargs):
        return Employee(**data)

    @validates("password")
    def password_strength(self, value):
        if not any(char.isdigit() for char in value):
            raise ValidationError("Password must contain at least one number")
        if not any(char.isupper() for char in value):
            raise ValidationError("Password must contain at least one uppercase letter")
        if not any(char.islower() for char in value):
            raise ValidationError("Password must contain at least one lowercase letter")
        if not any(char in "!@#$%^&*()-_=+[]{}|;:'\",.<>?/" for char in value):
            raise ValidationError("Password must contain at least one special character")
        return value