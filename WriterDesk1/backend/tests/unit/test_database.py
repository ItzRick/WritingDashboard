from distutils.command.upload import upload
from app.models import Files, Scores, User, ParticipantToProject, Scores, Explanations, Projects, Clicks
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
    '''
        Test if we get the correct display if we run User.query.all(), so the representation of '<User <username>>'. 
        Attributes: 
            users: all users of the type User in the database.
        Arguments:
            testClient:  The test client we test this for.
            initDatabaseEmpty: the database instance we test this for. 
    '''
    del testClient, initDatabaseEmpty
    users = User.query.all()
    assert str(users[0]) == '<User ad>'

def testParticipantToProject(testClient, initDatabaseEmpty):
    '''
        Test if we get the correct display if we run ParticipantToProject.query.all(), 
        so the representation of '<ParticipantToProject <userid> <projectid>>'. 
        Attributes: 
            participantProject: an instance of the ParticipantToProject class we add to the database.
            participantsProjectsRetrieved: all ParticipantProjects as retrieved from the database.
        Arguments:
            testClient:  The test client we test this for.
            initDatabaseEmpty: the database instance we test this for. 
    '''
    del testClient, initDatabaseEmpty
    # Upload the ParticipantProject to the database:
    participantProject = ParticipantToProject(0, 1)
    uploadToDatabase(participantProject)
    # Retrieve it from the database and see if we get the correct representation.
    participantsProjectsRetrieved = ParticipantToProject.query.all()
    assert str(participantsProjectsRetrieved[0]) == '<ParticipantToProject 0 1>'

def testParticipantToProjectSerialize(testClient, initDatabaseEmpty):
    '''
        Test if we get the correct result from serializeParticipantToProject of a ParticipantProject, which 
        has been uploaded to the database.
        Attributes: 
            participantProject: an instance of the ParticipantToProject class we add to the database.
            participantsProjectsRetrieved: one ParticpantProject as retrieved from the database.
            participantProjectSerialized: This retrieved project serialized with the serializeParticipantToProject method.
        Arguments:
            testClient:  The test client we test this for.
            initDatabaseEmpty: the database instance we test this for. 
    '''
    del testClient, initDatabaseEmpty
    # Upload the ParticipantProject to the database:
    particpantProject = ParticipantToProject(0, 1)
    uploadToDatabase(particpantProject)
    # Retrieve this project from the database and serialize it, check the serialization:
    participantProjectRetrieved = ParticipantToProject.query.first()
    participantProjectSerialized = ParticipantToProject.serializeParticipantToProject(participantProjectRetrieved)
    assert participantProjectSerialized == {'linkedParticipant': None, 'projectId': 1, 'projects': None, 'userId': 0}

def testScores(testClient, initDatabaseEmpty):
    '''
        Test if we get the correct display if we run Scores.query.all(), 
        so the representation of '<Scores <fileId> <feedbackVersion>>'. 
        Attributes: 
            score: an instance of the Scores class we add to the database.
            scoresRetrieved: all Scores as retrieved from the database.
        Arguments:
            testClient:  The test client we test this for.
            initDatabase: the database instance we test this for. 
    '''
    del testClient, initDatabaseEmpty
    # Upload the score to the database:
    score = Scores(fileId = 0, scoreStyle = 1, scoreCohesion = 1, scoreStructure = 1, scoreIntegration = 1, feedbackVersion = 1)
    uploadToDatabase(score)
    # Retrieve the score and check the result:
    scoresRetrieved = Scores.query.all()
    assert str(scoresRetrieved[0]) == '<Scores 0 1.00>'

def testExplanations(testClient, initDatabaseEmpty):
    '''
        Test if we get the correct display if we run Explanations.query.all(), 
        so the representation of '<Explanations <fileId> <explId>>'. 
        Attributes: 
            explanation: an instance of the Explanations class we add to the database.
            explanationsRetrieved: all Explanations as retrieved from the database.
        Arguments:
            testClient:  The test client we test this for.
            initDatabase: the database instance we test this for. 
    '''
    del testClient, initDatabaseEmpty
    # Add this explanation to the database:
    explanation = Explanations(fileId = 0, explId = 0, type = 0, explanation = "", mistakeText = "", X1 = -1, X2 = -1, Y1 = -1, Y2 = -1,
    replacement1 = "", replacement2 = "", replacement3 = "", feedbackVersion = 0.01)
    uploadToDatabase(explanation)
    # Retrieve this explanation and check the result:
    explanationsRetrieved = Explanations.query.all()
    assert str(explanationsRetrieved[0]) == '<Explanations 0 0>' 
    
def testProjects(testClient, initDatabaseEmpty):
    '''
        Test if we get the correct display if we run Projects.query.all(), 
        so the representation of '<Project <projectname>>'. 
        Attributes: 
            project: an instance of the Projects class we add to the database.
            projectsRetrieved: all Projects as retrieved from the database.
        Arguments:
            testClient:  The test client we test this for.
            initDatabase: the database instance we test this for. 
    '''
    del testClient, initDatabaseEmpty
    # Upload this project to the database:
    project = Projects(userId = 0, projectName = "project")
    uploadToDatabase(project)
    # Retrieve all projects from the database and check the result:
    projectsRetrieved = Projects.query.all()
    assert str(projectsRetrieved[0]) == '<Project project>'

def testClicks(testClient, initDatabaseEmpty):
    '''
        Test if we get the correct display if we run Clicks.query.all(), 
        so the representation of '<Clicks <userId> <clickId>>'. 
        Attributes: 
            click: an instance of the Clicks class we add to the database.
            clicksFromDatabase: all Clicks as retrieved from the database.
        Arguments:
            testClient:  The test client we test this for.
            initDatabase: the database instance we test this for. 
    '''
    del testClient, initDatabaseEmpty
    click = Clicks(userId = 0, url = "https://xyz.xyz", eventType = "click")
    uploadToDatabase(click)
    clicksFromDatabase = Clicks.query.all()
    assert str(clicksFromDatabase[0]) == '<Clicks 0 1>'
