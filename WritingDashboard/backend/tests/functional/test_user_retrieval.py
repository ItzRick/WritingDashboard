from app.models import User
from app import db
import json

from test_set_role import loginHelper


def checkUserRet(uid, uName, uRole, data):
    '''
    Checks if uid, uName and uRole is in the data
    Argunments:
        uid: user Id
        uName: user name
        uRole: user role
        data: array of dictionaries containing user data
    Returns:
        Whether data contains an instance with uid, uName an uRole
    '''
    return (
        (any(
            (d['id'] == uid and
            d['username'] == uName and
            d['role'] == uRole)
        in d) for d in data)
    )

def testRetrieveUsers(testClient, initDatabase):
    '''
        This test checks the retrieval of of user data of all users except participants, in a json file.
        Attributes:
            user, user2, user3: Users to be added to the database.
        Arguments:
            testClient:  The test client we test this for.
            initDatabase: the database instance we test this for.
    '''
    del initDatabase
    # We add five users to the database session
    user = User(username='John', password_plaintext='blegh')
    db.session.add(user)
    user2 = User(username='Kevin', password_plaintext='bleh')
    db.session.add(user2)
    user3 = User(username='Samantha', password_plaintext='bleurgh')
    user3.role = 'participant'
    db.session.add(user3)
    db.session.commit()

    assert User.query.filter_by(username='ad').first() is not None

    # get access token for ad
    access_token = loginHelper(testClient, 'ad', 'min')

    # Retrieve the users except for those with the participant role
    response = testClient.get('/usersapi/users', headers={"Authorization": "Bearer " + access_token})

    # Check if we get the correct status_code:
    assert response.status_code == 200

    # Check if the expected response is correct:
    data = json.loads(response.data)
    assert checkUserRet(
        uid=User.query.filter_by(username='Pietje').first().id,
        uName='Pietje',
        uRole='user',
        data=data
    )
    assert checkUserRet(
        uid=User.query.filter_by(username='Donald').first().id,
        uName='Donald',
        uRole='user',
        data=data
    )
    assert checkUserRet(
        uid=User.query.filter_by(username='ad').first().id,
        uName='ad',
        uRole='admin',
        data=data
    )
    assert checkUserRet(
        uid=User.query.filter_by(username='Kevin').first().id,
        uName='Kevin',
        uRole='user',
        data=data
    )

def testNotAdmin(testClient, initDatabase):
    '''
    Test if we are refused access when not in admin mode
    First we login as an Pietje, who is not an admin,
    so should not be able to retrieve users
    Arguments:
        testClient:   The test client we test this for.
        initDatabase: The database instance we test this for.
    Attributes:
        user: user 'Pietje'
        userId: user id of pietje, not an admin
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

    response = testClient.get('/usersapi/users', headers={"Authorization": "Bearer " + access_token})
    assert response.status_code == 403
    assert response.data == b'Method only accessible for admin users'


def testAdmin(testClient, initDatabase):
    '''
    Test if we are allowed access when in admin mode
    First we login as an Ad, who is an admin,
    so should be able to retrieve users
    Arguments:
        testClient:   The test client we test this for.
        initDatabase: The database instance we test this for.
    Attributes:
        user: user 'ad'
        userId: user of admin
        newRole: new proposed and valid role
        access_token: admin's access token
        data: data for request to server
        response: response of setting the role
    '''
    del initDatabase
    user = User.query.filter_by(username='ad').first()
    # get his user id
    userId = user.id

    assert User.query.filter_by(id=userId).first() is not None

    # get access token for Ad
    access_token = loginHelper(testClient, 'ad', 'min')

    response = testClient.get('/usersapi/users', headers={"Authorization": "Bearer " + access_token})
    assert response.status_code == 200
