from flask import Blueprint, jsonify, request
from werkzeug.exceptions import abort
import requests

mod = Blueprint('geocoding', __name__, url_prefix='/geocoding')

photon_url = 'http://photon.komoot.de'


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
    request_json = request.get_json()
    if request_json is None or 'lat' not in request_json or 'lon' not in request_json:
        abort(400, 'lat and/or lon is missing')

    try:
        payload = {
            'lat': request_json[u'lat'],
            'lon': request_json[u'lon'],
        }
        photon_req = requests.get(photon_url + '/reverse', params=payload)
        if photon_req.status_code != requests.codes.ok:
            abort(500, 'Photon is not responding correctly: Bad status code')
        photon_json = photon_req.json()
    except ValueError:
        abort(500, 'Photon is not responding correctly: Invalid JSON')

    if not (photon_json is not None and
                u'features' in photon_json and
                len(photon_json[u'features']) >= 1 and
                u'properties' in photon_json[u'features'][0] and
                u'osm_id' in photon_json[u'features'][0][u'properties']
            ):
        if len(photon_json[u'features']) == 0:
            abort(404, 'No osm object found')
        abort(500, 'Photon is not responding correctly')

    osm_id = photon_json[u'features'][0][u'properties'][u'osm_id']

    return jsonify(osm_id=osm_id)


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
