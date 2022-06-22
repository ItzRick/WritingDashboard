import os

from app import db
from app.models import User, Projects, Clicks, Files, Scores, Explanations
from app.generateParticipants import generateParticipants
from app.database import uploadToDatabase

def helperFiles(filename, uid, courseCode, extension):
    BASEDIR = os.path.abspath(os.path.dirname(__file__))
    fileDir = os.path.join(BASEDIR, filename)
    f = Files(
        path=fileDir, 
        filename=filename, 
        userId=uid, 
        courseCode=courseCode,
        fileType=extension
    )
    uploadToDatabase(f)
    return f.id

def helperScores(fileId, sSty, sCoh, sStr, sInt):
    s = Scores(fileId, sSty, sCoh, sStr, sInt)
    uploadToDatabase(s)

def helperExpl(fileId, type, expl, ):
    e = Explanations()
    # TODO
    uploadToDatabase(e)
    return 0

def initialiseATP():
    '''
        Initialise the database for the ATP in accordance with the specs as given on 20:00, 22-6-2022 

        IMPORTANT: prints 2 participant's username and password
    '''
    # clear the database
    db.session.close()
    db.drop_all()
    db.create_all()

    # A user with username ’student@tue.nl’, password ’StudentPass1’ and the student role.
    uname = 'student@tue.nl'
    u = User(username=uname, password_plaintext='StudentPass1', role='student')
    uid = u.id
    uploadToDatabase(u)
    assert User.query.filter_by(username=uname).first() is not None

    # Five files ’file 1-5’ with as userId the id of ’student@tue.nl’.
    fid1 = helperFiles(
        fileName='test1.pdf',
        extension='.pdf',
        uid=uid,
        courseCode='c1',
    )
    fid2 = helperFiles(
        fileName='test2.pdf',
        extension='.pdf',
        uid=uid,
        courseCode='c2',
    )
    fid3 = helperFiles(
        fileName='test3.pdf',
        extension='.pdf',
        uid=uid,
        courseCode='c3',
    )
    fid4 = helperFiles(
        fileName='test4.pdf',
        extension='.pdf',
        uid=uid,
        courseCode='c4',
    )
    fid5 = helperFiles(
        fileName='test5.pdf',
        extension='.pdf',
        uid=uid,
        courseCode='c5',
    )

    # Language and style scores ’scoreStyle 1-5’ for files ’file 1-5’.
    # Cohesion scores ’scoreCohesion 1-5’ for files ’file 1-5’.
    # Structure scores ’scoreStructure 1-5’ for files ’file 1-5’.
    # Source integration and content scores ’scoreIntegration 1-5’ for files ’file 1-5’.
    helperScores(fid1, 1,2,3,4)
    helperScores(fid2, 5,6,7,8)
    helperScores(fid3, 9,10,0,1)
    helperScores(fid4, 2,3,4,5)
    helperScores(fid5, 6,7,8,9)

    # A user with username ’researcher@tue.nl’, password ’ResearcherPass1’ and the researcher role.
    u = User(username=uname, password_plaintext='ResearcherPass1', role='researcher')
    researcherId = u.id #save id for later
    uploadToDatabase(u)
    assert User.query.filter_by(id=researcherId).first() is not None

    # A project with projectName ’DeleteMe’ and as userId the id of ’researcher@tue.nl’.
    p = Projects(userId=researcherId, projectName='DeleteMe')
    projectId = p.id #save id for later
    uploadToDatabase(p)
    assert Projects.query.filter_by(id=projectId).first() is not None

    # Two users with usernames ’par ’ and ’par ’, passwords ” and ” and the participant role.
    # Two ParticipantToProject entries with as userId the ids of ’par ’ and ’par ’ and as projectId the id of ’DeleteMe’.
    participants = generateParticipants(nrOfParticipants=2, projectId=projectId)
    participantsIds = [User.query.filter_by(username=x.username).first() for x in participants]
    
    # A file ’participant file’ with as userId the id of ’par ’.
    fid1 = helperFiles(
        fileName='test1.pdf',
        extension='.pdf',
        uid=participantsIds[0],
        courseCode='c1',
    )
    fid2 = helperFiles(
        fileName='test2.pdf',
        extension='.pdf',
        uid=participantsIds[0],
        courseCode='c2',
    )

    # Scores and explanations for file ’participant file’.
    helperScores(fid1, 1,2,3,4)
    helperScores(fid2, 5,6,7,8)

    # At least two Clickdata entries with as userId the id of ’par ’, one containing the url of the Document page, one containing another url.
    idParOne = participantsIds[0]
    c = Clicks(idParOne, 'Document', 'test1.test1')
    uploadToDatabase(c)
    c = Clicks(idParOne, 'Main', 'test2.test2')
    uploadToDatabase(c)

    # A user with username ’admin@tue.nl’, password ’AdminPass1’ and administrator role.
    u = User(username='admin@tue.nl', password_plaintext='AdminPass1', role='admin')
    uploadToDatabase(u)