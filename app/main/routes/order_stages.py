import os
from flask import render_template, request, redirect, url_for
from ...main import bp
from ...schemas.purchase_order import PurchaseOrder
from ...database import db

# Route to display order statuses
@bp.route('/order_stages', methods=['GET'])
def order_stages():
    page = request.args.get('page', 1, type=int)
    per_page = 10

    #orders using Flask-SQLAlchemy
    orders_query = PurchaseOrder.query.order_by(PurchaseOrder.id).paginate(page=page, per_page=per_page, error_out=False)
    orders = orders_query.items
    total_pages = orders_query.pages

    return render_template(
        'order_stages.html',
        orders=orders,
        message=None,
        current_page=page,
        total_pages=total_pages,
        active_page='order_stages',
        env=os.getenv('FLASK_ENV')
    )

# Route to update the status of an order
@bp.route('/update_order_status/<int:order_id>', methods=['POST'])
def update_order_status(order_id):
    order = PurchaseOrder.query.get(order_id)

    if not order:
        return redirect(url_for('main.order_stages'))

    new_status = request.form.get('status')
    if new_status:
        order.status = new_status
        db.session.commit()

    return redirect(url_for('main.order_stages'))

