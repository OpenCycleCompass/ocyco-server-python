import os
import config

from flask import Flask


class Ocyco(Flask):
    def __init__(self, name='ocyco', config_file=None, *args, **kw):
        # Create Flask instance
        super(Ocyco, self).__init__(name, *args, **kw)

        # Load default settings and from environment variable
        self.config.from_pyfile(config.DEFAULT_CONF_PATH)

        if 'OCYCO_CONFIG' in os.environ:
            self.config.from_pyfile(os.environ['OCYCO_CONFIG'])

        if config_file:
            self.config.from_pyfile(config_file)

    def add_sqlalchemy(self):
        """ Create and configure SQLAlchemy extension """
        from ocyco.database import db
        db.init_app(self)


def create_app(*args, **kw):
    app = Ocyco(*args, **kw)
    app.add_sqlalchemy()
    return app
