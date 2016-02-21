from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('config')

db = SQLAlchemy(app)

# import and register track class
from app.tracks.views import mod as track_mod


@app.errorhandler(404)
def not_found(error):
    # TODO: central error handlers
    return jsonify(error="Not found"), 404


app.register_blueprint(track_mod)

# When should we do this? -> now (!)
db.create_all()