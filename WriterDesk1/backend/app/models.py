from app import db
from sqlalchemy.inspection import inspect

# Class to turn database models into dictionaries,
# which are able to be turned into json
class Serializer(object):
    def serialize(self):
        return {c: getattr(self, c) for c in inspect(self).attrs.keys()}

    @staticmethod
    def serializeList(l):
        return [m.serialize() for m in l]

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    # password_hash = db.Column(db.String(128))

    def __repr__(self):
        return '<User {}>'.format(self.username)

class Files(db.Model, Serializer):
    id = db.Column(db.Integer, primary_key=True)
    userId = db.Column(db.Integer, unique=False)
    path = db.Column(db.String, unique=False)
    filename = db.Column(db.String(256), unique=False)
    courseCode = db.Column(db.String(16), unique=False)
    date = db.Column(db.DateTime, unique=False)

    def __repr__(self):
        return '<File {}>'.format(self.filename)