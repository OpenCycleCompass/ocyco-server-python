from flask import Blueprint, jsonify, request

from app.profiles.models import Profiles
from app.way_types.models import WayTypes  # create way_types table (static_cost table depends on it)


mod = Blueprint('profile', __name__)

# TODO: validate language tag
# TODO: unknown language error handling


@mod.route('/profiles', methods=['GET'])
def profiles_list():
    """
    List all profiles
    """
    # Read JSON from request
    json = request.get_json()
    # language (default is 'de-DE')
    language = 'de-DE'
    # Check for lang fields present
    if (json is not None) and (not ('lang' in json)):
        language = json.get('lang')
    profile_list = {}
    for profile in Profiles.query.all():
        profile_list[profile.get_name()] = profile.get_description(language)
    return jsonify(profile_list)


@mod.route('/profiles/<string:profile_name>', methods=['GET'])
def profile_get(profile_name):
    """
    Get a profile by name inclusive costs
    """
    # Read JSON from request
    json = request.get_json()
    language='de-DE'
    # Check for lang fields present
    if (json is not None) and (not ('lang' in json)):
        language = json.get('lang')
    profile = Profiles.query.filter(Profiles.name == profile_name).first()
    return jsonify(profile.to_dict_long(language))


@mod.route('/profiles/<string:profile_name>', methods=['POST'])
def profile_update(profile_name):
    """
    Update profiles cost
    """
    json = request.get_json()
    # TODO
    return jsonify({})
