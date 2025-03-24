from flask import jsonify
from . import bp

@bp.route('/order', methods=['POST'])
def place_order():
    return jsonify({'message': 'Order placed'})
