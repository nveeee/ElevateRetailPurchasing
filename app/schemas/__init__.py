from .purchase_order import PurchaseOrderSchema
from .purchase_order_item import PurchaseOrderItemSchema
from .supplier import SupplierSchema
from .employee import EmployeeSchema
from .product import ProductSchema

from .enums import Status
from .enums import PaymentTerms

supplier_schema = SupplierSchema()
purchase_order_schema = PurchaseOrderSchema()
purchase_order_item_schema = PurchaseOrderItemSchema()
employee_schema = EmployeeSchema()
product_schema = ProductSchema()

status_enum = Status
payment_terms_enum = PaymentTerms

__all__ = ["SupplierSchema", "supplier_schema", "PurchaseOrderSchema", "purchase_order_schema",
           "PurchaseOrderItemSchema", "purchase_order_item_schema", "EmployeeSchema", "employee_schema",
           "Status", "status_enum", "PaymentTerms", "payment_terms_enum", "ProductSchema", "product_schema"]
