import os
from flask import render_template, request, redirect, url_for
from ...main import bp
from ...schemas.purchase_order import PurchaseOrder
from ...database import db

# Route to display order status page
@bp.route('/order_stages', methods=['GET'])
def order_stages():
    orders = PurchaseOrder.query.all()

    if not orders:
        return render_template(
            'order_stages.html',
            orders=None,
            message="There are no orders in place right now.",
            env=os.getenv('FLASK_ENV')
        )

    return render_template(
        'order_stages.html',
        orders=orders,
        message=None,
        env=os.getenv('FLASK_ENV')
    )

# Route to update status of an order
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
