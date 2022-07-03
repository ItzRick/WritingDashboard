from app.scoreapi.scores import getCurrentExplanationVersion, setScoreDB, setExplanationDB, removeExplanationsAndScores
from app.models import Files, Explanations, User, Scores

def testGetCurrentExplanationVersion(testClient, initDatabase):
    '''
        Test the getCurrentExplanationVersion method for files from which we can retrieve an associated score.
        Arguments:
            testClient:  The test client we test this for.
            initDatabase: the database instance we test this for. 
        Attributes:     
            file: A file instance of the database, as previously uploaded to said database.
    '''
    del testClient, initDatabase
    # Get a file instance from the database:
    file = Files.query.first()
    # Call the genFeedback method and check if we get the correct info returned:
    setScoreDB(file.id, 0, 0, 0, 0, 2)
    assert getCurrentExplanationVersion(file.id) == 2


def testGetCurrentExplanationVersionWithRemove(testClient, initDatabase):
    '''
        Test the getCurrentExplanationVersion method for files from which we can retrieve an explanation 
        and for when we get an error, that is an explanation with a different version than the associated score.
        Arguments:
            testClient:  The test client we test this for.
            initDatabase: the database instance we test this for. 
        Attributes:     
            file: A file instance of the database, as previously uploaded to said database.
    '''
    del testClient, initDatabase
    # Get a file instance from the database:
    file = Files.query.first()
    # Call the genFeedback method and check if we get the correct info returned:
    setScoreDB(file.id, 0, 0, 0, 0, 2)
    assert getCurrentExplanationVersion(file.id) == 2
    setExplanationDB(fileId = file.id, type = 1, explanation = 'hi', feedbackVersion = 3)
    assert getCurrentExplanationVersion(file.id) == -1
    assert Scores.query.first() == None
    assert Explanations.query.first() == None

def testRemoveExplanationsAndScores(testClient, initDatabase):
    '''
        Test the removeExplanationsAndScores after we have uploaded some scores and explanations to the database.
        Arguments:
            testClient:  The test client we test this for.
            initDatabase: the database instance we test this for. 
        Attributes:     
            file: A file instance of the database, as previously uploaded to said database.
    '''
    del testClient, initDatabase
    # Get a file instance from the database:
    file = Files.query.first()
    # Call the genFeedback method and check if we get the correct info returned:
    setScoreDB(file.id, 0, 0, 0, 0, 2)
    setExplanationDB(fileId = file.id, type = 1, explanation = 'hi', feedbackVersion = 2)
    assert Scores.query.first() != None
    assert Explanations.query.first() != None
    removeExplanationsAndScores(file.id)
    assert Scores.query.first() == None
    assert Explanations.query.first() == None
    