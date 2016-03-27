from app import db


class CostDynamic(db.Model):
    __tablename__ = 'cost_dynamic'
    _local_id = db.Column('local_id', db.BigInteger, db.Sequence('cost_dynamic_local_id_seq'), primary_key=True,
                          unique=True, autoincrement=True)
    track_id = db.Column(db.BigInteger, db.ForeignKey('tracks.id'), nullable=False, index=True)
    segment_id = db.Column(db.BigInteger, index=True, nullable=False)  # external pgRouting segment id
    cost_forward = db.Column(db.Numeric(16, 8))
    cost_reverse = db.Column(db.Numeric(16, 8))

    def __init__(self, track_id, segment_id, cost_forward, cost_reverse):
        # local_id auto increment
        self.track_id = track_id
        self.segment_id = segment_id
        self.cost_forward = cost_forward
        self.cost_reverse = cost_reverse

    def __repr__(self):
        return '<cost_dynamic local_id=%i, segment=%i, track=%i>' % self._local_id, self.segment_id, self.track_id
