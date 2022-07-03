from flask_jwt_extended import current_user
from test_set_role import loginHelper


def testGetTrackable(testClient, initDatabase):
    '''
        Test if we can retrieve the correct value for trackable from the database. We first get the value for
        user ad min and then change the value in the database for this user to check if we get a different value after.
        Arguments:
            testClient: The test client we test this for.
            initDatabase: The database instance we test this for.
        Attributes:
            response1, response2: The responses of the getTrackable backend calls
            access_token: Access token for user ad min.
    '''
    del initDatabase

    # Get access token for ad min
    access_token = loginHelper(testClient, 'ad', 'min')

    # Get trackable for ad min
    response1 = testClient.get('/loginapi/getTrackable', headers={"Authorization": "Bearer " + access_token})
    # Check if response status code is correct
    assert response1.status_code == 200
    # Check if response data is correct
    assert response1.data == b'yes'

    current_user.trackable = False  # Set trackable to False

    # Get trackable for ad min again
    response2 = testClient.get('/loginapi/getTrackable', headers={"Authorization": "Bearer " + access_token})
    # Check if response status code is correct
    assert response2.status_code == 200
    # Check if response data is correct
    assert response2.data == b'no'


def testSetTrackableChange(testClient, initDatabase):
    '''
        Test if we can set the value of trackable for the current user in the database. We first get the value for
        user ad min and then change the value in the database for this user to check if we get a different value after.
        Arguments:
            testClient: The test client we test this for.
            initDatabase: The database instance we test this for.
        Attributes:
            response1, response2, response2: The responses of the getTrackable and setTrackable backend calls
            access_token: Access token for user ad min.
            data: Data for new trackable value to be set.
    '''
    del initDatabase

    # Get access token for ad min
    access_token = loginHelper(testClient, 'ad', 'min')

    # Get trackable for ad min
    response1 = testClient.get('/loginapi/getTrackable', headers={"Authorization": "Bearer " + access_token})
    # Check if response status code is correct
    assert response1.status_code == 200
    # Check if response data is correct
    assert response1.data == b'yes'

    data = {'newTrackable': 'no'}  # Data for post request

    response2 = testClient.post('/loginapi/setTrackable', data=data, headers={"Authorization": "Bearer " + access_token})
    # Check if response status code is correct
    assert response2.status_code == 200
    # Check if response data is correct
    assert response2.data == b'success'

    # Get trackable for ad min again
    response3 = testClient.get('/loginapi/getTrackable', headers={"Authorization": "Bearer " + access_token})
    # Check if response status code is correct
    assert response3.status_code == 200
    # Check if response data is correct
    assert response3.data == b'no'


def testSetTrackableKeep(testClient, initDatabase):
    '''
        Test if we can set the value of trackable for the current user in the database if it is equal to the current value.
        We first get the value for user ad min and then change the value in the database for this user
        to check if we get the same value after.
        Arguments:
            testClient: The test client we test this for.
            initDatabase: The database instance we test this for.
        Attributes:
            response1, response2, response2: The responses of the getTrackable and setTrackable backend calls
            access_token: Access token for user ad min.
            data: Data for new trackable value to be set.
    '''
    del initDatabase

    # Get access token for ad min
    access_token = loginHelper(testClient, 'ad', 'min')

    # Get trackable for ad min
    response1 = testClient.get('/loginapi/getTrackable', headers={"Authorization": "Bearer " + access_token})
    # Check if response status code is correct
    assert response1.status_code == 200
    # Check if response data is correct
    assert response1.data == b'yes'

    data = {'newTrackable': 'yes'}  # Data for post request

    response2 = testClient.post('/loginapi/setTrackable', data=data, headers={"Authorization": "Bearer " + access_token})
    # Check if response status code is correct
    assert response2.status_code == 200
    # Check if response data is correct
    assert response2.data == b'success'

    # Get trackable for ad min again
    response3 = testClient.get('/loginapi/getTrackable', headers={"Authorization": "Bearer " + access_token})
    # Check if response status code is correct
    assert response3.status_code == 200
    # Check if response data is correct
    assert response3.data == b'yes'


def testSetTrackableError(testClient, initDatabase):
    '''
        Test if we get the correct error value if we try to change trackable with data that is not 'yes' or 'no' .
        We first get the value for user ad min and then change the value to a wrong value and check if
        the value did not change in the database after.
        Arguments:
            testClient: The test client we test this for.
            initDatabase: The database instance we test this for.
        Attributes:
            response1, response2, response2: The responses of the getTrackable and setTrackable backend calls
            access_token: Access token for user ad min.
            data: Data for new trackable value to be set.
    '''
    del initDatabase

    # Get access token for ad min
    access_token = loginHelper(testClient, 'ad', 'min')

    # Get trackable for ad min
    response1 = testClient.get('/loginapi/getTrackable', headers={"Authorization": "Bearer " + access_token})
    # Check if response status code is correct
    assert response1.status_code == 200
    # Check if response data is correct
    assert response1.data == b'yes'

    data = {'newTrackable': 'SomeText'}  # Data for post request

    response2 = testClient.post('/loginapi/setTrackable', data=data, headers={"Authorization": "Bearer " + access_token})
    # Check if response status code is correct
    assert response2.status_code == 400
    # Check if response data is correct
    assert response2.data == b'newTrackable is not yes or no'

    # Get trackable for ad min again
    response3 = testClient.get('/loginapi/getTrackable', headers={"Authorization": "Bearer " + access_token})
    # Check if response status code is correct
    assert response3.status_code == 200
    # Check if response data is correct
    assert response3.data == b'yes'

