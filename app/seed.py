import random
from faker import Faker
from app import create_app, db
from app.schemas.supplier import Supplier
from app.schemas.product import Product
from app.schemas.purchase_order import PurchaseOrder
from app.schemas.purchase_order_item import PurchaseOrderItem
from app.schemas.enums import PaymentTerms, Status

fake = Faker()


def seed_suppliers(count=10):
    """Seed the database with fake suppliers"""
    suppliers = []
    for i in range(1, count + 1):
        supplier = Supplier(
            supplier_id=i,
            supplier_name=fake.company(),
            contact_name=fake.name(),
            contact_email=fake.email(),
            contact_phone=fake.phone_number(),
            payment_terms=random.choice([term.value for term in PaymentTerms])
        )
        suppliers.append(supplier)

    db.session.add_all(suppliers)
    db.session.commit()
    print(f"Added {count} suppliers")
    return suppliers


def seed_products(count=50):
    """Seed the database with fake products"""
    # Get all supplier IDs
    supplier_ids = [s.id for s in Supplier.query.all()]
    if not supplier_ids:
        print("No suppliers found. Please seed suppliers first.")
        return []

    products = []
    categories = ["Electronics", "Clothing", "Food", "Furniture", "Books", "Tools"]

    for i in range(1, count + 1):
        product = Product(
            product_id=i,
            product_name=fake.catch_phrase(),
            description=fake.paragraph(),
            unit_price=round(random.uniform(10.0, 1000.0), 2),
            quantity=random.randint(0, 100),
            category_id=random.randint(1, len(categories)),
            supplier_id=random.choice(supplier_ids)
        )
        products.append(product)

    db.session.add_all(products)
    db.session.commit()
    print(f"Added {count} products")
    return products


def seed_purchase_orders(count=20):
    """Seed the database with fake purchase orders"""
    # Get all supplier IDs
    supplier_ids = [s.id for s in Supplier.query.all()]
    if not supplier_ids:
        print("No suppliers found. Please seed suppliers first.")
        return []

    purchase_orders = []

    for i in range(1, count + 1):
        order_date = fake.date_between(start_date='-1y', end_date='today')
        po = PurchaseOrder(
            purchase_order_id=f"PO-{fake.random_number(digits=5)}",
            order_date=order_date,
            total_amount=0,  # Will be calculated after adding line items
            payment_terms=random.choice([term.value for term in PaymentTerms]),
            supplier_id=random.choice(supplier_ids),
            status=random.choice([status.value for status in Status])
        )
        purchase_orders.append(po)

    db.session.add_all(purchase_orders)
    db.session.commit()
    print(f"Added {count} purchase orders")
    return purchase_orders


def seed_purchase_order_item(min_lines=1, max_lines=5):
    """Seed the database with fake purchase order lines"""
    # Get all purchase order IDs
    po_ids = [po.id for po in PurchaseOrder.query.all()]
    if not po_ids:
        print("No purchase orders found. Please seed purchase orders first.")
        return []

    # Get all product IDs
    product_ids = [p.id for p in Product.query.all()]
    if not product_ids:
        print("No products found. Please seed products first.")
        return []

    purchase_order_item = []

    for po_id in po_ids:
        # Generate random number of line items for each purchase order
        num_lines = random.randint(min_lines, max_lines)
        po_total = 0

        for _ in range(num_lines):
            product = Product.query.get(random.choice(product_ids))
            quantity = random.randint(1, 10)
            unit_cost = product.unit_price
            line_total = quantity * unit_cost

            po_line = PurchaseOrderItem(
                product_id=product.id,
                purchase_order_id=po_id,
                quantity=quantity,
                unit_cost=unit_cost
            )
            purchase_order_item.append(po_line)
            po_total += line_total

        # Update the purchase order's total amount
        po = PurchaseOrder.query.get(po_id)
        po.total_amount = po_total

    db.session.add_all(purchase_order_item)
    db.session.commit()
    print(f"Added purchase order lines to {len(po_ids)} purchase orders")
    return purchase_order_item


def seed_all():
    """Seed all tables with fake data"""
    print("Starting database seeding...")

    # Clear existing data
    PurchaseOrderItem.query.delete()
    PurchaseOrder.query.delete()
    Product.query.delete()
    Supplier.query.delete()
    db.session.commit()

    # Seed tables
    seed_suppliers(10)
    seed_products(50)
    seed_purchase_orders(20)
    seed_purchase_order_item(1, 5)

    print("Database seeding completed!")


if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        seed_all()
