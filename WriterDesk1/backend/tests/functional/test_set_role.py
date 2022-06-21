from app.models import User
import json

def loginHelper(testClient, username, password):
    '''
    Support function to log into the server as user with username and password
    and get the access_token
    Arguments:
        testClient:   The test client we test this for.
        username: username of the user we want the access_token from
        password: password of the user we want the access_token from
    Attributes:
        data: data for login
        responseLogin: response from logging in
        access_token: the access token
        responseAccess: response from checking if token is correct
    return:
        access_token: token needed to run locked jwt functions
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
    responseAccess = testClient.get('/loginapi/protected', headers = {"Authorization": "Bearer " + access_token})
    # Check if we got the correct status code
    assert responseAccess.status_code == 200
    
    return access_token

def testSetRole(testClient, initDatabase):
    '''
    Test if we can properly set the role for user 'Pietje'
    First we login as an admin, to then proceed to change the role
    Arguments:
        testClient:   The test client we test this for.
        initDatabase: The database instance we test this for.
    Attributes:
        user: user instance of 'Pietje'
        userId: user id of 'Pietje'
        newRole: new proposed and valid role
        access_token: admin's access token
        data: data for request to server
        response: response of setting the role
    '''
    del initDatabase
    # get user pietje
    user = User.query.filter_by(username='Pietje').first()
    #check current role
    assert user.role == 'user'
    # set user id and new role
    userId = user.id
    newRole = 'student'

    # get access token for the admin who can change the role
    access_token = loginHelper(testClient, 'ad', 'min')
    
    # set new role in data
    data = {
        'userId': userId,
        'newRole':newRole
    }

    # check response data
    response = testClient.post('/loginapi/setRole', data=data, headers = {"Authorization": "Bearer " + access_token})
    assert response.status_code == 200
    assert user.role == newRole

def testInvalidUser(testClient, initDatabase):
    '''
    Test if we receive a 404 if we provide a userId not in Users
    First we login as an admin, to then proceed to change the role
    Arguments:
        testClient:   The test client we test this for.
        initDatabase: The database instance we test this for.
    Attributes:
        userId: invalid user id
        newRole: new proposed and valid role
        access_token: admin's access token
        data: data for request to server
        response: response of setting the role
    '''
    del initDatabase
    # make up a probably invalid user id
    userId = -1
    newRole = 'student'

    # make sure the userId is invalid
    assert User.query.filter_by(id=userId).first() is None

    # get access token for the admin
    access_token = loginHelper(testClient, 'ad', 'min')

    # set data
    data = {
        'userId': userId,
        'newRole': newRole,
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
    First we login as an admin, to then proceed to change the role
    Arguments:
        testClient:   The test client we test this for.
        initDatabase: The database instance we test this for.
    Attributes:
        user: user instance of 'Pietje'
        userId: invalid user id
        access_token: admin's access token
        newRole: new proposed and valid role
        response: response of setting the role
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
    First we login as an Pietje, who is not an admin, 
    so should not be able to change the role
    Arguments:
        testClient:   The test client we test this for.
        initDatabase: The database instance we test this for.
    Attributes:
        user: user 'Pietje'
        userId: invalid user id
        newRole: new proposed and valid role
        access_token: admin's access token
        data: data for request to server
        response: response of setting the role
    '''
    del initDatabase
    user = User.query.filter_by(username='Pietje').first()
    # get his user id
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