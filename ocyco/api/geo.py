from flask import Blueprint, jsonify, request

from sqlalchemy import text

from ocyco.database import db
from ocyco.api.exceptions import ParameterMissingException

mod = Blueprint('geo', __name__)


def coordinates_from_linestring(linestring):
    """
    parse WKT linestring and return list of dicts of lat and lon values for jsonify()
    :param linestring: WKT linestring
    :return: a list of dict containing lat and lon values
    """
    # remove LINESTRING and brackets
    linestring = linestring[11:-1]
    # split in (lat lon) pairs
    linestring = linestring.split(',')
    coordinates = []
    for coordinate in linestring:
        # split lat and lon value
        coordinate = coordinate.split(' ')
        coordinates.append({
            'lon': coordinate[0],
            'lat': coordinate[1]
        })
    return coordinates


@mod.route('/geo', methods=['POST'])
def get_geo():
    """
    Get segments contained in database
    """
    # Read JSON from request
    json = request.get_json()
    # Check bounding box in json request
    if (json is None) or not ('start_lat' in json
                              and 'start_lon' in json
                              and 'end_lat' in json
                              and 'end_lon' in json):
        raise ParameterMissingException('bounding box missing')
    lat_min = min(json.get('start_lat'), json.get('end_lat'))
    lat_max = max(json.get('start_lat'), json.get('end_lat'))
    lon_min = min(json.get('start_lon'), json.get('end_lon'))
    lon_max = max(json.get('start_lon'), json.get('end_lon'))
    query = text('SELECT gid, osm_id, ST_AsText(ways.the_geom) '
                 'FROM ways '
                 'WHERE the_geom && ST_MakeEnvelope(:lon_min, :lat_min, :lon_max, :lat_max, 4326) '
                 'LIMIT 100;')
    query_result = db.engine.execute(query, lon_min=lon_min, lat_min=lat_min, lon_max=lon_max, lat_max=lat_max)
    segments = []
    for row in query_result:
        segments.append({
            'gid': row[0],
            'osm_id': row[1],
            'coordinates': coordinates_from_linestring(row[2])
        })
    return jsonify({'segment_count': query_result.rowcount, 'segments': segments})


@mod.route('/geo/profiles/<string:profile_name>', methods=['POST'])
def get_geo_profile(profile_name):
    """
    Get profiles specific cost (geo information).
    :param profile_name: the profile name from the url
    """
    # TODO
    return jsonify({})


@mod.route('/geo/dyncost', methods=['POST'])
def get_geo_dyncost():
    """
    Get dynamic cost (geo information).
    """
    # TODO
    return jsonify({})
