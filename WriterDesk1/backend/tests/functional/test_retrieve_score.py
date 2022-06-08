import os
from datetime import date
from app.models import Scores, Files
from werkzeug.utils import secure_filename
import json

def generalSetScore(testClient, fileId, sStyle, sCohesion, sStructure, sIntegration):
    '''
        A general method to test uploading a score
        Attributes: 
            data: The data we are trying to test the setScore with.
            response: Response of the post request.
            score: Score that should be set in the database
        Arguments:
            testClient:  The test client we test this for.
            fileId: fileId of file related to this test
            sStyle: language and style score
            sCohesion: cohesion score
            sStructure: structure score
            sIntegration: source integration and content score
    '''
    # Create the data packet:
    data = {
        'fileId': fileId,
        'scoreStyle': sStyle,
        'scoreCohesion': sCohesion,
        'scoreStructure': sStructure,
        'scoreIntegration' : sIntegration,
    }
    # Corresponding file exists?
    assert Files.query.filter_by(id=fileId).first() is not None
    # Create the response by means of the post request:
    response = testClient.post('/scoreapi/setScore', data=data)
    # See if we indeed get code 200 and the correct message from this request:
    assert response.data == b'successfully uploaded Scores'
    assert response.status_code == 200
    # See if the correct data has been added to the database which we retrieve by the filename:
    score = Scores.query.filter_by(fileId=fileId).first()
    assert score.fileId == fileId
    assert score.scoreStyle == sStyle
    assert score.scoreCohesion == sCohesion
    assert score.scoreStructure == sStructure
    assert score.scoreIntegration == sIntegration

def generalGetScore(testClient, fileId, scoreStyle, scoreCohesion, scoreStructure, scoreIntegration):
    data = {
        'fileId':fileId,
    }

    # Retrieve the files from the specified user
    response = testClient.get('/scoreapi/getScores', query_string=data)
    # Check if we get the correct status_code:
    assert response.status_code == 200
    # Check response
    data = json.loads(response.data)
    assert float(data['scoreStyle']) == scoreStyle
    assert float(data['scoreCohesion']) == scoreCohesion
    assert float(data['scoreStructure']) == scoreStructure
    assert float(data['scoreIntegration']) == scoreIntegration
    
    

def testSpecificScores(testClient, initDatabase):
    '''
        This test checks whether we can send and retreive score from and to the database
        It first makes a file since scores need a fileId to be related to
        Attributes: 
            courseCode: courseCode when initializing a file
            fileName: filename when initializing a file
            BASEDIR: Location of the conftest.py file.
            fileDir: Location of the file we are testing the upload of.
            response: the result fo retrieving the scores in the specified order
            file: file instance 
            fileId: file id related to the 
            scoreStyle: language and style score
            scoreCohesion: cohesion score
            scoreStructure: structure score
            scoreIntegration: source integration and content score
        Arguments:
            testClient:  The test client we test this for.
            initDatabase: the database instance we test this for. 
    '''
    del initDatabase

    # first upload a related file
    courseCode = '2WBB0'
    fileName = 'test.txt'
    BASEDIR = os.path.abspath(os.path.dirname(__file__))
    fileDir = os.path.join(BASEDIR, fileName)
    data = {
        'files': (open(fileDir, 'rb'), fileName),
        'fileName': fileName,
        'courseCode': courseCode,
        'userId': 256,
        'date': date(1998, 10, 30)
    }
    # Create the response by means of the post request:
    response = testClient.post('/fileapi/upload', data=data)
    assert response.data == b'success'
    file = Files.query.filter_by(filename=secure_filename(fileName)).first()
    assert file.courseCode == courseCode

    # set fileId
    fileId = file.id
    scoreStyle=0
    scoreCohesion=0
    scoreStructure=0
    scoreIntegration=0
    generalSetScore(testClient, fileId, scoreStyle, scoreCohesion, scoreStructure, scoreIntegration)
    generalGetScore(testClient, fileId, scoreStyle, scoreCohesion, scoreStructure, scoreIntegration)