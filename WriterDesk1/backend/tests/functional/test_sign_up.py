from app.models import User
from app import create_app, db
import json

def testSignUp(testClient, initDatabase):
    '''
        Test if signup gives a 200 status code with a username is not yet in the database
        Attributes:
            data: input username and password for the post request
            response: response of the post request
        Arguments:
            testClient: the test client we test this for
            initDatabase: the database instance we test this for
    '''

    del initDatabase
    data = {
        'username':'testSignUp',
        'password':'SignUp11',
    }

    response = testClient.post('/loginapi/signup', json=data, headers={"Content-Type": "application/json"})
    assert response.status_code == 200

def testSignUpExisting(testClient,initDatabase):
    '''
        Test if signup gives a 400 status code with a username that already exists in the database
        Attributes:
            data: input username and password for the post request
            response: response of the post request
            responseDuplicate: response of a second post request with the same data
        Arguments:
            testClient: the test client we test this for
            initDatabase: the database instance we test this for
    '''

    del initDatabase
    data = {
        'username':'testSignUp',
        'password':'SignUp11',
    }
    
    response = testClient.post('/loginapi/signup', json=data, headers={"Content-Type": "application/json"})
    assert response.status_code == 200
    responseDuplicate = testClient.post('/loginapi/signup', json=data, headers={"Content-Type": "application/json"})
    assert responseDuplicate.status_code == 400