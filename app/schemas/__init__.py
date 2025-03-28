from .purchase_order import PurchaseOrderSchema
from .purchase_order_line import PurchaseOrderLineSchema
from .supplier import SupplierSchema
from .employee import EmployeeSchema
from .product import ProductSchema

from .enums import Status
from .enums import PaymentTerms

supplier_schema = SupplierSchema()
purchase_order_schema = PurchaseOrderSchema()
purchase_order_line_schema = PurchaseOrderLineSchema()
employee_schema = EmployeeSchema()
product_schema = ProductSchema()

status_enum = Status
payment_terms_enum = PaymentTerms

__all__ = ["SupplierSchema", "supplier_schema", "PurchaseOrderSchema", "purchase_order_schema",
           "PurchaseOrderLineSchema", "purchase_order_line_schema", "EmployeeSchema", "employee_schema",
           "Status", "status_enum", "PaymentTerms", "payment_terms_enum", "ProductSchema", "product_schema"]
