import datetime
import copy
from flask import Blueprint, jsonify, request

from sqlalchemy import func, text
from sqlalchemy.orm.exc import MultipleResultsFound, NoResultFound
from werkzeug.exceptions import abort
from app import db
from app.tracks.models import Tracks, TrackPoints

mod = Blueprint('track', __name__, url_prefix='/track')


def make_hash(o):
    """
    Makes a hash from a dictionary, list, tuple or set to any level, that contains
    only other hashable types (including any lists, tuples, sets, and
    dictionaries).
    From http://stackoverflow.com/a/8714242
    """
    if isinstance(o, (set, tuple, list)):
        return hash(tuple([make_hash(e) for e in o]))
    elif not isinstance(o, dict):
        return hash(o)
    new_o = copy.deepcopy(o)
    for k, v in new_o.items():
        new_o[k] = make_hash(v)
    return hash(tuple(frozenset(sorted(new_o.items()))))


@mod.route('/list', methods=['GET'])
def track_list():
    """
    List all tracks in database
    """
    return jsonify(tracks=[track.to_dict_short() for track in Tracks.query.all()])


@mod.route('/num', methods=['GET'])
def track_num():
    """
    Count all tracks in database
    """
    return jsonify(num=db.session.query(func.count(Tracks.id)).scalar())


@mod.route('/<int:track_id>', methods=['GET'])
def track_get(track_id):
    """
    Get track from database
    """
    try:
        return jsonify(Tracks.query.filter(Tracks.id == track_id).one().to_dict_long())
    except MultipleResultsFound, e:
        # internal server error
        abort(500, 'track exists multiple time in database')
    except NoResultFound, e:
        abort(404, 'track does not exist')


@mod.route('/<int:track_id>', methods=['DELETE'])
def track_delete(track_id):
    """
    Delete track from database
    """
    # track_points are automatically deleted because of orm relationship
    try:
        track = Tracks.query.filter(Tracks.id == track_id).one()
        track_num_points = track.num_points
        db.session.delete(track)
        db.session.commit()
        return jsonify({
            'success': True,
            'num_points': track_num_points,
        })
    except MultipleResultsFound, e:
        # internal server error
        abort(500, 'track exists multiple time in database')
    except NoResultFound, e:
        abort(410, 'track does not exist')


@mod.route('/add', methods=['POST'])
def track_add():
    """
    Put new track into database
    """
    # Read JSON from request
    json = request.get_json()
    # Check for required fields present
    if not (('data' in json) and ('public' in json) and ('length' in json) and ('duration' in json)):
        # TODO custom error message
        abort(400, 'some fields are missing in json')
    for point in json['data']:
        if not (('lat' in point) and ('lon' in point) and ('time' in point)):
            # TODO custom error message
            abort(401, 'data array is incorrect')
    # insert Track into database
    if 'created' in json:
        track_created = 0
    else:
        track_created = datetime.datetime.now()
    # TODO: determinate city (reverse geocoding...)
    track_city = 'MyCity'
    # Create Linestring of track geometry
    track_geom = ['LINESTRING(']
    for point in json['data']:
        track_geom.append(str(point['lon']))
        track_geom.append(' ')
        track_geom.append(str(point['lat']))
        track_geom.append(',')
    track_geom.pop()  # remove last ','
    track_geom.append(')')
    track_geom = "".join(track_geom)  # build string
    # create new track object
    track = Tracks(created=track_created,
                   uploaded=datetime.datetime.now(),
                   length=json['length'],
                   duration=json['duration'],
                   num_points=len(json['data']),
                   public=json['public'],
                   name=json.get('name'),
                   comment=json.get('comment'),
                   city=track_city,
                   data_hash=str(make_hash(json['data'])),
                   extension_geom=None,
                   track_geom=track_geom,
                   )
    db.session.add(track)
    # get id from created track
    db.session.commit()
    track_id = track.id
    # Insert track point into track_points table
    for point in json['data']:
        # TODO get time from timestamp
        db.session.add(TrackPoints(track_id, point['lat'], point['lon'], point['time'], point.get('altitude'),
                                   point.get('accuracy'), point.get('velocity'), point.get('vibrations')))
    db.session.commit()
    # query ST_Extent(track_points.geom) and insert into tracks.extension_geom
    query = text('UPDATE tracks SET '
                 'extension_geom = (SELECT ST_Extent(geom)::geometry FROM track_points WHERE id = :id) '
                 'WHERE id = :id')
    db.engine.execute(query, id=track_id)
    # query return values from database
    track_num_points = db.session.query(func.count(TrackPoints.id)).filter(TrackPoints.id == track_id).scalar()
    track_created = Tracks.query.filter(Tracks.id == track_id).first().created
    return jsonify({
        'success': True,
        'id': track_id,
        'num_points': track_num_points,
        'created': track_created
    })
