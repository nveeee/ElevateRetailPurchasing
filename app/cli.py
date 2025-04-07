import click
from app.seed import seed_all, seed_suppliers, seed_products, seed_purchase_orders, seed_purchase_order_item

def register_commands(app):
    """Register CLI commands for the application"""
    
    @app.cli.command('seed-db')
    @click.option('--suppliers', default=10, help='Number of suppliers to create')
    @click.option('--products', default=50, help='Number of products to create')
    @click.option('--orders', default=20, help='Number of purchase orders to create')
    @click.option('--min-lines', default=1, help='Minimum number of lines per purchase order')
    @click.option('--max-lines', default=5, help='Maximum number of lines per purchase order')
    @click.option('--all', is_flag=True, help='Seed all tables with default values')
    def seed_database(suppliers, products, orders, min_lines, max_lines, all):
        """Seed the database with fake data."""
        if all:
            seed_all()
        else:
            # Clear existing data
            from app.schemas.purchase_order_item import PurchaseOrderItem
            from app.schemas.purchase_order import PurchaseOrder
            from app.schemas.product import Product
            from app.schemas.supplier import Supplier
            from app import db
            
            PurchaseOrderItem.query.delete()
            PurchaseOrder.query.delete()
            Product.query.delete()
            Supplier.query.delete()
            db.session.commit()
            
            seed_suppliers(suppliers)
            seed_products(products)
            seed_purchase_orders(orders)
            seed_purchase_order_item(min_lines, max_lines)
