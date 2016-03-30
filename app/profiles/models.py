from app import db

from app.profile_descriptions.models import ProfileDescriptions
from app.cost_static.models import CostStatic

from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm.exc import MultipleResultsFound


class Profiles(db.Model):
    __tablename__ = 'profiles'
    id = db.Column('id', db.BigInteger, db.Sequence('profiles_id_seq'), primary_key=True, index=True, unique=True,
                   autoincrement=True)
    name = db.Column(db.Text, nullable=False, unique=True)
    amount_dyncost = db.Column(db.Numeric(16, 8), nullable=False)

    def __init__(self, name, amount_dyncost=0.0):
        # 'id' auto increment
        self.name = name
        self.amount_dyncost = amount_dyncost

    def __repr__(self):
        return '<profile %i %s>' % self.id, self.name

    def to_dict_short(self):
        return {
            'id': self.id,
            'name': self.name,
        }

    def to_dict_long(self, language):
        cost_list = []
        costs = CostStatic.query.filter_by(profile=self.id).all()
        for cost in costs:
            cost_list.append(cost.get_dict())
        return {
            'id': self.id,
            'name': self.name,
            'description': {language: self.get_description(language)},
            'costs': cost_list,
            'amount_dyncost': float(self.amount_dyncost),
        }

    def get_name(self):
        return self.name

    def get_description(self, language):
        try:
            description = ProfileDescriptions.query.filter_by(id=self.id, language=language).one().description
        except MultipleResultsFound:
            return 'Multiple profile descriptions for profile \'' + self.id + '\' and language \'' + language + '\' found.'
        except NoResultFound:
            if language == ProfileDescriptions.default_language:
                return 'No profile description found.'
            else:
                return self.get_description(ProfileDescriptions.default_language)

        return description
