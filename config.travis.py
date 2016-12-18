DEBUG = False
SQLALCHEMY_ECHO = False

ADMINS = frozenset(['postmaster+travis-testing@open-cycle-compass.de'])

SQLALCHEMY_DATABASE_URI = 'postgres://postgres@localhost/ocyco_pytest'
DATABASE_CONNECT_OPTIONS = {}

SQLALCHEMY_TRACK_MODIFICATIONS = False
