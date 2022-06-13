from app import db
from werkzeug.security import generate_password_hash, check_password_hash

from datetime import datetime
from sqlalchemy.inspection import inspect

# Class to turn database models into dictionaries,
# which are able to be turned into json
class Serializer(object):
    def serialize(self):
        return {c: getattr(self, c) for c in inspect(self).attrs.keys()}

    @staticmethod
    def serializeList(l):
        return [m.serialize() for m in l]

class User(db.Model, Serializer):
    '''
        Declare user model containing usernames and passwords (hashed), we use single table inheritance for different types of users.
        Attributes:
            type: used as discrimator, indicates type of object in row
            id: Unique primary key User ID 
            username: email address or username from user
            passwordHash: hashed password from user, hashed using werkzeug.security
    '''
    __tablename__ = "user"
    type = db.Column(db.String(32))
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), index=True, unique=True)
    passwordHash = db.Column(db.String(128))

    def __init__(self, username: str, password_plaintext: str, role: str ='user'):
        ''' Create new user, use set_password to create hashed password for plaintext password'''
        self.type = role
        self.username = username
        self.set_password(password_plaintext)

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.passwordHash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.passwordHash, password)



class Files(db.Model, Serializer):
    '''
        Class to enter files in the database. 
        Attributes:
            id: Id of this database instance, of this file that has been added in the database.
            userId: Id of the user corresponding to the current file.
            path: Path of the current file that is added to the database. 
            filename: Filename of the current file that is added to the datbase.
            courseCode: Coursecode corresponding to the current file that is added to the database.
            date: Date the current file that is uploaded to the database has been created. 
    '''
    id = db.Column(db.Integer, primary_key=True)
    # userId = db.Column(db.Integer, unique=False)
    userId = db.Column(db.Integer, db.ForeignKey('user.id'))
    path = db.Column(db.String, unique=False)
    filename = db.Column(db.String(256), index=True, unique=False)
    fileType = db.Column(db.String(5), unique=False)
    courseCode = db.Column(db.String(16), unique=False, default=None)
    date = db.Column(db.DateTime, unique=False, default=datetime.today())

    def __repr__(self):
        return '<File {}>'.format(self.filename)
