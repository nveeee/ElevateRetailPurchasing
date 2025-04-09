from flask import render_template, request
from app.main import bp
from app.api.util import get_products


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
