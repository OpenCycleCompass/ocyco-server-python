from app import db

import geoalchemy2
from shapely import wkb


class TrackPoints(db.Model):
    __tablename__ = 'track_points'
    _local_id = db.Column('local_id', db.BigInteger, db.Sequence('track_points_local_id_seq'), primary_key=True,
                          unique=True, autoincrement=True)
    id = db.Column('id', db.BigInteger, db.ForeignKey('tracks.id'), nullable=False, index=True)
    geom = db.Column(geoalchemy2.Geometry('POINT'), nullable=False, index=True)  # geo index?
    time = db.Column(db.TIMESTAMP, nullable=False)
    altitude = db.Column(db.Numeric(16, 8))
    accuracy = db.Column(db.Numeric(11, 8))
    velocity = db.Column(db.Numeric(11, 8))
    vibrations = db.Column(db.Numeric(16, 8))

    def __init__(self, id, lat, lon, time, altitude, accuracy, velocity, vibrations):
        self.id = id
        self.geom = 'POINT(' + str(lon) + ' ' + str(lat) + ')'
        self.time = time
        self.altitude = altitude
        self.accuracy = accuracy
        self.velocity = velocity
        self.vibrations = vibrations

    def __repr__(self):
        return '<trackpoint %i: %s>' % self.id, self.geom

    def to_dict_short(self):
        point = wkb.loads(bytes(self.geom.data))
        return {
            'lat': point.y,
            'lon': point.x,
            'time': self.time,
               }

    def to_dict_long(self):
        point = wkb.loads(bytes(self.geom.data))
        return {
            'lat': point.y,
            'lon': point.x,
            'time': self.time,
            'alt': self.altitude,
            'accuracy': self.accuracy,
            'velocity': self.velocity,
            'vibrations': self.vibrations,
               }
