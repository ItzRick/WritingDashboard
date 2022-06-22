from app.models import User, Clicks
from test_set_role import loginHelper
from app.database import uploadToDatabase

def testZeroUsers(testClient, initDatabase):
    '''
        Tests if an admin that selects zero users gets an error when trying to 
        download the user data.
        Attributes:
            admin: a user with the admin role.
            access_token: used for showing that user is logged in.
            users: list containing the user ids of the users user
            data will be downloaded for
            params: the data for the request.
            response: the response from the request.
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

    users = []
    params = {
        'userId': users,
    }
    response = testClient.get('/clickapi/getUserData', 
        query_string=params, 
        headers={"Authorization": "Bearer " + access_token})
    assert response.status_code == 400
    assert response.data == 'Select at least one user'.encode('utf-8')

def testOneUser(testClient, initDatabase):
    '''
        Tests if an admin that selects one user gets the user data of that user.
        Attributes:
            admin: a user with the admin role.
            access_token: used for showing that user is logged in.
            user: a user to get the user data from.
            url: the url of the test click.
            eventType: the event type of the test click.
            userClick: the test click related to the user.
            users: list containing the user ids of the users user data will be 
            downloaded for
            params: the data for the request.
            response: the response from the request.
            firstRow: the first row in the csv.
            secondRow: the second row in the csv.
            participantsClickData: the rows combined.
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

    # make a user
    user = User(username='u1', password_plaintext='p1')
    uploadToDatabase(user)

    # check a user
    assert user.username == 'u1'
    assert user.check_password('p1')
    assert user.role == 'user'

    # make a click
    url='somePage'
    eventType = 'someEventType'
    userClick = Clicks(user.id, url, eventType)
    uploadToDatabase(userClick)

    # check the click
    assert userClick.userId == user.id
    assert userClick.url == url
    assert userClick.eventType == eventType

    # retrieve and check the data
    users = [user.id]
    params = {
        'userId': users,
    }
    response = testClient.get('/clickapi/getUserData', 
        query_string=params, 
        headers={"Authorization": "Bearer " + access_token})
    assert response.status_code == 200

    # make the csv file as String
    firstRow = 'clickId,userId,timestamp,url,eventType,actionId'
    secondRow = str(userClick.clickId) + ',' + str(userClick.userId) + ',' + userClick.timestamp.strftime('%Y-%m-%d %H:%M:%S.%f') + ',' + userClick.url + ',' + userClick.eventType + ',' + (userClick.actionId or '')
    usersClickData = firstRow + '\n' + secondRow + '\n'
    assert response.data == usersClickData.encode('utf-8')

def testTwoUsers(testClient, initDatabase):
    '''
        Tests if an admin that selects two users gets the user data of that 
        user.
        Attributes:
            admin: a user with the admin role.
            access_token: used for showing that user is logged in.
            user: a user to get the user data from.
            user1: a user to get the user data from.
            url: the url of the test click.
            eventType: the event type of the test click.
            userClick: the test click related to the user.
            url1: the url of the test click.
            eventType1: the event type of the test click.
            userClick1: the test click related to the user.
            users: list containing the user ids of the users user data will be 
            downloaded for
            params: the data for the request.
            response: the response from the request.
            firstRow: the first row in the csv.
            secondRow: the second row in the csv.
            thidRow: the third row in the csv.
            participantsClickData: the rows combined.
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

    # make two users
    user = User(username='u1', password_plaintext='p1')
    user1 = User(username='u2', password_plaintext='p1')
    uploadToDatabase(user)
    uploadToDatabase(user1)

    # check two users
    assert user.username == 'u1'
    assert user.check_password('p1')
    assert user.role == 'user'
    assert user1.username == 'u2'
    assert user1.check_password('p1')
    assert user1.role == 'user'

    # make two clicks
    url='somePage'
    eventType = 'someEventType'
    userClick = Clicks(user.id, url, eventType)
    url1='somePage'
    eventType1 = 'someEventType'
    userClick1 = Clicks(user1.id, url1, eventType1)
    uploadToDatabase(userClick)
    uploadToDatabase(userClick1)

    # check two clicks
    assert userClick.userId == user.id
    assert userClick.url == url
    assert userClick.eventType == eventType
    assert userClick1.userId == user1.id
    assert userClick1.url == url1
    assert userClick1.eventType == eventType1

    # retrieve and check the data
    users = [user.id, user1.id]
    params = {
        'userId': users,
    }
    response = testClient.get('/clickapi/getUserData', 
        query_string=params, 
        headers={"Authorization": "Bearer " + access_token})
    assert response.status_code == 200

    # make the csv file as String
    firstRow = 'clickId,userId,timestamp,url,eventType,actionId'
    secondRow = str(userClick.clickId) + ',' + str(userClick.userId) + ',' + userClick.timestamp.strftime('%Y-%m-%d %H:%M:%S.%f') + ',' + userClick.url + ',' + userClick.eventType + ',' + (userClick.actionId or '')
    thirdRow = str(userClick1.clickId) + ',' + str(userClick1.userId) + ',' + userClick1.timestamp.strftime('%Y-%m-%d %H:%M:%S.%f') + ',' + userClick1.url + ',' + userClick1.eventType + ',' + (userClick1.actionId or '')
    usersClickData = firstRow + '\n' + secondRow + '\n' + thirdRow + '\n'
    assert response.data == usersClickData.encode('utf-8')

def testNoUserData(testClient, initDatabase):
    '''
        Tests if an admin that selects one users gets the user data of
        that users. The user data of the users is None except for
        the user id of the users.
        Attributes:
            admin: a user with the admin role.
            access_token: used for showing that user is logged in.
            users: a user with the participant role.
            users: list containing the user ids of the users user data will be 
            downloaded for
            params: the data for the request.
            response: the response from the request.
            firstRow: the first row in the csv.
            secondRow: the second row in the csv.
            usersClickData: the rows combined.
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

    # make a participant
    user = User(username='u1', password_plaintext='p1')
    uploadToDatabase(user)

    # check a participant
    assert user.username == 'u1'
    assert user.check_password('p1')
    assert user.role == 'user'

    # retrieve and check the data
    users = [user.id]
    params = {
        'userId': users,
    }
    response = testClient.get('/clickapi/getUserData', 
        query_string=params, 
        headers={"Authorization": "Bearer " + access_token})
    assert response.status_code == 200

    # make the csv file as String
    firstRow = 'clickId,userId,timestamp,url,eventType,actionId'
    # all columns except for userId are None, so it will just have comma's
    secondRow = ',' + str(user.id) + ',' + ',' + ',' + ','
    usersClickData = firstRow + '\n' + secondRow + '\n'
    assert response.data == usersClickData.encode('utf-8')

def testNoAccessStudent(testClient, initDatabase):
    '''
        Tests if a student does not have access to retrieving the user data of
        users.
        Attributes:
            student: a user with the student role.
            access_token: used for showing that user is logged in.
            response: the response from the request.
        Arguments:
            testClient: the test client we test this for.
            initDatabase: the database instance we test this for.
    '''
    del initDatabase

    # make a student
    student = User(username='s1', password_plaintext='p1', role='student')
    uploadToDatabase(student)

    # check a student
    assert student.username == 's1'
    assert student.check_password('p1')
    assert student.role == 'student'

    # get access token
    access_token = loginHelper(testClient, 's1', 'p1')

    response = testClient.get('/clickapi/getUserData', 
        headers={"Authorization": "Bearer " + access_token})
    assert response.status_code == 403
    assert response.data == 'Method only accessible for admin users'.encode('utf-8')

def testNoAccessParticipant(testClient, initDatabase):
    '''
        Tests if a participant does not have access to retrieving the user 
        data of users.
        Attributes:
            participant: a user with the participant role.
            access_token: used for showing that user is logged in.
            response: the response from the request.
        Arguments:
            testClient: the test client we test this for.
            initDatabase: the database instance we test this for.
    '''
    del initDatabase

    # make a participant
    participant = User(username='p1', password_plaintext='p1', role='participant')
    uploadToDatabase(participant)

    # check a participant
    assert participant.username == 'p1'
    assert participant.check_password('p1')
    assert participant.role == 'participant'

    # get access token
    access_token = loginHelper(testClient, 'p1', 'p1')

    response = testClient.get('/clickapi/getUserData', 
        headers={"Authorization": "Bearer " + access_token})
    assert response.status_code == 403
    assert response.data == 'Method only accessible for admin users'.encode('utf-8')

def testNoAccessResearcher(testClient, initDatabase):
    '''
        Tests if a researcher does not have access to retrieving the user data 
        of users.
        Attributes:
            researcher: a user with the researcher role.
            access_token: used for showing that user is logged in.
            response: the response from the request.
        Arguments:
            testClient: the test client we test this for.
            initDatabase: the database instance we test this for.
    '''
    del initDatabase

    # make a researcher
    researcher = User(username='r1', password_plaintext='p1', role='researcher')
    uploadToDatabase(researcher)

    # check a researcher
    assert researcher.username == 'r1'
    assert researcher.check_password('p1')
    assert researcher.role == 'researcher'

    # get access token
    access_token = loginHelper(testClient, 'r1', 'p1')

    response = testClient.get('/clickapi/getUserData', 
        headers={"Authorization": "Bearer " + access_token})
    assert response.status_code == 403
    assert response.data == 'Method only accessible for admin users'.encode('utf-8')