from asyncio.windows_events import NULL
from datetime import datetime
from tkinter import CASCADE
from app import db
from sqlalchemy.inspection import inspect


# Class to turn database models into dictionaries,
# which are able to be turned into json
class Serializer(object):
    def serialize(self):
        return {c: getattr(self, c) for c in inspect(self).attrs.keys()}

    def serializeFile(self):
        dict = {}
        for c in inspect(self).attrs.keys():
            if not c == 'scores' and not c == 'explanations' and not c == 'owner':
                dict[c] =  getattr(self, c)
        return dict

    @staticmethod
    def serializeList(l):
        return [m.serialize() for m in l]

    @staticmethod
    def serializeFiles(l):
        return [m.serializeFile() for m in l]

class User(db.Model):
    id       = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email    = db.Column(db.String(120), index=True, unique=True)
    # password_hash = db.Column(db.String(128))

    # relationships
    file = db.relationship('Files', backref='owner', lazy='dynamic', cascade='all,delete')

    def __repr__(self):
        return '<User {}>'.format(self.username)

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
    id         = db.Column(db.Integer, primary_key=True)
    userId     = db.Column(db.Integer, db.ForeignKey('user.id'))
    path       = db.Column(db.String, unique=False)
    filename   = db.Column(db.String(256), index=True, unique=False)
    fileType   = db.Column(db.String(5), unique=False)
    courseCode = db.Column(db.String(16), unique=False, default=NULL)
    date       = db.Column(db.DateTime, unique=False, default=datetime.today())

    serialize_only = ('id', 'userId', 'path', 'fileName', 'fileType', 'çourseCode', 'date')

    # relationships
    scores       = db.relationship('Scores', backref='scoredFile', lazy='dynamic', cascade='all,delete')
    explanations = db.relationship('Explanations', backref='explainedFile', lazy='dynamic', cascade='all,delete')

    def __repr__(self):
        return '<Files {}>'.format(self.filename)

        

class Scores(db.Model):
    '''
        Class to enter scores and explanations related to a file. 
        Each instance here is one-to-one related to an instance in Files
        Attributes:
            fileId: Id of this database instance, Id of the file corresponding to a file in the Files
            scoreStyle: Score for Language and Style
            scoreCohesion: Score for Cohesion
            scoreStructure: Score for Structure
            scoreIntegration: Score for Source Integration and Content
    '''
    fileId = db.Column(db.Integer, db.ForeignKey('files.id'), primary_key=True)
    # Scores are numeric values with 2 decimals before and 2 decimals after the point. 
    # Thus, allowing us at least values between 10.00 and 0.00
    scoreStyle       = db.Column(db.Numeric(4,2), unique=False, default=0.0)
    scoreCohesion    = db.Column(db.Numeric(4,2), unique=False, default=0.0)
    scoreStructure   = db.Column(db.Numeric(4,2), unique=False, default=0.0)
    scoreIntegration = db.Column(db.Numeric(4,2), unique=False, default=0.0)

    def __repr__(self):
        return '<ScoresExplanations {}>'.format(self.fileId)

class Explanations(db.Model):
    '''
        Class to enter explanations related to a file. 
        Attributes:
            fileId: Id of this database instance, of this file that has been added in the database.
            explId: Id of the file corresponding to a file in the Files
            type: Explanation type, 0=style, 1=cohesion, 2=structure, 3=integration
            explanation: String containing a comment on a part of the text in the file
            location: ???
    '''
    fileId      = db.Column(db.Integer, db.ForeignKey('files.id'), primary_key=True)
    explId      = db.Column(db.Integer, primary_key=True)
    type        = db.Column(db.Integer)
    explanation = db.Column(db.String)
    # TODO location of explanation??

    def __repr__(self):
        return '<Explanations {}>'.format(self.fileId, self.explId)