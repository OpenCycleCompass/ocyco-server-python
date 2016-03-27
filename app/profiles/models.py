from app import db

from app.profile_descriptions.models import ProfileDescriptions
from app.cost_static.models import CostStatic

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
        cost_list = []
        costs = CostStatic.query.filter(CostStatic.profile == self.id).all()
        for cost in costs:
            cost_list.append(cost.get_dict())
        return {
            'id': self.id,
            'name': self.name,
            'description': {language: self.get_description(language)},
            'costs': cost_list,
               }

    def get_name(self):
        return self.name

    def get_description(self, language):
        return ProfileDescriptions.query\
            .filter(ProfileDescriptions.id == self.id)\
            .filter(ProfileDescriptions.language == language)\
            .first().description
