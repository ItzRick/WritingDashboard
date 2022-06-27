from app.models import User
from test_set_role import loginHelper

def testSetUsername(testClient, initDatabase):
    '''
    Test if we can properly set the username
    Assumed that currentUser=='Pietje' with current plainTextPassword=='Bell'
    Arguments:
        testClient:   The test client we test this for.
        initDatabase: The database instance we test this for.
    Atributes: 
        user: user pietje
        newUsername: intended new username
        access_token: the access token
        data: intended data for the request
    '''
    del initDatabase
    user = User.query.filter_by(username='Pietje').first()

    #check username and password
    assert user.username == 'Pietje'
    assert user.check_password('Bell')

    newUsername = 'new name'

    # get access token for Pietje Bell
    access_token = loginHelper(testClient, 'Pietje', 'Bell')

    # set new password in data
    data = {
        'currentPassword':'Bell',
        'newUsername': newUsername
    }

    # test response data
    response = testClient.post('/loginapi/setUsername', json=data, headers = {"Authorization": "Bearer " + access_token})
    assert response.status_code == 200
    assert response.data == b'Successfully changed username!'
    assert user.username == newUsername

def testSetUsernameIncorrectPasswordGiven(testClient, initDatabase):
    '''
    Test if we can indeed do not set the username if we supply an incorrect password.
    Assumed that currentUser=='Pietje' with current plainTextPassword=='Bell'
    Arguments:
        testClient:   The test client we test this for.
        initDatabase: The database instance we test this for.
    Atributes: 
        user: user pietje
        newUsername: intended new username
        access_token: the access token
        data: intended data for the request
    '''
    del initDatabase
    user = User.query.filter_by(username='Pietje').first()

    #check username and password
    assert user.username == 'Pietje'
    assert user.check_password('Bell')

    newUsername = 'new name'

    # get access token for Pietje Bell
    access_token = loginHelper(testClient, 'Pietje', 'Bell')

    # set new password in data
    data = {
        'currentPassword':'wrong',
        'newUsername': newUsername
    }

    # test response data:
    response = testClient.post('/loginapi/setUsername', json=data, headers = {"Authorization": "Bearer " + access_token})
    assert response.status_code == 403
    assert response.data == b'Current password is incorrect!'
    # Check if the password is indeed not updated:
    assert user.username == 'Pietje'

def testSetUsernameExistingUsername(testClient, initDatabase):
    '''
    Test if we can indeed do not set the username if we supply an already existing username
    Assumed that currentUser=='Pietje' with current plainTextPassword=='Bell'
    Arguments:
        testClient:   The test client we test this for.
        initDatabase: The database instance we test this for.
    Atributes: 
        user: user pietje
        newUsername: intended new username
        userDonald: another user named Donald
        access_token: the access token
        data: intended data for the request
    '''
    del initDatabase
    user = User.query.filter_by(username='Pietje').first()

    #check username and password
    assert user.username == 'Pietje'
    assert user.check_password('Bell')

    # find the user Donald
    newUsername = 'Donald'
    userDonald = User.query.filter_by(username=newUsername).first()
    assert userDonald is not None

    # get access token for Pietje Bell
    access_token = loginHelper(testClient, 'Pietje', 'Bell')

    # set new password in data
    data = {
        'currentPassword':'Bell',
        'newUsername': newUsername
    }

    # test response data:
    response = testClient.post('/loginapi/setUsername', json=data, headers = {"Authorization": "Bearer " + access_token})
    assert response.status_code == 403
    assert response.data == b'Username is already being used'
    # Check if the password is indeed not updated:
    assert user.username == 'Pietje'

    