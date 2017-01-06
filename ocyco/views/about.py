from flask import Blueprint, jsonify

from ocyco.__about__ import ocyco_git, ocyco_git_branch, ocyco_start_time

mod = Blueprint('about', __name__)


@mod.route('/version', methods=['GET'])
def version():
    """
    Show version information
    """
    version_info = {
        'version': None,
        'starttime': ocyco_start_time,
        'git': ocyco_git,
        'git_branch': ocyco_git_branch,
    }
    return jsonify(version_info)
