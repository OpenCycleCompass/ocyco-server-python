DEBUG = True
SQLALCHEMY_ECHO = True

ADMINS = frozenset(['ibis@mytfg.de'])

SQLALCHEMY_DATABASE_URI = 'postgres://postgres:testing@localhost/ibis'
DATABASE_CONNECT_OPTIONS = {}

SQLALCHEMY_TRACK_MODIFICATIONS = True