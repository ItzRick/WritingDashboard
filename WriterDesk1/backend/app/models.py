from datetime import datetime
from app import db
from werkzeug.security import generate_password_hash, check_password_hash

from datetime import datetime
from sqlalchemy.inspection import inspect

class User(db.Model):
    '''
        Declare user model containing usernames and passwords (hashed), we use single table inheritance for different types of users.
        Cascade makes sure that if a User is removed, related files instances in the db are also removed
        Attributes:
            role: Identifies role of user, role is one of: ['admin', 'participant', 'researcher', 'student']
            id: Unique primary key User ID 
            username: email address or username from user
            passwordHash: hashed password from user, hashed using werkzeug.security
            trackable: whether or not the user wants to be tracked. 
    '''
    __tablename__ = "user"
    role = db.Column(db.String(32))
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), index=True, unique=True)
    passwordHash = db.Column(db.String(128))
    trackable = db.Column(db.Boolean, default=True)

    def __init__(self, username: str, password_plaintext: str, role: str ='user', trackable: bool = True):
        ''' 
            Create new user, use set_password to create hashed password for plaintext password
            Arguments:
                username: Username of new user
                password_plaintext: Password (to be hashed) for new user
                role: Role of new user, standard is: 'user'        
                trackable: whether the user wants to be tracked or not  
        '''
        self.role = role
        self.username = username
        self.set_password(password_plaintext)
        self.trackable = trackable

    def serializeUser(self):
        dict = {}
        for c in inspect(self).attrs.keys():
            if not c == 'file' and not c == 'passwordHash':
                dict[c] =  getattr(self, c)
        return dict

    @staticmethod
    def serializeList(l):
        return [m.serializeUser() for m in l]

    # relationships
    file = db.relationship('Files', backref='owner', lazy='dynamic', cascade='all,delete')
    researcher = db.relationship('Projects', backref='projectOwner', lazy='dynamic', cascade='all,delete')
    participant = db.relationship('ParticipantToProject', backref='participanttoproject', lazy=True, cascade='all,delete')

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.passwordHash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.passwordHash, password)

class Files(db.Model):
    '''
        Class to enter files in the database. 
        Cascade makes sure that if a File is removed, related Scores and Explanations instances in the db are also removed
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
    courseCode = db.Column(db.String(16), unique=False, default=None)
    date       = db.Column(db.DateTime, unique=False, default=datetime.today())

    def serializeFile(self):
        dict = {}
        for c in inspect(self).attrs.keys():
            if not c == 'scores' and not c == 'explanations' and not c == 'owner':
                dict[c] =  getattr(self, c)
            elif c == 'scores':
                for scores in self.scores.all():
                    for d in inspect(scores).attrs.keys():
                        if d != 'fileId' and d != 'scoredFile': 
                            attr = getattr(scores, d)
                            if attr >= 0:
                                dict[d] = getattr(scores, d)
        return dict

    @staticmethod
    def serializeList(l):
        return [m.serializeFile() for m in l]

    # relationships
    scores       = db.relationship('Scores', backref='scoredFile', lazy='dynamic', cascade='all,delete')
    explanations = db.relationship('Explanations', backref='explainedFile', lazy='dynamic', cascade='all,delete')

    def __repr__(self):
        return '<Files {}>'.format(self.filename)

class ParticipantToProject(db.Model):
    '''
        Model containing user id's and project id's, linking a participant to a research project.
        Attributes:
            userId: id of the participant
            projectId: id of the research project
            participant: User object linked by userId
            project: Projects object linked by projectId
    '''
    __tablename__ = "participanttoproject"
    userId = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True, autoincrement=False)
    projectId = db.Column(db.Integer, db.ForeignKey('projects.id'))

    def __init__(self, userId: int, projectId: int):
        '''
            Create new tuple, linking a participant to a project
            Arguments:
                userId: id of the participant
                projectId: id of the research project
        '''
        self.userId = userId
        self.projectId = projectId

    def serializeParticipantToProject(self):
        dict = {}
        for c in inspect(self).attrs.keys():
            if not c == 'participant' and not c == 'project':
                dict[c] =  getattr(self, c)
        return dict

    def __repr__(self):
        return '<ParticipantToProject {}>'.format(self.userId)

class Scores(db.Model):
    '''
        Class to enter scores and explanations related to a file.
        Each instance here is one-to-one related to an instance in Files
        Scores should be between 0 and 10. Additionally, values are rounded to 2 decimals
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
    scoreStyle       = db.Column(db.Numeric(4,2), unique=False, default=None)
    scoreCohesion    = db.Column(db.Numeric(4,2), unique=False, default=None)
    scoreStructure   = db.Column(db.Numeric(4,2), unique=False, default=None)
    scoreIntegration = db.Column(db.Numeric(4,2), unique=False, default=None)

    def __repr__(self):
        return '<ScoresExplanations {}>'.format(self.fileId)

class Explanations(db.Model):
    '''
        Class to enter explanations related to a file. 
        Attributes:
            fileId: Id of this database instance, of this file that has been added in the database.
            explId: Id of the file corresponding to a file in the Files
            type: Explanation type, what type of mistake is explained,
                    0=style, 1=cohesion, 2=structure, 3=integration
            explanation: String containing a comment on a part of the text in the file
            mistakeText: What text in the document is wrong
            X1: X of the top right corner of the boxing rectangle
            X2: X of the bottom left corner of the boxing rectangle
            Y1: Y of the top right corner of the boxing rectangle
            Y2: Y of the bottom left corner of the boxing rectangle
            replacement1..3: Three possible replacements for the mistakeText
    '''
    fileId      = db.Column(db.Integer, db.ForeignKey('files.id'), index=True)
    explId      = db.Column(db.Integer, primary_key=True, autoincrement=True)
    type        = db.Column(db.Integer, default=-1)
    explanation = db.Column(db.String, default='')
    mistakeText = db.Column(db.String, default='')
    X1          = db.Column(db.Float, default=-1)
    X2          = db.Column(db.Float, default=-1)
    Y1          = db.Column(db.Float, default=-1)
    Y2          = db.Column(db.Float, default=-1)
    replacement1= db.Column(db.String, default='')
    replacement2= db.Column(db.String, default='')
    replacement3= db.Column(db.String, default='')

    def __repr__(self):
        return '<Explanations {}>'.format(self.fileId, self.explId)

    @property
    def serialize(self):
        dict = {}
        for c in inspect(self).attrs.keys():
            #skip related file
            if not c == 'explainedFile':
                dict[c] = getattr(self, c)
        return dict


class Projects(db.Model):
    '''
        Class to enter research projects in the database.
        Attributes:
            id: Id of this database instance, of this project that has been added in the database.
            userId: Id of the researcher corresponding to the research project.
            projectName: Name of the research project.
            participants: participants object linked by projectId
    '''
    __tablename__ = "projects"
    id = db.Column(db.Integer, primary_key=True)
    userId = db.Column(db.Integer, db.ForeignKey('user.id'))
    projectName = db.Column(db.String(256), index=True, unique=False, default='')

    participants = db.relationship('ParticipantToProject', backref='projects', lazy='dynamic', cascade='all,delete')

    def __init__(self, userId: int, projectName: str):
        ''' Create new tuple'''
        self.userId = userId
        self.projectName = projectName

    def __repr__(self):
        return '<Project {}>'.format(self.projectName)
