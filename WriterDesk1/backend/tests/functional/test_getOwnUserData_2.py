from app.models import User, Clicks
from app.database import uploadToDatabase
from test_set_role import loginHelper
from datetime import datetime

def testAdminOneClick(testClient, initDatabase):
    '''
        Tests if a user with the admin role and one click made can 
        download their corresponding user data.
        Attributes:
            admin: a user with the admin role.
            access_token: used for showing that user is logged in.
            url: the url of the test click.
            eventType: the event type of the test click.
            adminClick: the test click related to the admin.
            userId: the id of the admin.
            params: the data for the request.
            response: the response from the request.
            firstRow: the first row in the csv.
            secondRow: the second row in the csv.
            adminClickData: the rows combined.
        Arguments:
            testClient: the test client we test this for.
            initDatabase: the database instance we test this for.
    '''
    del initDatabase

    # make an admin
    admin = User(username='a1', password_plaintext='p1', role='admin')
    uploadToDatabase(admin)

    # check an admin
    assert admin.username == 'a1'
    assert admin.check_password('p1')
    assert admin.role == 'admin'

    # get access token
    access_token = loginHelper(testClient, 'a1', 'p1')

    # make a click
    url='somePage'
    eventType = 'someEventType'
    adminClick = Clicks(admin.id, url, eventType)
    uploadToDatabase(adminClick)

    # check the click
    assert adminClick.userId == admin.id
    assert adminClick.url == url
    assert adminClick.eventType == eventType

    # retrieve and check the user data
    response = testClient.get('/clickapi/getOwnUserData', 
        headers={"Authorization": "Bearer " + access_token})
    assert response.status_code == 200

    # make the csv file as String
    firstRow = 'clickId,userId,timestamp,url,eventType,actionId'
    secondRow = str(adminClick.clickId) + ',' + str(adminClick.userId) + ',' + adminClick.timestamp.strftime('%Y-%m-%d %H:%M:%S.%f') + ',' + adminClick.url + ',' + adminClick.eventType + ',' + (adminClick.actionId or '')
    adminClickData = firstRow + '\n' + secondRow + '\n'
    assert response.data == adminClickData.encode('utf-8')

def testAdminTwoClicks(testClient, initDatabase):
    '''
        Tests if a user with the admin role and two clicks made can 
        download their corresponding user data.
        Attributes:
            admin: a user with the admin role.
            access_token: used for showing that user is logged in.
            url: the url of the test click.
            eventType: the event type of the test click.
            adminClick: the test click related to the admin.
            url1: the url of the test click.
            eventType1: the event type of the test click.
            adminClick1: the test click related to the admin.
            userId: the id of the admin.
            params: the data for the request.
            response: the response from the request.
            firstRow: the first row in the csv.
            secondRow: the second row in the csv.
            thirdRow: the third row in the csv.
            adminClickData: the rows combined.
        Arguments:
            testClient: the test client we test this for.
            initDatabase: the database instance we test this for.
    '''
    del initDatabase

    # make an admin
    admin = User(username='a2', password_plaintext='p1', role='admin')
    uploadToDatabase(admin)

    # check an admin
    assert admin.username == 'a2'
    assert admin.check_password('p1')
    assert admin.role == 'admin'

    # get access token
    access_token = loginHelper(testClient, 'a2', 'p1')

    # make the two clicks
    url='somePage'
    eventType = 'someEventType'
    adminClick = Clicks(admin.id, url, eventType)
    url1='somePage1'
    eventType1 = 'someEventType1'
    adminClick1 = Clicks(admin.id, url1, eventType1)
    uploadToDatabase(adminClick)
    uploadToDatabase(adminClick1)

    # check the two clicks
    assert adminClick.userId == admin.id
    assert adminClick.url == url
    assert adminClick.eventType == eventType
    assert adminClick1.userId == admin.id
    assert adminClick1.url == url1
    assert adminClick1.eventType == eventType1

    # retrieve and check the user data
    response = testClient.get('/clickapi/getOwnUserData', 
        headers={"Authorization": "Bearer " + access_token})
    assert response.status_code == 200

    # make the csv file as String
    firstRow = 'clickId,userId,timestamp,url,eventType,actionId'
    secondRow = str(adminClick.clickId) + ',' + str(adminClick.userId) + ',' + adminClick.timestamp.strftime('%Y-%m-%d %H:%M:%S.%f') + ',' + adminClick.url + ',' + adminClick.eventType + ',' + (adminClick.actionId or '')
    thirdRow = str(adminClick1.clickId) + ',' + str(adminClick1.userId) + ',' + adminClick1.timestamp.strftime('%Y-%m-%d %H:%M:%S.%f') + ',' + adminClick1.url + ',' + adminClick1.eventType + ',' + (adminClick1.actionId or '')
    adminClickData = firstRow + '\n' + secondRow + '\n' + thirdRow + '\n'
    assert response.data == adminClickData.encode('utf-8')

def testNoClicks(testClient, initDatabase):   
    '''
        Tests if a user that has no clicks in the database returns a row with
        only None except for the user id.
        Attributes:
            user: a user with no clicks.
            access_token: used for showing that user is logged in.
            userId: the id of the user.
            params: the data for the request.
            response: the response from the request.
            firstRow: the first row in the csv.
            secondRow: the second row in the csv.
            clickData: the rows combined.
        Arguments:
            testClient: the test client we test this for.
            initDatabase: the database instance we test this for.
    '''
    del initDatabase

    # make a user
    user = User(username='u1', password_plaintext='p1', role='admin')
    uploadToDatabase(user)

    # check a user
    assert user.username == 'u1'
    assert user.check_password('p1')
    assert user.role == 'admin'

    # get access token
    access_token = loginHelper(testClient, 'u1', 'p1')

    # retrieve and check the user data
    response = testClient.get('/clickapi/getOwnUserData', 
        headers={"Authorization": "Bearer " + access_token})
    assert response.status_code == 200

    # make the csv file as String
    firstRow = 'clickId,userId,timestamp,url,eventType,actionId'
    # all columns except for userId are None, so it will just have comma's
    secondRow = ',' + str(user.id) + ',' + ',' + ',' + ','
    clickData = firstRow + '\n' + secondRow + '\n'
    assert response.data == clickData.encode('utf-8')