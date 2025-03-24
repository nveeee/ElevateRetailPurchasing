from marshmallow import Schema, fields, post_load

class Supplier:
    def __init__(self, supplier_id, supplier_name, contact_info):
        self.supplier_id = supplier_id
        self.supplier_name = supplier_name
        self.contact_info = contact_info

class SupplierSchema(Schema):
    supplier_id = fields.Int(required=True)
    supplier_name = fields.Str(required=True)
    contact_info = fields.Str(required=True)

    @post_load
    def make_supplier(self, data, **kwargs):
        return Supplier(**data)
