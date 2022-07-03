from app.models import Explanations, Files
import json
from app import db

from test_set_role import loginHelper

def testGetExplanationByFileAndTypeSingle(testClient, initDatabaseEmpty):
    '''
        Test to check if we can retrieve a single explanation.
        Attributes:
            expl1: Explanation that is added to the database.
            data: The data sent with the request.
            response: The response of the backend call.
            expectedResponse: The response we expect to get from the function.
        Arguments:
            testClient: The test client we test this for.
            initDatabaseEmpty: The database instance we test this for.
    '''
    del initDatabaseEmpty

    # Create explanation that is going to be added to the database
    expl1 = Explanations(fileId=63, explId=12, type=0, explanation='This is an explanation',
                         mistakeText='A mistake', X1=300, X2=350, Y1=100, Y2=120,
                         replacement1='', replacement2='', replacement3='', feedbackVersion=0.01)

    # Add to the database
    db.session.add(expl1)
    db.session.commit()

    # Data for get request
    data = {
        'fileId': 63,
        'type': 0
    }

    # Retrieve the explanations for the given file and type
    response = testClient.get('/scoreapi/getExplanationForFileAndType', query_string=data)
    # Check if we get the correct status_code:
    assert response.status_code == 200

    expectedResponse = [{'fileId': 63, 'explId': 12, 'type': 0, 'explanation': 'This is an explanation',
                        'mistakeText': 'A mistake', 'X1': 300.0, 'X2': 350.0, 'Y1': 100.0, 'Y2': 120.0,
                         'replacement1': '', 'replacement2': '', 'replacement3': '', 'feedbackVersion': '0.01'}]

    # Check response
    assert json.loads(response.data) == expectedResponse


def testGetExplanationByFileAndTypeMultiple(testClient, initDatabaseEmpty):
    '''
        Test to check if we can retrieve multiple explanations from a single file and with a single type.
        Attributes:
            expl1, expl2: Explanations that are added to the database.
            data: The data sent with the request.
            response: The response of the backend call.
            expectedResponse: The response we expect to get from the function.
        Arguments:
            testClient: The test client we test this for.
            initDatabaseEmpty: The database instance we test this for.
    '''
    del initDatabaseEmpty

    # Create explanations that are going to be added to the database
    expl1 = Explanations(fileId=63, explId=12, type=0, explanation='This is an explanation',
                         mistakeText='Mistake 1', X1=200, X2=350, Y1=900, Y2=910,
                         replacement1='Replacement1', replacement2='Replacement2', replacement3='', feedbackVersion=0.01)
    expl2 = Explanations(fileId=63, explId=15, type=0, explanation='This is an explanation',
                         mistakeText='Mistake 2', X1=300, X2=350, Y1=100, Y2=120,
                         replacement1='Replacement1', replacement2='', replacement3='', feedbackVersion=0.01)
    # Add to the database
    db.session.add(expl1)
    db.session.add(expl2)
    db.session.commit()

    # Data for get request
    data = {
        'fileId': 63,
        'type': 0
    }

    # Retrieve the explanations for the given file and type
    response = testClient.get('/scoreapi/getExplanationForFileAndType', query_string=data)
    # Check if we get the correct status_code:
    assert response.status_code == 200

    expectedResponse = [{'fileId': 63, 'explId': 12, 'type': 0, 'explanation': 'This is an explanation',
                        'mistakeText': 'Mistake 1', 'X1': 200.0, 'X2': 350.0, 'Y1': 900.0, 'Y2': 910.0,
                         'replacement1': 'Replacement1', 'replacement2': 'Replacement2', 'replacement3': '', 'feedbackVersion': '0.01'},
                        {'fileId': 63, 'explId': 15, 'type': 0, 'explanation': 'This is an explanation',
                         'mistakeText': 'Mistake 2', 'X1': 300.0, 'X2': 350.0, 'Y1': 100.0, 'Y2': 120.0,
                         'replacement1': 'Replacement1', 'replacement2': '', 'replacement3': '', 'feedbackVersion': '0.01'}
                        ]

    # Check response
    assert json.loads(response.data) == expectedResponse


def testGetExplanationByFileAndTypeMultipleFiles(testClient, initDatabaseEmpty):
    '''
        Test to check if we can retrieve a single explanations when there are multiple
        explanations with different fileIds in the database.
        Attributes:
            expl1, expl2: Explanations that are added to the database.
            data: The data sent with the request.
            response: The response of the backend call.
            expectedResponse: The response we expect to get from the function.
        Arguments:
            testClient: The test client we test this for.
            initDatabaseEmpty: The database instance we test this for.
    '''
    del initDatabaseEmpty

    # Create explanations that are going to be added to the database
    expl1 = Explanations(fileId=63, explId=12, type=0, explanation='This is an explanation',
                         mistakeText='Mistake 1', X1=200, X2=350, Y1=900, Y2=910,
                         replacement1='Replacement1', replacement2='Replacement2', replacement3='', feedbackVersion=0.01)
    expl2 = Explanations(fileId=65, explId=15, type=0, explanation='This is an explanation',
                         mistakeText='Mistake 2', X1=300, X2=350, Y1=100, Y2=120,
                         replacement1='Replacement1', replacement2='', replacement3='', feedbackVersion=0.01)
    # Add to the database
    db.session.add(expl1)
    db.session.add(expl2)
    db.session.commit()

    # Data for get request
    data = {
        'fileId': 63,
        'type': 0
    }

    # Retrieve the explanations for the given file and type
    response = testClient.get('/scoreapi/getExplanationForFileAndType', query_string=data)
    # Check if we get the correct status_code:
    assert response.status_code == 200

    expectedResponse = [{'fileId': 63, 'explId': 12, 'type': 0, 'explanation': 'This is an explanation',
                        'mistakeText': 'Mistake 1', 'X1': 200.0, 'X2': 350.0, 'Y1': 900.0, 'Y2': 910.0,
                         'replacement1': 'Replacement1', 'replacement2': 'Replacement2', 'replacement3': '', 'feedbackVersion': '0.01'}
                        ]

    # Check response
    assert json.loads(response.data) == expectedResponse


def testGetExplanationByFileAndTypeMultipleTypes(testClient, initDatabaseEmpty):
    '''
        Test to check if we can retrieve a single explanations when there are multiple
        explanations with different types in the database.
        Attributes:
            expl1, expl2: Explanations that are added to the database.
            data: The data sent with the request.
            response: The response of the backend call.
            expectedResponse: The response we expect to get from the function.
        Arguments:
            testClient: The test client we test this for.
            initDatabaseEmpty: The database instance we test this for.
    '''
    del initDatabaseEmpty

    # Create explanations that are going to be added to the database
    expl1 = Explanations(fileId=63, explId=12, type=0, explanation='This is an explanation',
                         mistakeText='Mistake 1', X1=200, X2=350, Y1=900, Y2=910,
                         replacement1='Replacement1', replacement2='Replacement2', replacement3='', feedbackVersion=0.01)
    expl2 = Explanations(fileId=63, explId=15, type=1, explanation='This is an explanation',
                         mistakeText='Mistake 2', X1=300, X2=350, Y1=100, Y2=120,
                         replacement1='Replacement1', replacement2='', replacement3='', feedbackVersion=0.01)
    # Add to the database
    db.session.add(expl1)
    db.session.add(expl2)
    db.session.commit()

    # Data for get request
    data = {
        'fileId': 63,
        'type': 0
    }

    # Retrieve the explanations for the given file and type
    response = testClient.get('/scoreapi/getExplanationForFileAndType', query_string=data)
    # Check if we get the correct status_code:
    assert response.status_code == 200

    expectedResponse = [{'fileId': 63, 'explId': 12, 'type': 0, 'explanation': 'This is an explanation',
                        'mistakeText': 'Mistake 1', 'X1': 200.0, 'X2': 350.0, 'Y1': 900.0, 'Y2': 910.0,
                         'replacement1': 'Replacement1', 'replacement2': 'Replacement2', 'replacement3': '', 'feedbackVersion': '0.01'}
                        ]

    # Check response
    assert json.loads(response.data) == expectedResponse


def testGetExplanationByFileAndTypeError(testClient, initDatabaseEmpty):
    '''
        Test to check if we retrieve a 400 error if there does not exist an explanation
        in the database with the given fileId and type.
        Attributes:
            expl1, expl2: Explanations that are added to the database.
            data: The data sent with the request.
            response: The response of the backend call.
            expectedResponse: The response we expect to get from the function.
        Arguments:
            testClient: The test client we test this for.
            initDatabaseEmpty: The database instance we test this for.
    '''
    del initDatabaseEmpty

    # Data for get request
    data = {
        'fileId': 63,
        'type': 0
    }

    # Retrieve the explanations for the given file and type
    response = testClient.get('/scoreapi/getExplanationForFileAndType', query_string=data)
    # Check if we get the correct status_code:
    assert response.status_code == 400

    expectedResponse = b'No explanations found with matching fileId and type'

    # Check response
    assert response.data == expectedResponse


def testGetExplanationByFileErrorNoneAvailable(testClient, initDatabaseEmpty):
    '''
        Test to check if we retrieve a 400 error if there does not exist an explanation
        in the database with the given fileId
        Attributes:
            fileId: the id of the file, should not exist
            data: The data sent with the request.
            response: The response of the backend call.
        Arguments:
            testClient: The test client we test this for.
            initDatabaseEmpty: The database instance we test this for.
    '''
    del initDatabaseEmpty
    fileId = 630
    assert Files.query.filter_by(id=fileId).first() is None

    # Data for get request
    data = {
        'fileId': fileId,
    }

    # get access token for the regular user
    access_token = loginHelper(testClient, 'ad', 'min')

    # Retrieve the explanations for the given file and type
    response = testClient.get('/scoreapi/getExplanationForFile', query_string=data, headers={"Authorization": "Bearer " + access_token})
    # Check if we get the correct status_code:
    assert response.status_code == 400

    # Check response
    assert response.data == b'No explanations found with matching fileId'

def testGetExplanationByFileWorking(testClient, initDatabaseEmpty):
    '''
        Test to check if, when there is data, if the file works
        Attributes:
            fileId: the id of the file, should not exist
            data: The data sent with the request.
            response: The response of the backend call.
        Arguments:
            testClient: The test client we test this for.
            initDatabaseEmpty: The database instance we test this for.
    '''
    del initDatabaseEmpty

    # Create explanations that are going to be added to the database
    expl1 = Explanations(fileId=63, explId=12, type=0, explanation='This is an explanation',
                         mistakeText='Mistake 1', X1=200, X2=350, Y1=900, Y2=910,
                         replacement1='Replacement1', replacement2='Replacement2', replacement3='', feedbackVersion=0.01)
    expl2 = Explanations(fileId=63, explId=15, type=1, explanation='This is an explanation',
                         mistakeText='Mistake 2', X1=300, X2=350, Y1=100, Y2=120,
                         replacement1='Replacement1', replacement2='', replacement3='', feedbackVersion=0.01)
    # Add to the database
    db.session.add(expl1)
    db.session.add(expl2)
    db.session.commit()

    fileId = 63
    assert Files.query.filter_by(id=fileId).first() is None

    # Data for get request
    data = {
        'fileId': fileId,
    }

    # get access token for the regular user
    access_token = loginHelper(testClient, 'ad', 'min')

    # Retrieve the explanations for the given file and type
    response = testClient.get('/scoreapi/getExplanationForFile', query_string=data, headers={"Authorization": "Bearer " + access_token})
    # Check if we get the correct status_code:
    assert response.status_code == 200

    expectedResponse = [{'fileId': 63, 'explId': 12, 'type': 0, 'explanation': 'This is an explanation',
                        'mistakeText': 'Mistake 1', 'X1': 200.0, 'X2': 350.0, 'Y1': 900.0, 'Y2': 910.0,
                         'replacement1': 'Replacement1', 'replacement2': 'Replacement2', 'replacement3': '', 'feedbackVersion': '0.01'}
                        ]


def testGetExplanationByFileAndCoordsSingle(testClient, initDatabaseEmpty):
    '''
        Test to check if we can retrieve a single explanation by fileId and coordinates.
        Attributes:
            expl1: Explanation that is added to the database.
            data: The data sent with the request.
            response: The response of the backend call.
            expectedResponse: The response we expect to get from the function.
        Arguments:
            testClient: The test client we test this for.
            initDatabaseEmpty: The database instance we test this for.
    '''
    del initDatabaseEmpty

    # Create explanation that is going to be added to the database
    expl1 = Explanations(fileId=63, explId=12, type=0, explanation='This is an explanation',
                         mistakeText='A mistake', X1=300, X2=350, Y1=100, Y2=120,
                         replacement1='', replacement2='', replacement3='', feedbackVersion=0.01)

    # Add to the database
    db.session.add(expl1)
    db.session.commit()

    # Data for get request
    data = {
        'fileId': 63,
        'x': 320,
        'y': 110
    }

    # Retrieve the explanations for the given file and coordinates
    response = testClient.get('/scoreapi/getExplanationForFileAndCoordinates', query_string=data)
    # Check if we get the correct status_code:
    assert response.status_code == 200

    expectedResponse = [{'fileId': 63, 'explId': 12, 'type': 0, 'explanation': 'This is an explanation',
                        'mistakeText': 'A mistake', 'X1': 300.0, 'X2': 350.0, 'Y1': 100.0, 'Y2': 120.0,
                         'replacement1': '', 'replacement2': '', 'replacement3': '', 'feedbackVersion': '0.01'}]

    # Check response
    assert json.loads(response.data) == expectedResponse


def testGetExplanationByFileAndCoordsMultiple(testClient, initDatabaseEmpty):
    '''
        Test to check if we can retrieve multiple explanations from a single file with matching coordinates.
        Attributes:
            expl1, expl2: Explanations that are added to the database.
            data: The data sent with the request.
            response: The response of the backend call.
            expectedResponse: The response we expect to get from the function.
        Arguments:
            testClient: The test client we test this for.
            initDatabaseEmpty: The database instance we test this for.
    '''
    del initDatabaseEmpty

    # Create explanation that is going to be added to the database
    expl1 = Explanations(fileId=10, explId=55, type=0, explanation='This is an explanation',
                         mistakeText='A mistake', X1=300, X2=350, Y1=100, Y2=120,
                         replacement1='', replacement2='', replacement3='', feedbackVersion=0.01)
    expl2 = Explanations(fileId=10, explId=56, type=1, explanation='This is an explanation',
                         mistakeText='Mistake 2', X1=300, X2=330, Y1=60, Y2=115,
                         replacement1='Replacement1', replacement2='', replacement3='', feedbackVersion=0.01)

    # Add to the database
    db.session.add(expl1)
    db.session.add(expl2)
    db.session.commit()

    # Data for get request
    data = {
        'fileId': 10,
        'x': 320,
        'y': 110
    }

    # Retrieve the explanations for the given file and coordinates
    response = testClient.get('/scoreapi/getExplanationForFileAndCoordinates', query_string=data)
    # Check if we get the correct status_code:
    assert response.status_code == 200

    expectedResponse = [{'fileId': 10, 'explId': 56, 'type': 1, 'explanation': 'This is an explanation',
                         'mistakeText': 'Mistake 2', 'X1': 300.0, 'X2': 330.0, 'Y1': 60.0, 'Y2': 115.0,
                         'replacement1': 'Replacement1', 'replacement2': '', 'replacement3': '',
                         'feedbackVersion': '0.01'},
                        {'fileId': 10, 'explId': 55, 'type': 0, 'explanation': 'This is an explanation',
                        'mistakeText': 'A mistake', 'X1': 300.0, 'X2': 350.0, 'Y1': 100.0, 'Y2': 120.0,
                         'replacement1': '', 'replacement2': '', 'replacement3': '', 'feedbackVersion': '0.01'}]

    # Check response
    assert json.loads(response.data) == expectedResponse


def testGetExplanationByFileAndCoordsError(testClient, initDatabaseEmpty):
    '''
        Test to check if we retrieve a 400 error if there does not exist an explanation
        in the database with the given fileId and coordinates.
        Attributes:
            data: The data sent with the request.
            response: The response of the backend call.
            expectedResponse: The response we expect to get from the function.
        Arguments:
            testClient: The test client we test this for.
            initDatabaseEmpty: The database instance we test this for.
    '''
    del initDatabaseEmpty

    # Data for get request
    data = {
        'fileId': 10,
        'x': 320,
        'y': 110
    }

    # Retrieve the explanations for the given file and coordinates
    response = testClient.get('/scoreapi/getExplanationForFileAndCoordinates', query_string=data)
    # Check if we get the correct status_code:
    assert response.status_code == 400

    expectedResponse = b'No explanations found with matching fileId and coordinates'

    # Check response
    assert response.data == expectedResponse
