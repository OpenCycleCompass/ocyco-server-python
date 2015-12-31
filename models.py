# -*- coding: utf-8 -*-
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
import geoalchemy2

from geoalchemy import GeometryColumn, Point, WKTSpatialElement, Geometry

import os

app = Flask(__name__, instance_relative_config=True)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://postgres:testing@localhost/postgres'
db = SQLAlchemy(app)


class tracks(db.Model):
    id = db.Column('id', db.BigInteger, db.Sequenz(), primary_key=True, index=True, unique=True, autoincrement=True)
    created = db.Column(db.TIMESTAMP, nullable=False)
    uploaded = db.Column(db.TIMESTAMP, nullable=False)
    length = db.Column(db.Numeric(16, 8), nullable=False)
    duration = db.Column(db.BigInteger, nullable=False)
    num_points = db.Column(db.BigInteger, nullable=False)
    public = db.Column(db.Boolean, nullable=False)
    name = db.Column(db.Text)
    comment = db.Column(db.Text)
    city = db.Column(db.Text)
    data_hash = db.Column(db.Text, unique=True)
    extension_geom = db.Column(geoalchemy2.Geometry('POLYGON'), index=True)  # geo index?
    track_geom = db.Column(geoalchemy2.Geometry('LINESTRING'))

    def __init__(self, created, uploaded, length, duration, num_points, public, name, comment, city, data_hash,
                 extension_geom, track_geom):
        # 'id' auto increment
        self.created = created
        self.uploaded = uploaded
        self.length = length
        self.duration = duration
        self.num_points = num_points
        self.public = public
        self.name = name
        self.comment = comment
        self.city = city
        self.data_hash = data_hash
        self.extension_geom = extension_geom
        self.track_geom = track_geom

    def __repr__(self):
        return '<track %i>' % self.id

    def toDict(self):
        return {
                'id': self.id,
                'name': self.name,
                # ... TODO
               }
