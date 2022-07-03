from app.feedback.feedback import genFeedback
from app.models import Files
import os

def testGenFeedbackException(testClient):
    '''
        Test if we can get an exception from the genFeedback method. In this case if we do not initialize the database.
        Attributes:
            file: A file instance with the file we test this for..
            isSuccessful: Boolean retrieved from the uploadFile method to indicate if we have correctly calculated the score.
            response: response, as retrieved from the genFeedback method.
            fileName: fileName of the file we test this method for.
            BASEPATH: Path of the current test_setFeedbackStyle.py file.
            fileDir: Location of the file we test this for.
        Arguments:
            testClient:  The test client we test this for.
    '''
    del testClient
    fileName = 'testfeedback.pdf'
    BASEDIR = os.path.abspath(os.path.dirname(__file__))
    fileDir = os.path.join(BASEDIR, 'testFiles', fileName)
    file = Files(id = 0, userId = 0, path = fileDir, filename = fileName)
    isSuccesful, response = genFeedback(file)
    assert isSuccesful == False
    assert '(sqlite3.OperationalError) no such table: scores' in response