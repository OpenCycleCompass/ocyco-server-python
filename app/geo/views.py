from flask import Blueprint, jsonify, request

from sqlalchemy import text

from werkzeug.exceptions import abort
from app import db

mod = Blueprint('geo', __name__)


def coordinates_from_linestring(linestring):
    # remove LINESTRING and brackets
    linestring = linestring[11:-1]
    linestring = linestring.split(',')
    coordinates = []
    for coordinate in linestring:
        coordinate = coordinate.split(' ')
        coordinates.append({
            'lat': coordinate[0],
            'lon': coordinate[1]
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
        abort(400, 'bounding box missing')
    lat_min = min(json.get('start_lat'), json.get('end_lat'))
    lat_max = max(json.get('start_lat'), json.get('end_lat'))
    lon_min = min(json.get('start_lon'), json.get('end_lon'))
    lon_max = max(json.get('start_lon'), json.get('end_lon'))

    query2 = text('SELECT ways.gid AS id, ST_AsText(ways.the_geom) AS geom, classes.cost AS cost '
                 'FROM ways JOIN classes ON ways.class_id = classes.id '
                 'WHERE ways.the_geom && ST_MakeEnvelope(:lon_min, :lat_min, :lon_max, :lat_max, 4326) '
                 'AND classes.profile = :profile '
                 'LIMIT 10000;')

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
