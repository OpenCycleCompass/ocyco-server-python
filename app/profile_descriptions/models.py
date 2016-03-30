from app import db


class ProfileDescriptions(db.Model):
    __tablename__ = 'profile_descriptions'
    _local_id = db.Column('local_id', db.BigInteger, db.Sequence('track_points_local_id_seq'), primary_key=True,
                          unique=True, autoincrement=True)
    id = db.Column('id', db.BigInteger, db.ForeignKey('profiles.id'), nullable=False, index=True)
    language = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text, nullable=False)

    default_language = 'en-US'

    def __init__(self, id, language, description):
        # 'id' auto increment
        self.id = id
        self.language = language
        self.description = description

    def __repr__(self):
        return '<profile_description %i %s>' % self.id, self.name
