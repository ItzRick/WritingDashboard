from app.feedback.generateFeedback.BaseFeedback import BaseFeedback
from app.models import Explanations, Files
from decimal import Decimal

def testBaseFeedback(testClient):
    '''
        Test if the genFeedback method returns None if this is not overridden.
        Attributes:
            feedbackObject: Object to create feedback for the source integration and content writing category.
        Arguments:
            testClient:  The test client we test this for.
    '''
    del testClient
    feedbackObject = BaseFeedback('', '', 1, 1, '')
    assert feedbackObject.genFeedback() == None

def testUploadToDatabase(testClient, initDatabase):
    '''
        Test if the uploadToDatabase method re-uses old explanation ids.
        Attributes:
            feedbackObject: Object to create feedback for the source integration and content writing category.
            file: An instance of the Files class as uploaded to the database.
            explanation: A single explanation, as uploaded to the database.
            explanations: Explanations, as uploaded to the database.
        Arguments:
            testClient:  The test client we test this for.
    '''
    del testClient, initDatabase
    # Retrieve a file from the database:
    file = Files.query.first()
    # Initialize the feedbackObject:
    feedbackObject = BaseFeedback('', '', file.id, 1, '')
    feedbackObject.explanationType = 0
    # Upload the first explanation to the database:
    feedbackObject.uploadExplanation(-1, -1, -1, -1, 0, 0, 'explanation', 'mistake', [], 0.01)
    # Check if we can retrieve this explanation correctly:
    explanation = Explanations.query.filter_by(fileId=file.id).first()
    assert explanation.serialize == {'X1': -1.0, 'X2': -1.0, 'Y1': -1.0, 'Y2': -1.0, 'explId': 0, 
    'explanation': 'explanation', 'feedbackVersion': Decimal('0.01'), 'fileId': 1, 'mistakeText': 'mistake', 
    'replacement1': '', 'replacement2': '',  'replacement3': '', 'type': 0}
    # Upload the second explanation:
    feedbackObject.addSingleExplanation(-1, -1, -1, -1, 0, 'explanation1', 'mistake1', [])
    feedbackObject.uploadToDatabase()
    # Check if we can retrieve this explanation correctly and if the explId is re-used:
    explanations = Explanations.query.filter_by(fileId=file.id).all()
    assert len(explanations) == 1
    assert explanations[0].serialize == {'X1': -1.0, 'X2': -1.0, 'Y1': -1.0, 'Y2': -1.0, 'explId': 0, 
    'explanation': 'explanation1', 'feedbackVersion': Decimal('0.00'), 'fileId': 1, 'mistakeText': 'mistake1', 
    'replacement1': '', 'replacement2': '',  'replacement3': '', 'type': 0}

def testUploadToDatabaseRemove(testClient, initDatabase):
    '''
        Test if the uploadToDatabase method removes old explanations if the length of the explanations is not equal.
        Attributes:
            feedbackObject: Object to create feedback for the source integration and content writing category.
            file: An instance of the Files class as uploaded to the database.
            explanations: Explanations, as uploaded to the database, before adding the extra explanation and after.
        Arguments:
            testClient:  The test client we test this for.
    '''
    del testClient, initDatabase
    # Retrieve a file from the database:
    file = Files.query.first()
    # Initialize the feedbackObject:
    feedbackObject = BaseFeedback('', '', file.id, 1, '')
    feedbackObject.explanationType = 0
    # Upload the first two explanations to the database:
    feedbackObject.uploadExplanation(-1, -1, -1, -1, 0, 0, 'explanation', 'mistake', [], 0.01)
    feedbackObject.uploadExplanation(-1, -1, -1, -1, 1, 0, 'explanation2', 'mistake2', [], 0.01)
    # Check if we can retrieve these explanations correctly:
    explanations = Explanations.query.filter_by(fileId=file.id).all()
    assert len(explanations) == 2
    assert explanations[0].serialize == {'X1': -1.0, 'X2': -1.0, 'Y1': -1.0, 'Y2': -1.0, 'explId': 0, 
    'explanation': 'explanation', 'feedbackVersion': Decimal('0.01'), 'fileId': 1, 'mistakeText': 'mistake', 
    'replacement1': '', 'replacement2': '',  'replacement3': '', 'type': 0}
    assert explanations[1].serialize == {'X1': -1.0, 'X2': -1.0, 'Y1': -1.0, 'Y2': -1.0, 'explId': 1, 
    'explanation': 'explanation2', 'feedbackVersion': Decimal('0.01'), 'fileId': 1, 'mistakeText': 'mistake2', 
    'replacement1': '', 'replacement2': '',  'replacement3': '', 'type': 0}
    # Upload the new explanation:
    feedbackObject.addSingleExplanation(-1, -1, -1, -1, 0, 'explanation1', 'mistake1', [])
    feedbackObject.uploadToDatabase()
    # Check if we can retrieve this explanation correctly and if the old explanations are removed:
    explanations = Explanations.query.filter_by(fileId=file.id).all()
    assert len(explanations) == 1
    assert explanations[0].serialize == {'X1': -1.0, 'X2': -1.0, 'Y1': -1.0, 'Y2': -1.0, 'explId': 1, 
    'explanation': 'explanation1', 'feedbackVersion': Decimal('0.00'), 'fileId': 1, 'mistakeText': 'mistake1', 
    'replacement1': '', 'replacement2': '',  'replacement3': '', 'type': 0}


