from app.models import Files, User
import os
from app.usersapi.routes import deleteFile
from flask import current_app
from datetime import date
from test_set_role import loginHelper

def testDeleteFileNone(testClient):
    '''
        Test the deleteFile method if we pass a none object as file, to indicate a file that cannot
        be found.
        Arguments: 
            fileName: Filename in the location of this testfile we upload.
            testClient: The test client we test this for.
        Attributes: 
            file: Database instance of a file that is inside the database. 
            message: Message as retrieved from the deleteFile method.
            code: Code as retrieved from the deleteFile method.
    '''
    del testClient
    message, code = deleteFile(None)
    assert message == 'file does not exist in database'
    assert code == 404

def testDeleteFileNotFound(testClient, initDatabase):
    '''
        Test the deleteFile method on a file that has only been added to the database.
        Arguments: 
            fileName: Filename in the location of this testfile we upload.
            testClient: The test client we test this for.
        Attributes: 
            file: Database instance of a file that is inside the database. 
            message: Message as retrieved from the deleteFile method.
            code: Code as retrieved from the deleteFile method.
    '''
    del testClient, initDatabase
    file = Files.query.first()
    message, code = deleteFile(file)
    assert message == 'file does not exist'
    assert code == 404

def testDeleteFileFound(testClient, initDatabase):
    '''
        Upload a file to the server, to test the deleteFile method on a file that has been uploaded.
        Arguments: 
            fileName: Filename in the location of this testfile we upload.
            testClient: The test client we test this for.
        Attributes: 
            user: A user which has been added to the database.
            BASEDIR: Directory the test_genFeedback.py file is located inside. 
            fileDir: The path to the actual file we upload. 
            data: Data to upload this file with. 
            response: Response after the ai call.
            file: Database instance of the file we have uploaded. 
            access_token: the access token.
            message: Message as retrieved from the deleteFile method.
            code: Code as retrieved from the deleteFile method.
    '''
    del initDatabase
    # Upload the file:
    fileName = "test.docx"
    user = User.query.filter_by(username='ad').first()
    # Get the BASEDIR and set the fileDir with that:
    BASEDIR = os.path.abspath(os.path.dirname(__file__))
    fileDir = os.path.join(BASEDIR, 'testFiles', fileName)
    # Create the data packet:
    data = {
        'files': (open(fileDir, 'rb'), fileName),
        'fileName': fileName,
        'userId': user.id,
        'courseCode': '',
        'date': date(2022, 5, 11)
    }
    # Create the response by means of the post request:
    access_token = loginHelper(testClient, 'ad', 'min')
    response = testClient.post('/fileapi/upload', data=data,
                                headers={"Authorization": "Bearer " + access_token})
    assert response.status_code == 200
    file = Files.query.filter_by(filename=fileName).first()
    # Check if this file actgually exists on the path:
    assert os.path.isfile(os.path.join(current_app.config['UPLOAD_FOLDER'], str(user.id), fileName))
    # Delete the file:
    message, code = deleteFile(file)
    # Check if the message and code from this method are correct:
    assert message == 'succes'
    assert code == 200
    # Check if the file does not exist anymore:
    assert not os.path.isfile(os.path.join(current_app.config['UPLOAD_FOLDER'], str(user.id), fileName))
