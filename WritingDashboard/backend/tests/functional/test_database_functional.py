from app.models import Files, User, ParticipantToProject, Projects, Scores, Explanations
from app.database import uploadToDatabase, getFilesByUser, removeFromDatabase, postUser, postParticipant, postParticipantToProject, recordsToCsv
from app import db
from datetime import datetime
import os
from flask import current_app
from pytest import raises

def testValidFile(testClient, initDatabase):
    '''
        Test if the files which are added in the database during setup are valid and all attributes
        can be correctly retrieved.
        Attributes:
            files: all files in the datbase of type Files.
            file1: The first file of this type in the database.
            file2: The second file of this type in the database.
        Arguments:
            testClient:  The test client we test this for.
            initDatabase: the database instance we test this for. 
    '''
    del testClient, initDatabase
    # Retrieve the files:
    files = Files.query.all()
    # Test if all attributes for the first file are still currently there:
    file = files[0]
    assert file.filename=='URD_Group3_vers03_Rc.pdf'
    assert file.path=='C:/Users/20192435/Downloads/SEP2021/WriterDesk1/backend/saved_documents/URD_Group3_vers03_Rc.pdf'
    assert file.date == datetime(2019, 2, 12)
    assert file.userId == 123
    assert file.courseCode == "2IPE0"
    assert file.fileType == '.pdf'
    # Test if all attributes for the file are still currently there: 
    file = files[1]
    assert file.filename=='SEP.pdf'
    assert file.path=='C:/Users/20192435/Downloads/SEP2021/WriterDesk1/backend/saved_documents/SEP.pdf'
    assert file.date == datetime(2020, 10, 2)
    assert file.userId == 567
    assert file.courseCode == "3NAB0"
    assert file.fileType == '.pdf'

def testUploadToDatabase(testClient, initDatabase):
    '''
        Test if the uploadToDatabase function form the database module works. To do this, an instance to be added to the Files table is created
        and it is checked that we can retrieve this file correctly. Furthermore, it is checked that all attributes are still the same.
        Attributes:
            file: File to be added to the database.
            file1: This same file, only then retrieved from the database.
        Arguments:
            testClient:  The test client we test this for.
            initDatabase: the database instance we test this for. 
    '''
    del testClient, initDatabase
    # Create a file instance of Files:
    file = Files(path='C:/Users/20192435/Downloads/SEP2021/WriterDesk1/backend/saved_documents/ScrumAndXpFromTheTrenchesonline07-31.pdf', 
    filename='ScrumAndXpFromTheTrenchesonline07-31.pdf', date=datetime(2019, 2, 12), userId = 123, courseCode = '2IPE0', fileType = '.pdf')
    # Call the uploadToDatabase function:
    uploadToDatabase(file)
    # Retrieve this file with query.filter_by and check if all attributes are retrieved correctly:
    file1 = Files.query.filter_by(filename='ScrumAndXpFromTheTrenchesonline07-31.pdf').first()
    assert file1.filename =='ScrumAndXpFromTheTrenchesonline07-31.pdf'
    assert file1.path =='C:/Users/20192435/Downloads/SEP2021/WriterDesk1/backend/saved_documents/ScrumAndXpFromTheTrenchesonline07-31.pdf'
    assert file1.date == datetime(2019, 2, 12)
    assert file1.userId == 123
    assert file1.courseCode == "2IPE0"
    assert file1.fileType == '.pdf'
    # Check if we can also retrieve this with query.all() and can then retrieve it with the second element, 
    # check if all attributes are retrieved correctly:
    file2 = Files.query.all()[2]
    assert file2.filename=='ScrumAndXpFromTheTrenchesonline07-31.pdf'
    assert file2.path=='C:/Users/20192435/Downloads/SEP2021/WriterDesk1/backend/saved_documents/ScrumAndXpFromTheTrenchesonline07-31.pdf'
    assert file2.date == datetime(2019, 2, 12)
    assert file2.userId == 123
    assert file2.courseCode == "2IPE0"
    assert file2.fileType == '.pdf'
    
def testGetFilesByUser(testClient, initDatabase):
    '''
        Test if we get the correct display if we run getFilesByUser(200, 'date.asc'), so the representation of '<File <filename>>'. 
        Attributes: 
            file, file2, file3: File to be added to the database.
        Arguments:
            testClient:  The test client we test this for.
    '''
    # This test case also includes testing getting files sorted by date ascending
    del testClient, initDatabase
    # We add three files to the database session
    try:
        db.session.commit()
    except:
        db.session.rollback()
    try: 
        file = Files(path='C:/normal/path/File-1.pdf', filename='File-1.pdf', date=datetime(2019, 2, 12), userId = 200, courseCode = '2IPE0')
        db.session.add(file)
        file2 = Files(path='C:/normal/path/File-2.pdf', filename='File-2.pdf', date=datetime(2019, 2, 12), userId = 201, courseCode = '2IPE0')
        db.session.add(file2)
        file3 = Files(path='C:/normal/path/File-3.pdf', filename='File-3.pdf', date=datetime(1999, 2, 12), userId = 200, courseCode = '2IPE0')
        db.session.add(file3)
        db.session.commit()
    except: 
        db.session.rollback()
    # We retrieve the files of the user with date ascending
    files = getFilesByUser(200, 'date.asc')
    # Check if the number of files is 2,
    # that the first file is the oldest file 
    # and that the userId for that file is correct.
    assert len(files) == 2
    assert files[0].get('filename') == 'File-3.pdf'
    assert files[0].get('userId') == 200

def testCreateDatabase(testClient):
    '''
        Test if we don't get any errors if we run db.create_all()
        Arguments:
            testClient:  The test client we test this for.
    '''
    del testClient
    db.create_all()

def testFiles(testClient, initDatabase):
    '''
        Test if we get the correct display if we run Files.query.all(), so the representation of '<File <filename>>'.
        Attributes:
            files: all files of the type Files in the database.
        Arguments:
            testClient:  The test client we test this for.
            initDatabase: the database instance we test this for.
    '''
    del testClient, initDatabase
    files = Files.query.all()
    assert str(files[0]) == '<Files URD_Group3_vers03_Rc.pdf>'
    assert str(files[1]) == '<Files SEP.pdf>'

def testExplanation():
    '''
        Test if the Explanations model in database works properly
        Attributes: 
            explanation: explanation model
    '''
    explanation = Explanations(
        fileId      = 0,
        explId      = 1,
        type        = 2,
        explanation = 'explan lange zin',
        mistakeText = 'error',
        X1          = 3.0001,
        X2          = 4.101,
        Y1          = 5.990,
        Y2          = 6.4,
        replacement1= 'vier',
        replacement2= '',
        replacement3= '',
    )
    assert explanation.fileId == 0
    assert explanation.explId == 1
    assert explanation.type == 2
    assert explanation.explanation == 'explan lange zin'
    assert explanation.mistakeText == 'error'
    assert explanation.X1 == 3.0001
    assert explanation.X2 == 4.101
    assert explanation.Y1 == 5.990
    assert explanation.Y2 == 6.4
    assert explanation.replacement1== 'vier'
    assert explanation.replacement2== ''
    assert explanation.replacement3== ''
    

def testUploadToDBScore(testClient, initDatabase):
    '''
        Test if the uploadToDatabase function form the database module works for scores. 
        Attributes:
            preScore: Scores to be added to the database.
            score: This same scores, only then retrieved from the database.
        Arguments:
            testClient:  The test client we test this for.
            initDatabase: the database instance we test this for. 
    '''
    del testClient, initDatabase
    preScore = Scores(
        fileId = 12,
        scoreStyle = 0.01,
        scoreCohesion = 2,
        scoreStructure = 3,
        scoreIntegration = 10.0,
    )
    uploadToDatabase(preScore)
    # Retrieve this file with query.filter_by and check if all attributes are retrieved correctly:
    score = Scores.query.filter_by(fileId=12).first()
    assert score.fileId == 12
    assert str(score.scoreStyle) == '0.01'
    assert str(score.scoreCohesion) == '2.00'
    assert str(score.scoreStructure) == '3.00'
    assert str(score.scoreIntegration) == '10.00'

def testUploadToDBExplanation(testClient, initDatabase):
    '''
        Test if the uploadToDatabase function form the database module works for Explanations. 
        Attributes:
            preExplanation: Explanations to be added to the database.
            score: This same Explanations, only then retrieved from the database.
        Arguments:
            testClient:  The test client we test this for.
            initDatabase: the database instance we test this for. 
    '''
    del testClient, initDatabase
    preExplanation = Explanations(
        fileId      = 0,
        explId      = 1,
        type        = 2,
        explanation = 'explan lange zin',
        mistakeText = 'error',
        X1          = 3.0001,
        X2          = 4.101,
        Y1          = 5.990,
        Y2          = 6.4,
        replacement1= 'vier',
        replacement2= '',
        replacement3= '',
    )
    uploadToDatabase(preExplanation)
    # Retrieve this file with query.filter_by and check if all attributes are retrieved correctly:
    explanation = Explanations.query.filter_by(fileId=0).first()
    assert explanation.fileId == 0
    assert explanation.explId == 1
    assert explanation.type == 2
    assert explanation.explanation == 'explan lange zin'
    assert explanation.mistakeText == 'error'
    assert explanation.X1 == 3.0001
    assert explanation.X2 == 4.101
    assert explanation.Y1 == 5.990
    assert explanation.Y2 == 6.4
    assert explanation.replacement1== 'vier'
    assert explanation.replacement2== ''
    assert explanation.replacement3== ''

def testRecordsToCsv(testClient, initDatabase):
    '''
        Test if the recordsToCsv function creates a csv file with the correct data. 
        Attributes:
            user1: User data to check in the created csv file
            user2: more User data to check in the created csv file
            users: username and role of users with a username starting with 'csv'
            result: query result converted to dictionary form
            path: path to the created csv file
            BASEDIR: directory this file and the test csv file are in
            testFilePath: path to the test csv file
            fileOne: list of lines from newly created csv file
            fileTwo: list of lines from test csv file
        Arguments:
            testClient:  The test client we test this for.
            initDatabase: the database instance we test this for. 
    '''

    del testClient, initDatabase

    # Add two users with username starting with 'csv'
    user1 = User(username="csv@tue.nl", password_plaintext="Password1", role="participant")
    uploadToDatabase(user1)
    user2 = User(username="csv2@tue.nl", password_plaintext="Password1", role="participant")
    uploadToDatabase(user2)

    # Get username and role of users with username starting with 'csv', put data in dictionary
    users = User.query.with_entities(User.username, User.role).filter(User.username.startswith("csv")).all()
    result = [{col: getattr(u, col) for col in u.keys()} for u in users]
    # Check if data is correctly added to dictionary
    assert len(result) == 2

    # Create csv file from dictionary at path
    path = os.path.join(current_app.config['UPLOAD_FOLDER'], "result.csv")
    recordsToCsv(path, result)

    # Get location of test csv file
    BASEDIR = os.path.abspath(os.path.dirname(__file__))
    testFilePath = os.path.join(BASEDIR, 'testFiles', 'testcsv.csv')

    # Get content from new csv file and test csv file
    with open(path, 'r', encoding="utf-8-sig") as csv1, open(testFilePath, 'r', encoding="utf-8-sig") as csv2:
        fileOne = csv1.readlines()
        fileTwo = csv2.readlines()

    # Check if contents of the csv files is the same
    assert len(fileOne) == len(fileTwo)
    for line in fileOne:
        assert line in fileTwo

def testPostUser(testClient, initDatabase):
    '''
        Test if postUser() correctly adds a user to the database
        Attributes:
            users: all users with username 'test@tue.nl'
        Arguments:
            testClient: the test client we test this for
            initDatabase: the database instance we test this for
    '''

    del testClient, initDatabase

    # Try to add a new user to the database
    try:
        postUser("test@tue.nl", "TestPassword1", False)
        db.session.commit()
    except:
        db.session.rollback()

    # Check if user is added correctly
    users = User.query.filter_by(username="test@tue.nl").all()
    assert len(users) == 1
    assert users[0].check_password("TestPassword1")
    assert not users[0].trackable

def testPostParticipant(testClient, initDatabase):
    '''
        Test if postParticipant() correctly adds a user to the database and returns user object.
        Attributes:
            user: returned user from postParticipant()
            users: all participants with username 'test@tue.nl'
        Arguments:
            testClient: the test client we test this for
            initDatabase: the database instance we test this for
    '''

    del testClient, initDatabase

    # Try to add a new participant to the database 
    try:
        user = postParticipant("test@tue.nl", "TestPassword1")
        db.session.commit()
    except:
        db.session.rollback()

    # Check if the particpant is added correctly
    users = User.query.filter_by(role="participant", username="test@tue.nl").all()
    assert len(users) == 1
    assert users[0].check_password("TestPassword1")
    assert user.id == users[0].id

def testPostExistingParticipant(testClient, initDatabase):
    '''
        Test if postParticipant() correctly raises an exception when trying to add a user to the database that already exists.
        Attributes:
            existingUser: user added to database, so it exists already when calling postParticipant()
            user: returned user from postParticipant()
            e: exception raised by postParticipant()
        Arguments:
            testClient: the test client we test this for
            initDatabase: the database instance we test this for
    '''

    del testClient, initDatabase
    
    # Add user with username 'par_existing@tue.nl'
    existingUser = User(username="par_existing@tue.nl", password_plaintext="TestPass1", role="participant")
    db.session.add(existingUser)
    db.session.commit()

    # Try to add a new participant with username 'par_existing@tue.nl' to the database 
    with raises(Exception) as e:
        user = postParticipant("par_existing@tue.nl", "TestPass1")
    # Check for the correct error message
    assert str(e.value) == "User exists already"

def testPostParticipantToProject(testClient, initDatabase):
    '''
        Test if postParticipantToProject() correctly adds an entry to the database.
        Attributes:
            project: project entry that will be linked with a participant
            entries: all entries in ParticipantToProject for the project
        Arguments:
            testClient: the test client we test this for
            initDatabase: the database instance we test this for
    '''
    del testClient, initDatabase

    # Create a new project
    project = Projects(userId=0, projectName="Project")
    db.session.add(project)
    db.session.commit()

    # Try to add a participant to the project
    try:
        postParticipantToProject(1, project.id)
        db.session.commit()
    except:
        db.session.rollback()

    # Check if entry was correctly in ParticipantToProject
    entries = ParticipantToProject.query.filter_by(projectId=project.id).all()
    assert len(entries) == 1
    assert entries[0].userId == 1
    assert entries[0].projectId == project.id
