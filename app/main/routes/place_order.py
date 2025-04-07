from flask import render_template, request, session
from app.main import bp
from app.api.util import get_products

@bp.route('/place_order')
def place_order():
    page = request.args.get('page', 1, type=int)
    per_page = 10
    products = get_products()  # Get products from database
    total = len(products)

    # Store in session for later access
    session['current_products'] = products[(page - 1) * per_page: page * per_page]

    return render_template(
        'place_order.html',
        active_page='place_order',
        products=session['current_products'],
        current_page=page,
        total_pages=(total // per_page) + (1 if total % per_page else 0)
    )

