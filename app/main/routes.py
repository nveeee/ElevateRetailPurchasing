from flask import render_template, request, session
from . import bp
from ..schemas.product import Product
from ..schemas.supplier import Supplier

def get_products():
    """Get all products from the database with their supplier names"""
    products = []
    
    # Query all products with their suppliers, sorted by quantity
    product_list = Product.query.order_by(Product.quantity.asc()).all()
    
    for product in product_list:
        # Get the supplier name for each product
        supplier = Supplier.query.get(product.supplier_id)
        supplier_name = supplier.supplier_name if supplier else "Unknown Supplier"
        
        products.append({
            "product_id": product.product_id,
            "product_name": product.product_name,
            "unit_price": f"{product.unit_price:.2f}",
            "quantity": product.quantity,
            "supplier_name": supplier_name,
        })
    
    return products

@bp.route('/')
def index():
    return render_template('index.html', active_page='home')

@bp.route('/place_order')
def place_order():
    page = request.args.get('page', 1, type=int)
    per_page = 10
    products = get_products()  # Get products from database
    total = len(products)
    
    # Store in session for later access
    session['current_products'] = products[(page-1)*per_page : page*per_page]
    
    return render_template(
        'place_order.html',
        active_page='place_order',
        products=session['current_products'],
        current_page=page,
        total_pages=(total // per_page) + (1 if total % per_page else 0)
    )

@bp.route('/po_form', methods=['POST'])
def po_form():
    # Get IDs from hidden input
    selected_ids = [int(id) for id in request.form.get('selected_products').split(',') if id]
    
    # Get all products
    all_products = get_products()
    
    # Filter selected products from complete list
    selected_products = [
        p for p in all_products
        if p['product_id'] in selected_ids
    ]
    
    return render_template(
        'po_form.html',
        active_page='place_order',
        products=selected_products
    )
