from flask import Blueprint, jsonify

mod = Blueprint('geocoding', __name__, url_prefix='/geocoding')


@mod.route('/id', methods=['POST'])
def geocoding_id():
    """
    Query internal ID of nearest OSM object to given lat-lon tupel.
    """
    # TODO
    return jsonify({})


@mod.route('/osm_id', methods=['POST'])
def geocoding_osm_id():
    """
    Query OSM ID of nearest OSM object to given lat-lon tupel.
    """
    # TODO
    return jsonify({})


@mod.route('/address/<address:string>', methods=['GET'])
def geocoding_address(address):
    """
    Get coordinates of given address.
    :param address: adress string from the url
    """
    # TODO
    return jsonify({})


@mod.route('/city', methods=['POST'])
def geocoding_city():
    """
    Get city of given coordinates.
    """
    # TODO
    return jsonify({})
