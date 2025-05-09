import os
from flask import render_template, request
from ...main import bp
from ...api.util import get_products
from ..forms.po_form import BulkOrderForm


@bp.route('/po_form', methods=['POST'])
def po_form():
    form = BulkOrderForm()

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
        form=form,
        active_page='place_order',
        products=selected_products,
        env=os.getenv('FLASK_ENV')
    )
