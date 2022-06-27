from datetime import datetime
from test_set_role import loginHelper
from app.models import Files, Scores
from app.scoreapi.scores import setScoreDB
from app import db
from flask_jwt_extended import current_user
import json


def testRetrieveFilesAndScoresSingle(testClient, initDatabase):
    '''
        Test if we can retrieve a file with scores from the database. We first upload a file to the database and
        add the corresponding scores to the scores table. Then, we run the getFilesAndScoresByUser function to
        see if we get the correct response.
        Arguments:
            testClient: The test client we test this for.
            initDatabase: The database instance we test this for.
        Attributes:
            response: The response of the getFilesAndScoresByUser backend call,
            file: File that is added to the database.
            access_token: Access token for user ad min.
            expected_response: The response we expect when we run the function.
    '''
    del initDatabase

    # get access token for ad min
    access_token = loginHelper(testClient, 'ad', 'min')

    # Add file to database
    file = Files(path='C:/normal/path/File-1.pdf', filename='File-1.pdf', date=datetime(2019, 2, 12),
                 userId=current_user.id, courseCode='2IPE0')
    db.session.add(file)
    db.session.commit()

    # Add scores to database
    setScoreDB(file.id, 1.00, 1.00, 1.00, 1.00, 0.01)

    # Run function
    response = testClient.get('/scoreapi/getFilesAndScoresByUser', headers={"Authorization": "Bearer " + access_token})

    # Check if we get the correct status code:
    assert response.status_code == 200

    expected_response = {"id": [file.id],
                         "filename": ["File-1.pdf"],
                         "date": ["02/12/19"],
                         "scoreStyle": ["1.00"],
                         "scoreCohesion": ["1.00"],
                         "scoreStructure": ["1.00"],
                         "scoreIntegration": ["1.00"]
                         }

    # Check if the expected response is correct:
    assert json.loads(response.data) == expected_response


def testRetrieveFilesAndScoresMultiple(testClient, initDatabase):
    '''
        Test if we can retrieve multiple file with scores from the database. We first upload the files to the database and
        add the corresponding scores to the scores table. Then, we run the getFilesAndScoresByUser function to
        see if we get the correct response.
        Arguments:
            testClient: The test client we test this for.
            initDatabase: The database instance we test this for.
        Attributes:
            response: The response of the getFilesAndScoresByUser backend call,
            file1, file2: Files that are added to the database.
            access_token: Access token for user ad min.
            expected_response: The response we expect when we run the function.
    '''
    del initDatabase

    # get access token for ad min
    access_token = loginHelper(testClient, 'ad', 'min')

    # Add file to database
    file1 = Files(path='C:/normal/path/File-1.pdf', filename='File-1.pdf', date=datetime(2019, 2, 12),
                  userId=current_user.id, courseCode='2IPE0')
    file2 = Files(path='C:/normal/path/File-2.pdf', filename='File-2.pdf', date=datetime(2019, 3, 12),
                  userId=current_user.id, courseCode='2IPE0')
    db.session.add(file1)
    db.session.add(file2)
    db.session.commit()

    # Add scores to database
    setScoreDB(file1.id, 1.80, 9.00, 6.70, 7.80, 0.01)
    setScoreDB(file2.id, 8.60, 5.40, 3.20, 1.90, 100.00)

    # Run function
    response = testClient.get('/scoreapi/getFilesAndScoresByUser', headers={"Authorization": "Bearer " + access_token})

    # Check if we get the correct status code:
    assert response.status_code == 200

    expected_response = {"id": [file1.id, file2.id],
                         "filename": ["File-1.pdf", "File-2.pdf"],
                         "date": ["02/12/19", "03/12/19"],
                         "scoreStyle": ["1.80", "8.60"],
                         "scoreCohesion": ["9.00", "5.40"],
                         "scoreStructure": ["6.70", "3.20"],
                         "scoreIntegration": ["7.80", "1.90"]
                         }

    # Check if the expected response is correct:
    assert json.loads(response.data) == expected_response


def testRetrieveFilesAndScoresEmpty(testClient, initDatabase):
    '''
        Test if the function retrieves nothing when no files of the user are uploaded.
        Arguments:
            testClient: The test client we test this for.
            initDatabase: The database instance we test this for.
        Attributes:
            response: The response of the getFilesAndScoresByUser backend call,
            access_token: Access token for user ad min.
            expected_response: The response we expect when we run the function.
    '''
    del initDatabase

    # get access token for ad min
    access_token = loginHelper(testClient, 'ad', 'min')

    # Run function
    response = testClient.get('/scoreapi/getFilesAndScoresByUser', headers={"Authorization": "Bearer " + access_token})

    # Check if we get the correct status code:
    assert response.status_code == 200

    expected_response = {"id": [],
                         "filename": [],
                         "date": [],
                         "scoreStyle": [],
                         "scoreCohesion": [],
                         "scoreStructure": [],
                         "scoreIntegration": []
                         }

    # Check if the expected response is correct:
    assert json.loads(response.data) == expected_response


def testRetrieveFilesAndScoresNoScores(testClient, initDatabase):
    '''
        Test if we get nothing if we retrieve a file without scores from the database. We first upload a file
        to the database. Then, we run the getFilesAndScoresByUser function to
        see if we get the correct response.
        Arguments:
            testClient: The test client we test this for.
            initDatabase: The database instance we test this for.
        Attributes:
            response: The response of the getFilesAndScoresByUser backend call,
            file: File that is added to the database.
            access_token: Access token for user ad min.
            expected_response: The response we expect when we run the function.
    '''
    del initDatabase

    # get access token for ad min
    access_token = loginHelper(testClient, 'ad', 'min')

    # Add file to database
    file = Files(path='C:/normal/path/File-1.pdf', filename='File-1.pdf', date=datetime(2019, 2, 12),
                 userId=current_user.id, courseCode='2IPE0')
    db.session.add(file)
    db.session.commit()

    # Run function
    response = testClient.get('/scoreapi/getFilesAndScoresByUser', headers={"Authorization": "Bearer " + access_token})

    # Check if we get the correct status code:
    assert response.status_code == 200

    expected_response = {"id": [],
                         "filename": [],
                         "date": [],
                         "scoreStyle": [],
                         "scoreCohesion": [],
                         "scoreStructure": [],
                         "scoreIntegration": []
                         }

    # Check if the expected response is correct:
    assert json.loads(response.data) == expected_response


def testRetrieveFilesAndScoresNoFile(testClient, initDatabase):
    '''
        Test if we get nothing if we retrieve a file without scores from the database. We first upload a file
        to the database. Then, we run the getFilesAndScoresByUser function to
        see if we get the correct response.
        Arguments:
            testClient: The test client we test this for.
            initDatabase: The database instance we test this for.
        Attributes:
            response: The response of the getFilesAndScoresByUser backend call,
            access_token: Access token for user ad min.
            expected_response: The response we expect when we run the function.
    '''
    del initDatabase

    # get access token for ad min
    access_token = loginHelper(testClient, 'ad', 'min')

    setScoreDB(12, 5.80, 4.60, 4.70, 6.80, 0.01)

    # Run function
    response = testClient.get('/scoreapi/getFilesAndScoresByUser', headers={"Authorization": "Bearer " + access_token})

    # Check if we get the correct status code:
    assert response.status_code == 200

    expected_response = {"id": [],
                         "filename": [],
                         "date": [],
                         "scoreStyle": [],
                         "scoreCohesion": [],
                         "scoreStructure": [],
                         "scoreIntegration": []
                         }

    # Check if the expected response is correct:
    assert json.loads(response.data) == expected_response


def testRetrieveFilesAndScoresDifferentUser(testClient, initDatabase):
    '''
        Test if we can retrieve a file with scores from the database. We first upload a file to the database and
        add the corresponding scores to the scores table. Then, we run the getFilesAndScoresByUser function to
        see if we get the correct response.
        Arguments:
            testClient: The test client we test this for.
            initDatabase: The database instance we test this for.
        Attributes:
            response: The response of the getFilesAndScoresByUser backend call,
            file: File that is added to the database.
            access_token: Access token for user ad min.
            expected_response: The response we expect when we run the function.
    '''
    del initDatabase

    # get access token for ad min
    access_token = loginHelper(testClient, 'ad', 'min')

    # Add file to database
    file = Files(path='C:/normal/path/File-1.pdf', filename='File-1.pdf', date=datetime(2019, 2, 12),
                 userId=1234, courseCode='2IPE0')
    db.session.add(file)
    db.session.commit()

    # Add scores to database
    setScoreDB(file.id, 1.00, 1.00, 1.00, 1.00, 0.01)

    # Run function
    response = testClient.get('/scoreapi/getFilesAndScoresByUser', headers={"Authorization": "Bearer " + access_token})

    # Check if we get the correct status code:
    assert response.status_code == 200

    expected_response = {"id": [],
                         "filename": [],
                         "date": [],
                         "scoreStyle": [],
                         "scoreCohesion": [],
                         "scoreStructure": [],
                         "scoreIntegration": []
                         }

    # Check if the expected response is correct:
    assert json.loads(response.data) == expected_response

