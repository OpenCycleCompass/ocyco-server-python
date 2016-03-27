from app import db


class CostStatic(db.Model):
    __tablename__ = 'cost_static'
    _local_id = db.Column('local_id', db.BigInteger, db.Sequence('track_points_local_id_seq'), primary_key=True,
                          unique=True, autoincrement=True)
    id = db.Column('id', db.BigInteger, db.ForeignKey('way_types.id'), nullable=False, index=True)
    profile = db.Column('profile', db.BigInteger, db.ForeignKey('profiles.id'), nullable=False, index=True)
    cost_forward = db.Column(db.Numeric(16, 8))
    cost_reverse = db.Column(db.Numeric(16, 8))

    # unique constraint: (id, profile)-tupel
    # TODO
    # db.UniqueConstraint('cost_static.id', 'cost_static.profile')
    # TODO index? -> !

    def __init__(self, id, profile, cost_forward, cost_reverse):
        self.id = id  # way_type id
        self.profile = profile
        self.cost_forward = cost_forward
        self.cost_reverse = cost_reverse

    def __repr__(self):
        return '<cost_static %i, profile=%i>' % self.id, self.profile

    def get_dict(self):
        return {
            'way_type': self.id,
            'cost_forward': float(self.cost_forward),
            'cost_reverse': float(self.cost_reverse),
        }