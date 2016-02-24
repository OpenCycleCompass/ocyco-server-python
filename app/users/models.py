from app import db


class Users(db.Model):
    __tablename__ = 'users'
    name = db.Column(db.Text, primary_key=True, unique=True, nullable=False)
    password = db.Column(db.Text, nullable=False)
    rights = db.Column(db.BigInteger, nullable=False)
    enabled = db.Column(db.Boolean, nullable=False)

    def __init__(self, name, password, rights, enabled):
        self.name = name
        self.password = password
        self.rights = rights
        self.enabled = enabled

    def __repr__(self):
        return '<user %s>' % self.name

    def to_dict_short(self):
        return {
            'name': self.name,
               }

    def to_dict_long(self):
        return {
            'name': self.name,
            'rights': self.rights,
            'enabled': self.enabled,
               }

    def verify_password(self, password_hash):
        return self.password == password_hash
