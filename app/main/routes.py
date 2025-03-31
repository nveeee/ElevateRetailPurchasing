from flask import render_template, request, session
from . import bp

def get_fake_products():
    # Mock database query returning product data
    return [
        {
            "product_id": i,
            "product_name": f"Product {i}",
            "unit_price": f"{(i * 5 + 10):.2f}",
            "quantity": 50 * i,
            "supplier_name": f"Supplier {chr(65 + (i % 3))}",
        } for i in range(1, 51)
    ]

@bp.route('/')
def index():
    return render_template('index.html', active_page='home')

@bp.route('/place_order')
def place_order():
    page = request.args.get('page', 1, type=int)
    per_page = 10
    products = get_fake_products() # TODO: Replace with database query
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
    all_products = get_fake_products()
    
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
