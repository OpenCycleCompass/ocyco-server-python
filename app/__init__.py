import os
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
if os.environ.get('OPENSHIFT_APP_DNS') is not None:
    app.config.from_pyfile('../openshift.cfg')
else:
    app.config.from_object('config')

db = SQLAlchemy(app)

# import and register track class
from .tracks.views import mod as track_mod


# TODO: central error handlers
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


@app.errorhandler(500)
def not_found(error):
    return jsonify({
        'status': 'Internal error',
        'error': error.description
    }), 500


app.register_blueprint(track_mod)

# When should we do this? -> now (!)
db.create_all()


if __name__ == '__main__' and os.environ['OPENSHIFT_APP_DNS'] is not None:
    app.run(app.config['IP'], app.config['PORT'])