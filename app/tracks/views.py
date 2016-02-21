from flask import Blueprint, jsonify

from sqlalchemy import func
from app import db
from app.tracks.models import Tracks

mod = Blueprint('track', __name__, url_prefix='/track')


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


@mod.route('/<int:id>', methods=['GET'])
def track_get(id):
    """
    Get track from database
    """
    return jsonify(Tracks.query.filter(Tracks.id == id).first().to_dict_long())
