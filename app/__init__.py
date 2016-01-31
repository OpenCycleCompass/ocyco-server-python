from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config.from_object('config')

db = SQLAlchemy(app)

# When should we do this?
db.create_all()


@app.errorhandler(404)
def not_found(error):
    # TODO: central error handlers
    return '{"error": "404 - Not found"}', 404


# import and register track class
from app.tracks.views import mod as tracks_mod
app.register_blueprint(tracks_mod)
