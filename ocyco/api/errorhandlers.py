from flask import jsonify
from ocyco.api.exceptions import ParameterInvalidException, ParameterMissingException, NotFoundException,\
    ConflictExistingObjectException, MultipleMatchesException, PhotonException


def register(app):
    """
    Register error handlers on the given app
    :type app: flask.Flask
    """

    # errorhandlers for Flask Exceptions
    @app.errorhandler(ParameterInvalidException)
    @app.errorhandler(ParameterMissingException)
    @app.errorhandler(NotFoundException)
    @app.errorhandler(ConflictExistingObjectException)
    @app.errorhandler(MultipleMatchesException)
    @app.errorhandler(PhotonException)
    def error_ocyco_exception(error):
        return jsonify(error.to_dict()), error.status_code

    @app.errorhandler(400)
    @app.errorhandler(401)
    @app.errorhandler(404)
    @app.errorhandler(405)
    @app.errorhandler(409)
    @app.errorhandler(500)
    def error_by_code(error):
        return jsonify(error=error.description), error.code

    @app.errorhandler(TypeError)
    @app.errorhandler(ValueError)
    def error_bad_request(e):
        return jsonify(error=e.message), 400

    @app.errorhandler(LookupError)
    def error_not_found(e):
        return jsonify(error=e.message), 404

    @app.errorhandler(Exception)
    def error_unknown(e):
        return jsonify(error=e.message), 500
