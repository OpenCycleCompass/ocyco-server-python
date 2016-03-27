from app import db


class WayTypeDescriptions(db.Model):
    __tablename__ = 'way_type_descriptions'
    _local_id = db.Column('local_id', db.BigInteger, db.Sequence('way_type_description_local_id_seq'),
                          primary_key=True, unique=True, autoincrement=True)
    id = db.Column('id', db.BigInteger, db.ForeignKey('way_types.id'), nullable=False, index=True)
    language = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text, nullable=False)

    def __init__(self, id, description, language='de-DE'):
        self.id = id
        self.language = language
        self.description = description

    def __repr__(self):
        return '<way_type_description %i %s>' % self.id, self.language
