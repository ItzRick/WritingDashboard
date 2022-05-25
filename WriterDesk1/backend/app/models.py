from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):
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
    
    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.passwordHash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.passwordHash, password)

    __mapper_args__ = {
        'polymorphic_on': type,
        'polymorphic_identity':"user",
    }


class Student(User):
    '''
        Subclass of User table, for students
    '''

    __tablename__ = None
    
    __mapper_args__ = {
        'polymorphic_identity': "student",
    }

class Participant(User):
    '''
        Subclass of User table, for participantszz
    '''
    __tablename__ = None
    
    __mapper_args__ = {
        'polymorphic_identity': "participant",
    }