#rom flask import Blueprint

#bp = Blueprint('main', __name__)

#from . import index, po_form, place_order, order_success  # noqa: F401, E402

from flask import Blueprint

#Define the Blueprint for the main routes
bp = Blueprint('main', __name__)

#Import your route handlers here
from . import index, po_form, place_order, order_success, order_stages  # noqa: F401, E402
