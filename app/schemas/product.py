from marshmallow import Schema, fields, post_load, validates, ValidationError


class Product:
    def __init__(self, product_id, product_name, description, unit_price, quantity, supplier_id):
        self.product_id = product_id
        self.product_name = product_name
        self.description = description
        self.unit_price = unit_price
        self.quantity = quantity
        self.supplier_id = supplier_id

    @classmethod
    def get_supplier_id(cls, product_id):
        try:
            # TODO: Search database for product by id

            fake_product_response = {
                "product_id": 1,
                "product_name": "Product 1",
                "description": "Product description",
                "unit_price": 100.00,
                "quantity": 10,
                "supplier_id": 1
            }

            return fake_product_response.get("supplier_id")
        except Exception as e:
            raise e


class ProductSchema(Schema):
    product_id = fields.Int(required=True)
    product_name = fields.Str(required=True)
    description = fields.Str(required=True)
    unit_price = fields.Float(required=True)

    @validates("unit_price")
    def validate_unit_price(self, value):
        if value <= 0:
            raise ValidationError("Unit price must be greater than 0")


    @post_load
    def make_product(self, data, **kwargs):
        return Product(**data)
