from flask import Blueprint, jsonify, request
from werkzeug.exceptions import abort
from ocyco.api.exceptions import OcycoException, ParameterInvalidException, ParameterMissingException, NotFoundException, ConflictExistingObjectException, MultipleMatchesException, PhotonException
import requests

mod = Blueprint('geocoding', __name__, url_prefix='/geocoding')

photon_url = 'http://photon.komoot.de'


@mod.route('/id', methods=['POST'])
def geocoding_id():
    """
    Query internal ID of nearest OSM object to given lat-lon tupel.
    """
    request_json = request.get_json()
    if request_json is None or 'lat' not in request_json or 'lon' not in request_json:
        raise ParameterMissingException('lat and/or lon is missing')

    try:
        payload = {
            'lat': request_json[u'lat'],
            'lon': request_json[u'lon'],
        }
        photon_req = requests.get(photon_url + '/reverse', params=payload)
        if photon_req.status_code != requests.codes.ok:
            raise PhotonException('Photon is not responding correctly: Bad status code')
        photon_json = photon_req.json()
        osm_id = photon_json[u'features'][0][u'properties'][u'osm_id']
        internal_id = osm_id  # TODO: query internal ID from database
        return jsonify(id=internal_id)
    except ValueError:
        raise PhotonException('Photon is not responding correctly: Invalid JSON')
    except IndexError:
        raise NotFoundException('No osm object found')
    except KeyError:
        raise PhotonException('Photon is not responding correctly')


@mod.route('/osm_id', methods=['POST'])
def geocoding_osm_id():
    """
    Query OSM ID of nearest OSM object to given lat-lon tupel.
    """
    request_json = request.get_json()
    if request_json is None or 'lat' not in request_json or 'lon' not in request_json:
        raise ParameterMissingException('lat and/or lon is missing')

    try:
        payload = {
            'lat': request_json[u'lat'],
            'lon': request_json[u'lon'],
        }
        photon_req = requests.get(photon_url + '/reverse', params=payload)
        if photon_req.status_code != requests.codes.ok:
            raise PhotonException('Photon is not responding correctly: Bad status code')
        photon_json = photon_req.json()
        return jsonify(osm_id=photon_json[u'features'][0][u'properties'][u'osm_id'])
    except ValueError:
        raise PhotonException('Photon is not responding correctly: Invalid JSON')
    except IndexError:
        raise NotFoundException('No osm object found')
    except KeyError:
        raise PhotonException('Photon is not responding correctly')


@mod.route('/address/<string:address>', methods=['GET'])
def geocoding_address(address):
    """
    Get coordinates of given address.
    :param address: address string from the url
    """
    try:
        payload = {
            'q': address,
            'limit': 1,
        }
        photon_req = requests.get(photon_url + '/api/', params=payload)
        if photon_req.status_code != requests.codes.ok:
            raise PhotonException('Photon is not responding correctly: Bad status code')
        photon_json = photon_req.json()
        osm_id = photon_json[u'features'][0][u'properties'][u'osm_id']
        lon = photon_json[u'features'][0][u'geometry'][u'coordinates'][0]
        lat = photon_json[u'features'][0][u'geometry'][u'coordinates'][1]
        return jsonify(osm_id=osm_id, lon=lon, lat=lat)
    except ValueError:
        raise PhotonException('Photon is not responding correctly: Invalid JSON')
    except IndexError:
        raise NotFoundException('No osm object found')
    except KeyError:
        raise PhotonException('Photon is not responding correctly')

@mod.route('/city', methods=['POST'])
def geocoding_city():
    """
    Get city of given coordinates.
    """
    request_json = request.get_json()
    if request_json is None or 'lat' not in request_json or 'lon' not in request_json:
        raise ParameterMissingException('lat and/or lon is missing')

    try:
        payload = {
            'lat': request_json[u'lat'],
            'lon': request_json[u'lon'],
        }
        photon_req = requests.get(photon_url + '/reverse', params=payload)
        if photon_req.status_code != requests.codes.ok:
            raise PhotonException('Photon is not responding correctly: Bad status code')
        photon_json = photon_req.json()
        return jsonify(city=photon_json[u'features'][0][u'properties'][u'city'])
    except ValueError:
        raise PhotonException('Photon is not responding correctly: Invalid JSON')
    except IndexError:
        raise NotFoundException('No osm object found')
    except KeyError:
        raise PhotonException('Photon is not responding correctly')
