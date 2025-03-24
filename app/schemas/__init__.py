from .purchase_order import PurchaseOrderSchema
from .purchase_order_line import PurchaseOrderLineSchema
from .supplier import SupplierSchema
from .employee import EmployeeSchema

supplier_schema = SupplierSchema()
purchase_order_schema = PurchaseOrderSchema()
purchase_order_line_schema = PurchaseOrderLineSchema()
employee_schema = EmployeeSchema()

__all__ = ["SupplierSchema", "supplier_schema", "PurchaseOrderSchema", "purchase_order_schema",
           "PurchaseOrderLineSchema", "purchase_order_line_schema", "EmployeeSchema", "employee_schema"]
