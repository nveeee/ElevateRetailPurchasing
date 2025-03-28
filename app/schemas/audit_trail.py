from xmlrpc.client import DateTime
from datetime import datetime
from marshmallow import Schema, fields, post_load, validate, ValidationError, validates
from enum import Enum

class AuditTrail:
    def __init__(self, employee_id: int, action: str):
        self.employee_id = employee_id
        self.action = action
        self.timestamp = datetime.now()



class AuditTrailSchema(Schema):
    employee_id = fields.Int(required=True)
    action = fields.Str(required=True)
    audit_trail_id = fields.Int(required=True)
    timestamp = fields.DateTime(required=True)

    @post_load
    def make_audit_trail(self, data, **kwargs):
        return AuditTrail(**data)
