from app.models import Explanations
import json
from app import db
from decimal import Decimal

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