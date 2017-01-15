from ocyco.database import db


class WayTypes(db.Model):
    __tablename__ = 'way_types'
    id = db.Column('id', db.BigInteger, primary_key=True, index=True, unique=True)

    def __init__(self, id):
        self.id = id

    def __repr__(self):
        return '<way_type %i>' % self.id
