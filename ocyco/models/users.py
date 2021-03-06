from ocyco.database import db

from passlib.hash import sha512_crypt


class Users(db.Model):
    __tablename__ = 'users'
    name = db.Column(db.Text, primary_key=True, unique=True, nullable=False)
    password_hash = db.Column(db.Text, nullable=False)
    rights = db.Column(db.BigInteger, nullable=False)
    enabled = db.Column(db.Boolean, nullable=False)

    def __init__(self, name, password, rights, enabled):
        hash = sha512_crypt.encrypt(password)
        self.name = name
        self.password_hash = hash
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

    def verify_password(self, password):
        return sha512_crypt.verify(password, self.password_hash)

    def is_superuser(self):
        return self.rights >= 100
