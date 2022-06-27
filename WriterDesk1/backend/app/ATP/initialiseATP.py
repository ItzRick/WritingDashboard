import os

from app import db
from app.models import User, Projects, Clicks, Files, Scores, Explanations
from app.generateParticipants import generateParticipants
from app.database import uploadToDatabase
from flask import current_app
import shutil
import os

from app.feedback.feedback import genFeedback

'''
TO RUN THE INITIALIZATION
simply run:

flask shell

from the backend in cmd. And then run:

from app.ATP.initialiseATP import initialiseATP
initialiseATP()

'''


def helperFiles(fileName, uid, courseCode, extension):
    BASEDIR = os.path.abspath(os.path.dirname(__file__))
    fileDir = os.path.join(BASEDIR, fileName)
    f = Files(
        path=fileDir, 
        filename=fileName, 
        userId=uid, 
        courseCode=courseCode,
        fileType=extension
    )
    uploadToDatabase(f)
    return f

def helperScores(file, sSty, sCoh, sStr, sInt):
    s = Scores(file.id, sSty, sCoh, sStr, sInt)
    uploadToDatabase(s)

def helperExpl(file):
    print(file.id)
    genFeedback(file)

def initialiseATP(uploadFiles):
    '''
        Initialise the database for the ATP in accordance with the specs as given on 20:00, 22-6-2022 

        IMPORTANT: prints 2 participant's username and password
    '''
    # clear the database
    db.session.close()
    db.drop_all()
    db.create_all()

    # Delete current files and recreate the upload directory:   
    shutil.rmtree(current_app.config['UPLOAD_FOLDER'])
    os.mkdir(current_app.config['UPLOAD_FOLDER'])

    # A user with username ’student@tue.nl’, password ’StudentPass1’ and the student role.
    uname = 'student@tue.nl'
    u = User(username=uname, password_plaintext='StudentPass1', role='student')
    uploadToDatabase(u)
    uid = u.id
    assert User.query.filter_by(username=uname).first() is not None

    if uploadFiles:
        # Five files ’file 1-5’ with as userId the id of ’student@tue.nl’.
        f1 = helperFiles(
            fileName='file_1.pdf',
            extension='.pdf',
            uid=uid,
            courseCode='c1',
        )
        f2 = helperFiles(
            fileName='file_2.docx',
            extension='.docx',
            uid=uid,
            courseCode='c2',
        )
        f3 = helperFiles(
            fileName='file_3.txt',
            extension='.txt',
            uid=uid,
            courseCode='c3',
        )
        f4 = helperFiles(
            fileName='file_4.pdf',
            extension='.pdf',
            uid=uid,
            courseCode='c4',
        )
        f5 = helperFiles(
            fileName='file_5.pdf',
            extension='.pdf',
            uid=uid,
            courseCode='c5',
        )

        # Language and style scores ’scoreStyle 1-5’ for files ’file 1-5’.
        # Cohesion scores ’scoreCohesion 1-5’ for files ’file 1-5’.
        # Structure scores ’scoreStructure 1-5’ for files ’file 1-5’.
        # Source integration and content scores ’scoreIntegration 1-5’ for files ’file 1-5’.
        helperExpl(f1)
        helperExpl(f2)
        helperExpl(f3)
        helperExpl(f4)
        helperExpl(f5)

    # A user with username ’researcher@tue.nl’, password ’ResearcherPass1’ and the researcher role.
    uname='researcher@tue.nl'
    u = User(username=uname, password_plaintext='ResearcherPass1', role='researcher')
    uploadToDatabase(u)
    res = User.query.filter_by(username=uname).first()
    researcherId = res.id #save id for later
    assert res is not None

    # A project with projectName ’DeleteMe’ and as userId the id of ’researcher@tue.nl’.
    p = Projects(userId=researcherId, projectName='DeleteMe')
    uploadToDatabase(p)
    pro = Projects.query.filter_by(userId=researcherId).first()
    projectId = pro.id #save id for later
    assert pro is not None

    # Two users with usernames ’par_3’ and ’par_4’, password ’PartPass1’ and the participant role.
    # Two ParticipantToProject entries with as userId the ids of ’par_3’ and ’par_4’ and as projectId the id of ’DeleteMe’.
    participants = generateParticipants(nrOfParticipants=2, projectId=projectId)
    [User.query.filter_by(username=x['username']).first().set_password('PartPass1') for x in participants]
    db.session.commit()
    participantsIds = [User.query.filter_by(username=x['username']).first().id for x in participants]
    
    if uploadFiles:
        # A file ’participant file’ with as userId the id of ’par_3’.
        f1 = helperFiles(
            fileName='par_test1.pdf',
            extension='.pdf',
            uid=participantsIds[0],
            courseCode='c1',
        )
        # Scores and explanations for file ’participant file’.
        helperExpl(f1)

    # Idk of dit gaat werken, m aar laat het er wel in staan... 

    # At least two Clickdata entries with as userId the id of ’par_3’, one containing the url of the Document page, one containing another url.
    idParOne = participantsIds[0]
    c = Clicks(idParOne, 'https://writingdashboard.xyz/Document', 'view.document', 'name: par_test1.pdf, id: 6')
    uploadToDatabase(c)
    c = Clicks(idParOne, 'https://writingdashboard.xyz/Main', 'click.link', 'Settings')
    uploadToDatabase(c)

    # A project with project name ’Sidebar’ and as userId the id of ’researcher@tue.nl’.
    p = Projects(userId=researcherId, projectName='Sidebar')
    uploadToDatabase(p)
    pro = Projects.query.filter_by(projectName='Sidebar').first()
    projectId = pro.id #save id for later

    # A user with username ’par_5’, password ’PartPass1’ and the participant role.
    participant = generateParticipants(nrOfParticipants=1, projectId=projectId) 
    User.query.filter_by(username=participant[0]['username']).first().set_password('PartPass1')   
    db.session.commit()

    # A user with username ’admin@tue.nl’, password ’AdminPass1’ and administrator role.
    u = User(username='admin@tue.nl', password_plaintext='AdminPass1', role='admin')
    uploadToDatabase(u)

    # Kan je momenteel niet zien, maar goed:
    print('participants')
    print(participants) # keep this print here, and read it 