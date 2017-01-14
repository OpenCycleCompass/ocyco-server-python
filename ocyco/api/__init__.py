from ocyco.api.tracks import mod as track_mod
from ocyco.api.profiles import mod as profiles_mod
from ocyco.api.geo import mod as geo_mod
from ocyco.api.about import mod as about_mod
from ocyco.api.routing import mod as routing_mod
from ocyco.api.geocoding import mod as geocoding_mod

from ocyco.api.errorhandlers import register as register_error_handlers


def register(app):
    """
    :param flask.Flask app: a Flask app
    """

    register_error_handlers(app)

    app.register_blueprint(track_mod)
    app.register_blueprint(profiles_mod)
    app.register_blueprint(geo_mod)
    app.register_blueprint(about_mod)
    app.register_blueprint(routing_mod)
    app.register_blueprint(geocoding_mod)
