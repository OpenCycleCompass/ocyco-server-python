# -*- coding: utf-8 -*-

TESTING = True

DEBUG = True
SQLALCHEMY_ECHO = True

ADMINS = frozenset(['postmaster+pythonserver@open-cycle-compass.de'])

SQLALCHEMY_DATABASE_URI = 'postgres://postgres:postgres@localhost/ocyco'
DATABASE_CONNECT_OPTIONS = {}

SQLALCHEMY_TRACK_MODIFICATIONS = True
