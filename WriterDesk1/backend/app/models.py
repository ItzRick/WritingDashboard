from app import db, login
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class User(UserMixin, db.Model):
    __tablename__ = "user"
    type = db.Column(db.String(32))

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    
    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    __mapper_args__ = {
        'polymorphic_on': type,
        'polymorphic_identity':"user",
    }


class Student(User):
    __tablename__ = None
    
    __mapper_args__ = {
        'polymorphic_identity': "student",
    }

class Participant(User):
    __tablename__ = None
    
    __mapper_args__ = {
        'polymorphic_identity': "participant",
    }
    
    
@login.user_loader
def load_user(id):
    return User.query.get(int(id))