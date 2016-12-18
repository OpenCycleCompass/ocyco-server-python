import os
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy

import subprocess
import time

app = Flask(__name__)
if os.environ.get('OPENSHIFT_APP_DNS') is not None:
    app.config.from_pyfile('../openshift.cfg')
else:
    try:
        app.config.from_object('config')
    except NotADirectoryError:
        print('Unable to read ocyco flask config from config.py.')
        pass

db = SQLAlchemy(app)

ocyco_git = subprocess.check_output(['git', 'describe', '--always'])
ocyco_git_branch = subprocess.check_output(['git', 'rev-parse', '--abbrev-ref', 'HEAD'])
ocyco_start_time = time.time()

# import and register track classes
from .tracks.views import mod as track_mod
from .profiles.views import mod as profiles_mod
from .geo.views import mod as geo_mod
from .about.views import mod as about_mod
from .routing.views import mod as routing_mod
from .geocoding.views import mod as geocoding_mod


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
    }), 405


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


app.register_blueprint(track_mod)
app.register_blueprint(profiles_mod)
app.register_blueprint(geo_mod)
app.register_blueprint(about_mod)
app.register_blueprint(routing_mod)
app.register_blueprint(geocoding_mod)


# When/how should we do this? -> manually (!)
def init_db():
    db.create_all()


if __name__ == '__main__' and os.environ['OPENSHIFT_APP_DNS'] is not None:
    app.run(app.config['IP'], app.config['PORT'])
