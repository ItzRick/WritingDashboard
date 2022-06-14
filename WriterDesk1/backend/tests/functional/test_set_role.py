from app.models import User
import json

def loginHelper(testClient, username, password):
    '''
    Support function to log into the server as user with username and password
    Arguments:
        testClient:   The test client we test this for.
        username: 
        password: 
    Attributes:
        data: 
        access_token: 
    return:
        access_token: 
    '''
    data = {
        'username':username,
        'password':password,
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
    
    return access_token

def testSetRole(testClient, initDatabase):
    '''
    Test if we can properly set the role for user 'Pietje'
    Assumed that currentUser=='Pietje' with current role==None
    Arguments:
        testClient:   The test client we test this for.
        initDatabase: The database instance we test this for.
    '''
    del initDatabase
    user = User.query.filter_by(username='Pietje').first()

    #check current role
    assert user.role == None

    userId = user.id

    assert User.query.filter_by(id=userId).first() is not None

    # get access token for the admin who can change the role
    access_token = loginHelper(testClient, 'ad', 'min')

    newRole = 'student'
    # set new role in data
    data = {
        'userId': userId,
        'newRole':newRole
    }

    response = testClient.post('/loginapi/setRole', data=data, headers = {"Authorization": "Bearer " + access_token})
    assert response.status_code == 200
    assert user.role == newRole

def testInvalidUser(testClient, initDatabase):
    '''
    Test if we receive a 404 if we provide a userId not in Users
    Arguments:
        testClient:   The test client we test this for.
        initDatabase: The database instance we test this for.
    '''
    del initDatabase
    # get user id
    userId = -1
    newRole = 'student'

    # make sure it is invalid
    assert User.query.filter_by(id=userId).first() is None

    # get access token for the admin
    access_token = loginHelper(testClient, 'ad', 'min')

    # set data
    data = {
        'userId': userId,
        'newRole':newRole,
    }
    # send to server
    response = testClient.post('/loginapi/setRole', data=data, headers = {"Authorization": "Bearer " + access_token})
    # expect error
    assert response.status_code == 404
    assert response.data == b'user with userId not found'

def testInvalidRole(testClient, initDatabase):
    '''
    Test if we receive a 404 if we provide a role that is not in ['admin', 'participant', 'researcher', 'student']
    Assuming that there exists a valid user
    Arguments:
        testClient:   The test client we test this for.
        initDatabase: The database instance we test this for.
    '''
    del initDatabase
    # get a valid user and id
    user = User.query.first()
    userId = user.id
    newRole = 'fakeRole'

    # get access token for the admin
    access_token = loginHelper(testClient, 'ad', 'min')

    # set new role in data
    data = {
        'userId': userId,
        'newRole':newRole,
    }
    # send to server
    response = testClient.post('/loginapi/setRole', data=data, headers = {"Authorization": "Bearer " + access_token})
    # expect error
    assert response.status_code == 404
    assert response.data == b'Invalid role'


def testNotAdmin(testClient, initDatabase):
    '''
    Test if we are refused access when not in admin mode
    Assumed that currentUser=='Pietje'
    Arguments:
        testClient:   The test client we test this for.
        initDatabase: The database instance we test this for.
    '''
    del initDatabase
    user = User.query.filter_by(username='Pietje').first()

    #check if current username
    assert user.username == 'Pietje'

    userId = user.id

    assert User.query.filter_by(id=userId).first() is not None

    # get access token for Pietje Bell
    access_token = loginHelper(testClient, 'Pietje', 'Bell')

    newRole = 'student'
    # set new role in data
    data = {
        'userId': userId,
        'newRole':newRole
    }
    
    response = testClient.post('/loginapi/setRole', data=data, headers = {"Authorization": "Bearer " + access_token})
    assert response.status_code == 403
    assert response.data == b'Method only accessible for admin users'