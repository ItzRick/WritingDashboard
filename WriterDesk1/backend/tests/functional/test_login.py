from app.models import User
from app import create_app, db
import json

def test_valid_login(testClient, initDatabase):
    '''
    Test if login works with a valid username and password
    Arguments:
        testClient:  The test client we test this for.
        initDatabase: the database instance we test this for.
    '''

    del initDatabase
    data = {
        'username':'Pietje',
        'password':'Bell',
    }

    response = testClient.post('/loginapi/login', json=data, headers={"Content-Type": "application/json"})
    assert response.status_code == 200

def test_invalid_login(testClient,initDatabase):
    '''
    Test if login gives a 403 status code with an invalid username and password
    Arguments:
        testClient:  The test client we test this for.
        initDatabase: the database instance we test this for.
    '''
    del initDatabase
    data = {
        'username':'Pietje',
        'password':'Duck',
    }

    response = testClient.post('/loginapi/login', json=data, headers={"Content-Type": "application/json"})
    assert response.status_code == 403

def test_authenticated(testClient, initDatabase):
    '''
    Test if we can use access_token to authorise using proteced route
    Arguments:
        testClient:  The test client we test this for.
        initDatabase: the database instance we test this for.
    '''
    del initDatabase

    data = {
        'username':'Pietje',
        'password':'Bell',
    }

    # Login request
    responseLogin = testClient.post('/loginapi/login', json=data, headers={"Content-Type": "application/json"})
    # Check if we got the correct status code -> login was successfull
    assert responseLogin.status_code == 200

    # Get access token, which we got from login request
    access_token = json.loads(responseLogin.data)['access_token']

    # Request with authorization header containing access token
    response = testClient.get('/loginapi/protected', headers = {"Authorization": "Bearer " + access_token})
    # Check if we got the correct status code
    assert response.status_code == 200
