from flask import jsonify


def register(app):
    """
    Register error handlers on the given app
    :type app: flask.Flask
    """

    @app.errorhandler(400)
    def not_found(error):
        return jsonify({
            'status': 'Bad Request',
            'error': error.description
        }), 400

    @app.errorhandler(401)
    def not_found(error):
        return jsonify({
            'status': 'Unauthorized',
            'error': error.description
        }), 401

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'status': 'Not found',
            'error': error.description
        }), 404

    @app.errorhandler(405)
    def not_found(error):
        return jsonify({
            'status': 'Method Not Allowed',
            'error': error.description
        }), error.code

    @app.errorhandler(409)
    def not_found(error):
        return jsonify({
            'status': 'Conflict',
            'error': error.description
        }), 409

    @app.errorhandler(500)
    def not_found(error):
        return jsonify({
            'status': 'Internal error',
            'error': error.description
        }), 500

    @app.errorhandler(TypeError)
    @app.errorhandler(ValueError)
    def raise_bad_request(e):
        return jsonify(message=e.message), 400

    @app.errorhandler(LookupError)
    def raise_not_found(e):
        return jsonify(message=e.message), 404
