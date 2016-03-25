from app import db


class ProfileDescriptions(db.Model):
    __tablename__ = 'profile_descriptions'
    _local_id = db.Column('local_id', db.Sequence('profile_description_local_id_seq'), primary_key=True)
    id = db.Column('id', db.BigInteger, db.ForeignKey('profiles.id'), nullable=False, index=True)
    language = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text, nullable=False)

    def __init__(self, id, language, description):
        # 'id' auto increment
        self.id = id
        self.language = language
        self.description = description

    def __repr__(self):
        return '<profile %i %s>' % self.id, self.name
