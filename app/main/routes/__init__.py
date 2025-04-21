from flask import Blueprint

bp = Blueprint('main', __name__)

from . import index, po_form, place_order, order_success, order_stages  # noqa: F401, E402
