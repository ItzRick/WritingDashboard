from sqlalchemy import false
from app.feedback.feedback import genFeedback
from app.models import Files, Explanations, User
import os
import fitz

# def uploadFile()

def testGenFeedbackNoFile(testClient, initDatabase):
    '''
        Test if we upload a file instance, without a file on the disk, we indeed get returned false 
        and indeed get returned an error message. 
        Arguments:
            testClient:  The test client we test this for.
            initDatabase: the database instance we test this for. 
        Attributes:     
            file: A file instance of the database, as previously uploaded to said database.
            isSuccesful: True if the feedback has been correctly generated, False otherwise.
            message: Message if we get an exception during execution of the method.
    '''
    del testClient, initDatabase
    # Get a file instance from the database:
    file = Files.query.first()
    # Call the genFeedback method and check if we get the correct info returned:
    isSuccessful, message = genFeedback(file)
    assert isSuccessful == False
    assert message == 'cannot unpack non-iterable NoneType object'