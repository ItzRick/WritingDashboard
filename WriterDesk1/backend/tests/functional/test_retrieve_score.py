import os
from datetime import date
from app.models import Scores, Files
from werkzeug.utils import secure_filename
import json
from decimal import Decimal
from test_set_role import loginHelper

def uploadFile(testClient):
    '''
        General function to upload file
        Attributes:
            courseCode: courseCode when initializing a file
            fileName: filename of testing file
            BASEDIR: Location of the current testing file
            fileDir: Location of the file we are testing the upload of.
            response: the result fo retrieving the scores in the specified order
            file: file instance 
            access_token: the access token
        Arguments: 
            testClient: The test client we test this for.
        Returns:
            response: response from backend
            file: file instance in database that has been uploaded
    '''
    courseCode = '2WBB0'
    fileName = 'test.txt'
    BASEDIR = os.path.abspath(os.path.dirname(__file__))
    fileDir = os.path.join(BASEDIR, fileName)
    data = {
        'files': (open(fileDir, 'rb'), fileName),
        'fileName': fileName,
        'courseCode': courseCode,
        'userId': 256,
        'date': date(1998, 10, 30),
        'feedbackVersion': 0.01
    }
    # Create the response by means of the post request:
    access_token = loginHelper(testClient, 'ad', 'min')
    response = testClient.post('/fileapi/upload', data=data,
                                headers={"Authorization": "Bearer " + access_token})
    file = Files.query.filter_by(filename=fileName).first()
    assert response.data == f'Uploaded file with ids: [{file.id}]'.encode('utf-8')
    assert file.courseCode == courseCode
    return response, file

def generalGetScore(testClient, fileId, scoreStyle, scoreCohesion, scoreStructure, scoreIntegration):
    '''
        A general method to test retrieving a score.
        Check if the file related to fileId has scores and if they equal the given scores
        Attributes: 
            data: The data we are trying to test the getScore with.
            response: Response of the get request.
            dataResponse: response data, i.e. the score
            access_token: the access token
        Arguments:
            testClient:  The test client we test this for.
            fileId: fileId of file related to this test
            scoreStyle: language and style score
            scoreCohesion: cohesion score
            scoreStructure: structure score
            scoreIntegration: source integration and content score
    '''
    # data for get request
    data = {
        'fileId':fileId,
    }

    # Retrieve the files from the specified user
    access_token = loginHelper(testClient, 'ad', 'min')
    response = testClient.get('/scoreapi/getScores', query_string=data,
                                headers={"Authorization": "Bearer " + access_token})
    # Check if we get the correct status_code:
    assert response.status_code == 200
    # Check response
    dataResponse = json.loads(response.data)
    assert float(dataResponse['scoreStyle']) == scoreStyle
    assert float(dataResponse['scoreCohesion']) == scoreCohesion
    assert float(dataResponse['scoreStructure']) == scoreStructure
    assert float(dataResponse['scoreIntegration']) == scoreIntegration
    