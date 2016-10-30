from flask import Blueprint, jsonify, request

from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm.exc import MultipleResultsFound

from werkzeug.exceptions import abort
from app import db
from app.decorators import requires_authentication

from app.profiles.models import Profiles
from app.way_types.models import WayTypes  # create way_types table (static_cost table depends on it)
from app.cost_static.models import CostStatic
from app.profile_descriptions.models import ProfileDescriptions


mod = Blueprint('profile', __name__)


def isfloat(value):
    if not (isinstance(value, str) or isinstance(value, float) or isinstance(value, int)):
        return False
    try:
        float(value)
        return True
    except ValueError:
        return False


def is_valid_ietf_language(language):
    # TODO: validate language tag
    return True


@mod.route('/profiles', methods=['GET', 'POST'])
def profiles_list():
    """
    List all profiles
    """
    # read request body for POST method
    if request.method == 'POST':
        # Read JSON from request
        json = request.get_json()
    else:
        json = None
    # language (default is 'de-DE')
    language = 'de-DE'
    # Check for lang fields present
    if (json is not None) and (not ('lang' in json)):
        language = json.get('lang')
    profile_list = {}
    for profile in Profiles.query.all():
        profile_list[profile.get_name()] = profile.get_description(language)
    return jsonify(profile_list)


@mod.route('/profiles/<string:profile_name>', methods=['GET', 'POST'])
def profile_get(profile_name):
    """
    Get profile data by name inclusive costs
    :param profile_name: the profile name
    """
    # read request body for POST method
    if request.method == 'POST':
        # Read JSON from request
        json = request.get_json()
    else:
        json = None
    language = ProfileDescriptions.default_language
    # Check for lang fields present
    if (json is not None) and (not ('lang' in json)):
        language = json.get('lang')
    try:
        profile = Profiles.query.filter(Profiles.name == profile_name).one()
        return jsonify(profile.to_dict_long(language))
    except MultipleResultsFound:
        abort(500, 'Multiple profiles with name \'' + profile_name + '\' found.')
    except NoResultFound:
        abort(404, 'No such profile.')


@mod.route('/profiles/update/<string:profile_name>', methods=['POST'])
@requires_authentication
def profile_update(profile_name):
    """
    Update profiles cost
    :param profile_name: the profile name
    """
    try:
        profile_id = Profiles.query.filter_by(name=profile_name).one().id
    except MultipleResultsFound:
        abort(500, 'Multiple profiles with name \'' + profile_name + '\' found.')
    except NoResultFound:
        abort(404, 'No such profile.')
    way_types_rows = WayTypes.query.all()
    way_types = []
    for row in way_types_rows:
        way_types.append(int(row.id))
    json = request.get_json()
    if json is None:
        abort(400, 'JSON body missing')
    for cost_id in json:
        if cost_id == 'amount_dyncost':
            continue
        try:
            if not int(cost_id) in way_types:
                abort(400, 'unknown way_type id: ' + cost_id)
        except ValueError:
            abort(400, 'unknown json key: ' + cost_id)
        if isfloat(json.get(cost_id)):
            cost_value = float(json.get(cost_id))
            CostStatic.query.filter_by(profile=profile_id, id=cost_id).update({
                CostStatic.cost_forward: cost_value,
                CostStatic.cost_reverse: cost_value
            })
        elif ('forward' in json.get(cost_id)) and ('reverse' in json.get(cost_id)):
            try:
                CostStatic.query.filter_by(profile=profile_id, id=cost_id).update({
                    CostStatic.cost_forward: float(json.get(cost_id).get('forward')),
                    CostStatic.cost_reverse: float(json.get(cost_id).get('reverse'))
                })
            except ValueError:
                abort(400, 'bad cost value for way_type ' + cost_id)
        else:
            abort(400, 'bad cost value for way_type ' + cost_id)
    if 'amount_dyncost' in json:
        try:
            amount_dyncost_value = float(json.get('amount_dyncost'))
            if amount_dyncost_value > 1.0 or amount_dyncost_value < 0.0:
                abort(400, 'amount_dyncost must be in range [0, 1]')
            Profiles.query.filter_by(id=profile_id).update({Profiles.amount_dyncost: amount_dyncost_value})
        except ValueError:
            abort(400, 'bad value for amount_dyncost')
    db.session.commit()
    return '', 204


@mod.route('/profiles/<string:profile_name>', methods=['PUT'])
@requires_authentication
def profile_add(profile_name):
    """
    Add a new profile
    :param profile_name: the new profile name
    """
    if Profiles.query.filter_by(name=profile_name).count() > 0:
        abort(409, 'profile \'' + profile_name + '\' exists already')
    json = request.get_json()
    if json is None:
        abort(400, 'JSON body missing')
    if ProfileDescriptions.default_language not in json:
        abort(400, 'description for default language \'' + ProfileDescriptions.default_language + '\' is mandatory')
    profile = Profiles(profile_name)
    db.session.add(profile)
    db.session.commit()
    for lang_tag in json:
        if not is_valid_ietf_language(lang_tag):
            abort(400, 'invalid IETF language tag: ' + lang_tag)
        description = ProfileDescriptions(profile.id, lang_tag, json.get(lang_tag))
        db.session.add(description)
    db.session.commit()
    return jsonify({'success': True}), 201


@mod.route('/profiles/<string:profile_name>/descriptions', methods=['GET'])
def profile_descriptions(profile_name):
    """
    Get all profiles descriptions
    :param profile_name: the profile name
    """
    try:
        profile_id = Profiles.query.filter_by(name=profile_name).one().id
    except MultipleResultsFound:
        abort(500, 'Multiple profiles with name \'' + profile_name + '\' found.')
    except NoResultFound:
        abort(404, 'No such profile.')
    descriptions = ProfileDescriptions.query.filter_by(id=profile_id).all()
    description_list = {}
    for description in descriptions:
        description_list[str(description.language)] = str(description.description)
    return jsonify(description_list)


@mod.route('/profiles/<string:profile_name>/descriptions', methods=['POST'])
@requires_authentication
def profile_descriptions_modify(profile_name):
    """
    Modify or add (additional) profiles descriptions
    :param profile_name: the profile name
    """
    try:
        profile_id = Profiles.query.filter_by(name=profile_name).one().id
    except MultipleResultsFound:
        abort(500, 'Multiple profiles with name \'' + profile_name + '\' found.')
    except NoResultFound:
        abort(404, 'No such profile.')
    json = request.get_json()
    if json is None:
        abort(400, 'JSON body missing')
    for lang_tag in json:
        if not is_valid_ietf_language(lang_tag):
            abort(400, 'invalid IETF language tag: ' + lang_tag)
        description = ProfileDescriptions.query.filter_by(id=profile_id, language=lang_tag).first()
        if description:
            description.description = json.get(lang_tag)
        else:
            description = ProfileDescriptions(profile_id, lang_tag, json.get(lang_tag))
            db.session.add(description)
    db.session.commit()
    return jsonify({'success': True}), 201
