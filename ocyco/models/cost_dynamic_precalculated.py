from ocyco.database import db


class CostDynamicPrecalculated(db.Model):
    __tablename__ = 'cost_dynamic_precalculated'
    # external pgRouting segment id:
    segment_id = db.Column(db.BigInteger, index=True, nullable=False, unique=True, primary_key=True)
    cost_forward = db.Column(db.Numeric(16, 8))
    cost_reverse = db.Column(db.Numeric(16, 8))
    relevance = db.Column(db.Numeric(16, 8))

    def __init__(self, segment_id, cost_forward, cost_reverse, relevance):
        self.segment_id = segment_id
        self.cost_forward = cost_forward
        self.cost_reverse = cost_reverse
        self.relevance = relevance

    def __repr__(self):
        return '<cost_dynamic_precalculated %i>' % self.segment_id
