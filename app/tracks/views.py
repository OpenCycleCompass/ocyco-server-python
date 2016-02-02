from flask import Blueprint, jsonify

from app import db
from app.tracks.models import Tracks
from app.decorators import requires_superuser

mod = Blueprint('tracks', __name__, url_prefix='/tracks')


@mod.route('/list', methods=['GET'])
@requires_superuser
def track_list():
    """
    List all tracks in database
    """
    return jsonify(tracks=[track.toDict() for track in Tracks.query.all()])
