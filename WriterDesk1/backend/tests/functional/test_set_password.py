from app.models import User
from test_set_role import loginHelper

def testSetPassword(testClient, initDatabase):
    '''
    Test if we can properly set the password
    Assumed that currentUser=='Pietje' with current plainTextPassword=='Bell'
    Arguments:
        testClient:   The test client we test this for.
        initDatabase: The database instance we test this for.
    '''
    del initDatabase
    user = User.query.filter_by(username='Pietje').first()

    #check username and password
    assert user.username == 'Pietje'
    assert user.check_password('Bell')

    newPass = 'banaan'

    # get access token for Pietje Bell
    access_token = loginHelper(testClient, 'Pietje', 'Bell')

    # set new password in data
    data = {
        'newPassword':newPass,
        'oldPassword': 'Bell'
    }

    # test response data
    response = testClient.post('/loginapi/setPassword', json=data, headers = {"Authorization": "Bearer " + access_token})
    assert response.status_code == 200
    assert response.data == b'Successfully changed password!'
    assert user.check_password(newPass)

def testSetPasswordIncorrectGiven(testClient, initDatabase):
    '''
    Test if we can indeed do not set the password if we supply an incorrect password.
    Assumed that currentUser=='Pietje' with current plainTextPassword=='Bell'
    Arguments:
        testClient:   The test client we test this for.
        initDatabase: The database instance we test this for.
    '''
    del initDatabase
    user = User.query.filter_by(username='Pietje').first()

    #check username and password
    assert user.username == 'Pietje'
    assert user.check_password('Bell')

    newPass = 'banaan'

    # get access token for Pietje Bell
    access_token = loginHelper(testClient, 'Pietje', 'Bell')

    # set new password in data
    data = {
        'newPassword':newPass,
        'oldPassword': 'Sjaak'
    }

    # test response data:
    response = testClient.post('/loginapi/setPassword', json=data, headers = {"Authorization": "Bearer " + access_token})
    assert response.status_code == 403
    assert response.data == b'Current password is incorrect!'
    # Check if the password is indeed not updated:
    assert user.check_password('Bell')