from ...api.util import get_products
from ...main import bp
from flask import render_template


@bp.route('/')
def index():
    products = get_products(limit=10)

    return render_template('index.html', active_page='home', products=products)
