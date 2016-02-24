from app import db


class Profiles(db.Model):
    __tablename__ = 'profiles'
    id = db.Column('id', db.BigInteger, db.Sequence('profiles_id_seq'), primary_key=True, index=True, unique=True, autoincrement=True)
    name = db.Column(db.Text, nullable=False) # unique?

    def __init__(self, name):
        # 'id' auto increment
        self.name = name

    def __repr__(self):
        return '<profile %i %s>' % self.id, self.name

    def to_dict_short(self):
        return {
            'id': self.id,
            'name': self.name,
               }

    def to_dict_long(self, language):
        # TODO add description
        return {
            'id': self.id,
            'name': self.name,
            'lang': language,
            'description': 'TODO',
               }

    def get_description(self):
        return self.name + ": [TODO: Description]"
