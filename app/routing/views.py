from flask import Blueprint, jsonify

mod = Blueprint('routing', __name__, url_prefix='/routing')


@mod.route('/route', methods=['POST'])
def route():
    """
    Calculate a route between two specified points using a routing profile
    """
    # TODO
    return jsonify({})
