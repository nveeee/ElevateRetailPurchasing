from flask import Blueprint

bp = Blueprint('api', __name__)

from . import index, po_form, place_order, order_success  # noqa: F401, E402
