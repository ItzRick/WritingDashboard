from app.scoreapi.scores import setExplanationDB, removeExplanationsAndScores, setScoreDB
from app.models import Files, Explanations, Scores
from decimal import Decimal

def testsetExplanationDBFail(testClient, initDatabaseEmpty):
    '''
        Test if the setExplanationDB method fails if we have no file in the database and try to upload a score 
        for a fileId that is not in the database.
        Attributes:
            file: An instance of the Files class as uploaded to the database.
            isSuccesful: Retrieved from the setExplanationDB method to indicate if a explanation has been successfully uploaded.
            message: Message as retrieve from the setExplanationDB method.
        Arguments:
            testClient:  The test client we test this for.
            initDatabaseEmpty: the database instance we test this for.
    '''
    del testClient, initDatabaseEmpty
    # Retrieve a file from the database:
    file = Files.query.first()
    # Check if this file is equal to None:
    assert file == None
    # Try to upload an explanation to the database for a fileId that does not exist:
    isSuccesful, message = setExplanationDB(fileId = 0, type = 0, explanation = 'explanation', explId = -1, mistakeText = 'mistake', 
    X1 = -1, X2 = -1, Y1 = -1, Y2 = -1, replacement1 = '', replacement2 = '', replacement3 = '', feedbackVersion = 0.01)
    # See if we get the correct Boolean and message:
    assert isSuccesful == False
    assert message == 'No file found with fileId'

def testsetExplanationDBNew(testClient, initDatabase):
    '''
        Test if the setExplanationDB succesfully uploads a new explanation.
        Attributes:
            file: An instance of the Files class as uploaded to the database.
            isSuccesful: Retrieved from the setExplanationDB method to indicate if a explanation has been successfully uploaded.
            message: Message as retrieve from the setExplanationDB method.
            explanation: Explanation belonging to the fileId of the file we upload the explanation for.
        Arguments:
            testClient:  The test client we test this for.
            initDatabaseEmpty: the database instance we test this for.
    '''
    del testClient, initDatabase
    # Retrieve a file from the database:
    file = Files.query.first()
    # Try to upload an explanation for this file to the database:
    isSuccesful, message = setExplanationDB(fileId = file.id, type = 0, explanation = 'explanation', explId = -1, mistakeText = 'mistake', 
    X1 = -1, X2 = -1, Y1 = -1, Y2 = -1, replacement1 = '', replacement2 = '', replacement3 = '', feedbackVersion = 0.01)
    # See if we get the correct message and Boolean from this method:
    assert isSuccesful == True
    assert message == 'Successfully uploaded Explanations'
    # Check if the explanation has been succesfully uploaded to the database:
    explanation = Explanations.query.filter_by(fileId=file.id).first()
    assert explanation.serialize == {'X1': -1.0, 'X2': -1.0, 'Y1': -1.0, 'Y2': -1.0, 'explId': 1, 
    'explanation': 'explanation', 'feedbackVersion': Decimal('0.01'), 'fileId': file.id, 'mistakeText': 'mistake', 
    'replacement1': '', 'replacement2': '',  'replacement3': '', 'type': 0}

def testsetExplanationDBNewReuse(testClient, initDatabase):
    ''''
        Test if the setExplanationDB succesfully can re-use an explanation id..
        Attributes:
            file: An instance of the Files class as uploaded to the database.
            isSuccesful: Retrieved from the setExplanationDB method to indicate if a explanation has been successfully uploaded.
            message: Message as retrieve from the setExplanationDB method.
            explanations: Explanations belonging to the fileId of the file we upload the explanation for.
        Arguments:
            testClient:  The test client we test this for.
            initDatabaseEmpty: the database instance we test this for.
    '''
    del testClient, initDatabase
    # Retrieve a file from the database:
    file = Files.query.first()
    # Try to upload an explanation for this file to the database:
    isSuccesful, message = setExplanationDB(fileId = file.id, type = 0, explanation = 'explanation', explId = -1, 
    mistakeText = 'mistake', X1 = -1, X2 = -1, Y1 = -1, Y2 = -1, replacement1 = '', replacement2 = '', 
    replacement3 = '', feedbackVersion = 0.01)
    # See if the message and Boolean is correct:
    assert isSuccesful == True
    assert message == 'Successfully uploaded Explanations'
    # Check if the explanation has been successfully uploaded to the database:
    explanations = Explanations.query.filter_by(fileId=file.id).all()
    assert len(explanations) == 1
    assert explanations[0].serialize == {'X1': -1.0, 'X2': -1.0, 'Y1': -1.0, 'Y2': -1.0, 'explId': 1, 
    'explanation': 'explanation', 'feedbackVersion': Decimal('0.01'), 'fileId': file.id,
    'mistakeText': 'mistake', 'replacement1': '', 'replacement2': '',  'replacement3': '', 'type': 0}
    # Upload a new explanation for this explanationId:
    isSuccesful, message = setExplanationDB(fileId = file.id, type = 0, explanation = 'explanation1', 
    explId = explanations[0].explId, mistakeText = 'mistake1', X1 = -1, X2 = -1, Y1 = -1, Y2 = -1, 
    replacement1 = '', replacement2 = '', replacement3 = '', feedbackVersion = 0.01)
    # See if the message and Boolean is correct:
    assert isSuccesful == True
    assert message == 'Successfully uploaded Explanations'
    # Check if the explanation has been successfully uploaded to the database:
    explanations = Explanations.query.filter_by(fileId=file.id).all()
    assert len(explanations) == 1
    assert explanations[0].serialize == {'X1': -1.0, 'X2': -1.0, 'Y1': -1.0, 'Y2': -1.0, 'explId': 1, 
    'explanation': 'explanation1', 'feedbackVersion': Decimal('0.01'), 'fileId': file.id,
    'mistakeText': 'mistake1', 'replacement1': '', 'replacement2': '',  'replacement3': '', 'type': 0}

def testRemoveExplanationsAndScores(testClient, initDatabase):
    '''
        Test if the removeExplanationsAndScores method removes all explanations and scores corresponding to a file.
        Attributes:
            file: An instance of the Files class as uploaded to the database.
        Arguments:
            testClient:  The test client we test this for.
            initDatabaseEmpty: the database instance we test this for.
    '''
    del testClient, initDatabase
    # Retrieve a file from the database:
    file = Files.query.first()
    # Upload a score for this file:
    setScoreDB(fileId = file.id, scoreStyle = 1, scoreCohesion = 1, scoreStructure = 1, scoreIntegration = 1, feedbackVersion = 0.01)
    assert len(Scores.query.filter_by(fileId=file.id).all()) == 1
    # Upload an explanation for this file:
    setExplanationDB(fileId = file.id, type = 0, explanation = 'explanation', explId = -1, 
    mistakeText = 'mistake', X1 = -1, X2 = -1, Y1 = -1, Y2 = -1, replacement1 = '', replacement2 = '', 
    replacement3 = '', feedbackVersion = 0.01)
    assert len(Explanations.query.filter_by(fileId=file.id).all()) == 1
    # Call the removeExplanationsAndScores method and check if the scores and files have been successfully removed:
    removeExplanationsAndScores(file.id)
    assert len(Scores.query.filter_by(fileId=file.id).all()) == 0
    assert len(Explanations.query.filter_by(fileId=file.id).all()) == 0