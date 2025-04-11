from flask import render_template
from ...main import bp


@bp.route('/order_success')
def order_success():
    return render_template('order_success.html')
