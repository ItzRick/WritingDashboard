from distutils.command.upload import upload
from app.models import Files, Scores, User, ParticipantToProject, Scores, Explanations
from app.database import uploadToDatabase

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

def testScore():
    '''
        Test if the score model works properly
        Attributes: 
            score: score model
    '''
    score = Scores(
        fileId = 12,
        scoreStyle = 0.01,
        scoreCohesion = 2,
        scoreStructure = 3,
        scoreIntegration = 10.0,
    )
    assert score.fileId == 12
    assert score.scoreStyle == 0.01
    assert score.scoreCohesion == 2
    assert score.scoreStructure == 3
    assert score.scoreIntegration == 10.0

def testUser(testClient, initDatabaseEmpty):
    del testClient, initDatabaseEmpty
    user = User.query.all()
    assert str(user[0]) == '<User ad>'

def testParticipantToProject(testClient, initDatabaseEmpty):
    del testClient, initDatabaseEmpty
    particpantProject = ParticipantToProject(0, 1)
    uploadToDatabase(particpantProject)
    particpantsProjectRetrieved = ParticipantToProject.query.all()
    assert str(particpantsProjectRetrieved[0]) == '<ParticipantToProject 0 1>'

def testParticipantToProjectSerialize(testClient, initDatabaseEmpty):
    del testClient, initDatabaseEmpty
    particpantProject = ParticipantToProject(0, 1)
    uploadToDatabase(particpantProject)
    particpantProjectRetrieved = ParticipantToProject.query.first()
    particpantProjectSerialized = ParticipantToProject.serializeParticipantToProject(particpantProjectRetrieved)
    assert particpantProjectSerialized == {'linkedParticipant': None, 'projectId': 1, 'projects': None, 'userId': 0}

def testScores(testClient, initDatabaseEmpty):
    del testClient, initDatabaseEmpty
    score = Scores(fileId = 0, scoreStyle = 1, scoreCohesion = 1, scoreStructure = 1, scoreIntegration = 1, feedbackVersion = 1)
    uploadToDatabase(score)
    scoresRetrieved = Scores.query.all()
    assert str(scoresRetrieved[0]) == '<Scores 0 1.00>'

def testExplanations(testClient, initDatabaseEmpty):
    del testClient, initDatabaseEmpty
    explanation = Explanations(fileId = 0, explId = 0, type = 0, explanation = "", mistakeText = "", X1 = -1, X2 = -1, Y1 = -1, Y2 = -1,
    replacement1 = "", replacement2 = "", replacement3 = "", feedbackVersion = 0.01)
    uploadToDatabase(explanation)
    explanationsRetrieved = Explanations.query.all()
    assert str(explanationsRetrieved[0]) == '<Explanations 0 0>' 
    
