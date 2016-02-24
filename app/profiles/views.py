from flask import Blueprint, jsonify, request

from app.profiles.models import Profiles

mod = Blueprint('profile', __name__)


@mod.route('/profiles', methods=['GET'])
def profiles_list():
    """
    List all profiles
    """
    profiles = {}
    for profile in Profiles.query.all():
        profiles[profile.name] = profile.get_description()
    return jsonify(profiles)


@mod.route('/profiles/<string:profile_name>', methods=['GET'])
def profile_get(profile_name):
    """
    Get a profile by name inclusive costs
    """
    # TODO
    return jsonify({})


@mod.route('/profiles/<string:profile_name>', methods=['POST'])
def profile_update(profile_name):
    """
    Update profiles cost
    """
    json = request.get_json()
    # TODO
    return jsonify({})
