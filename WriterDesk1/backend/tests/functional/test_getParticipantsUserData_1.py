from app.models import User, Clicks
from test_set_role import loginHelper
from app.database import uploadToDatabase

def testZeroParticipantsResearcher(testClient, initDatabase):
    '''
        Tests if a researcher that selects zero participants gets an error
        when trying to download the user data.
        Attributes:
            researcher: a user with the researcher role.
            access_token: used for showing that user is logged in.
            participants: list containing the user ids of the participants user
            data will be downloaded for
            params: the data for the request.
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

    participants = []
    params = {
        'userId': participants,
    }
    response = testClient.get('/clickapi/getParticipantsUserData', 
        query_string=params, 
        headers={"Authorization": "Bearer " + access_token})
    assert response.status_code == 400
    assert response.data == 'Select at least one participant'.encode('utf-8')

def testOneParticipantResearcher(testClient, initDatabase):
    '''
        Tests if a researcher that selects one participant gets the user data of
        that participant.
        Attributes:
            researcher: a user with the researcher role.
            access_token: used for showing that user is logged in.
            participant: a user with the participant role.
            url: the url of the test click.
            eventType: the event type of the test click.
            participantClick: the test click related to the participant.
            participants: list containing the user ids of the participants user
            data will be downloaded for
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

    # make a researcher
    researcher = User(username='r1', password_plaintext='p1', role='researcher')
    uploadToDatabase(researcher)

    # check a researcher
    assert researcher.username == 'r1'
    assert researcher.check_password('p1')
    assert researcher.role == 'researcher'

    # get access token
    access_token = loginHelper(testClient, 'r1', 'p1')

    # make a participant
    participant = User(username='p1', password_plaintext='p1', role='participant')
    uploadToDatabase(participant)

    # check a participant
    assert participant.username == 'p1'
    assert participant.check_password('p1')
    assert participant.role == 'participant'

    # make a click
    url='somePage'
    eventType = 'someEventType'
    participantClick = Clicks(participant.id, url, eventType)
    uploadToDatabase(participantClick)

    # check the click
    assert participantClick.userId == participant.id
    assert participantClick.url == url
    assert participantClick.eventType == eventType

    # retrieve and check the data
    participants = [participant.id]
    params = {
        'userId': participants,
    }
    response = testClient.get('/clickapi/getParticipantsUserData', 
        query_string=params, 
        headers={"Authorization": "Bearer " + access_token})
    assert response.status_code == 200

    # make the csv file as String
    firstRow = 'clickId,userId,timestamp,url,eventType,actionId'
    secondRow = str(participantClick.clickId) + ',' + str(participantClick.userId) + ',' + participantClick.timestamp.strftime('%Y-%m-%d %H:%M:%S.%f') + ',' + participantClick.url + ',' + participantClick.eventType + ',' + (participantClick.actionId or '')
    participantsClickData = firstRow + '\n' + secondRow + '\n'
    assert response.data == participantsClickData.encode('utf-8')

def testTwoParticipantsResearcher(testClient, initDatabase):
    '''
        Tests if a researcher that selects two participants gets the user data 
        of that participant.
        Attributes:
            researcher: a user with the researcher role.
            access_token: used for showing that user is logged in.
            participant: a user with the participant role.
            url: the url of the test click.
            eventType: the event type of the test click.
            participantClick: the test click related to the participant.
            participant1: a user with the participant role.
            url1: the url of the test click.
            eventType1: the event type of the test click.
            participantClick1: the test click related to the participant.
            participants: list containing the user ids of the participants user
            data will be downloaded for
            params: the data for the request.
            response: the response from the request.
            firstRow: the first row in the csv.
            secondRow: the second row in the csv.
            thirdRow: the third row in the csv.
            participantsClickData: the rows combined.
        Arguments:
            testClient: the test client we test this for.
            initDatabase: the database instance we test this for.
    '''
    del initDatabase

    # make a researcher
    researcher = User(username='r2', password_plaintext='p1', role='researcher')
    uploadToDatabase(researcher)

    # check a researcher
    assert researcher.username == 'r2'
    assert researcher.check_password('p1')
    assert researcher.role == 'researcher'

    # get access token
    access_token = loginHelper(testClient, 'r2', 'p1')

    # make two participants
    participant = User(username='p1', password_plaintext='p1', role='participant')
    participant1 = User(username='p2', password_plaintext='p1', role='participant')
    uploadToDatabase(participant)
    uploadToDatabase(participant1)

    # check two participants
    assert participant.username == 'p1'
    assert participant.check_password('p1')
    assert participant.role == 'participant'
    assert participant1.username == 'p2'
    assert participant1.check_password('p1')
    assert participant1.role == 'participant'

    # make the two clicks
    url='somePage'
    eventType = 'someEventType'
    participantClick = Clicks(participant.id, url, eventType)
    url1='somePage1'
    eventType1 = 'someEventType1'
    participantClick1 = Clicks(participant1.id, url1, eventType1)
    uploadToDatabase(participantClick)
    uploadToDatabase(participantClick1)

    # check the two clicks
    assert participantClick.userId == participant.id
    assert participantClick.url == url
    assert participantClick.eventType == eventType
    assert participantClick1.userId == participant1.id
    assert participantClick1.url == url1
    assert participantClick1.eventType == eventType1

    # retrieve and check the data
    participants = [participant.id, participant1.id]
    params = {
        'userId': participants,
    }
    response = testClient.get('/clickapi/getParticipantsUserData', 
        query_string=params, 
        headers={"Authorization": "Bearer " + access_token})
    assert response.status_code == 200

    # make the csv file as String
    firstRow = 'clickId,userId,timestamp,url,eventType,actionId'
    secondRow = str(participantClick.clickId) + ',' + str(participantClick.userId) + ',' + participantClick.timestamp.strftime('%Y-%m-%d %H:%M:%S.%f') + ',' + participantClick.url + ',' + participantClick.eventType + ',' + (participantClick.actionId or '')
    thirdRow = str(participantClick1.clickId) + ',' + str(participantClick1.userId) + ',' + participantClick1.timestamp.strftime('%Y-%m-%d %H:%M:%S.%f') + ',' + participantClick1.url + ',' + participantClick1.eventType + ',' + (participantClick1.actionId or '')
    participantsClickData = firstRow + '\n' + secondRow + '\n' + thirdRow + '\n'
    assert response.data == participantsClickData.encode('utf-8')

def testZeroParticipantsAdmin(testClient, initDatabase):
    '''
        Tests if an admin that selects zero participants gets an error
        when trying to download the user data.
        Attributes:
            admin: a user with the admin role.
            access_token: used for showing that user is logged in.
            participants: list containing the user ids of the participants user
            data will be downloaded for
            params: the data for the request.
            response: the response from the request.
        Arguments:
            testClient: the test client we test this for.
            initDatabase: the database instance we test this for.
    '''
    del initDatabase

    # make and check an admin
    admin = User(username='a1', password_plaintext='p1', role='admin')
    uploadToDatabase(admin)
    assert admin.username == 'a1'
    assert admin.check_password('p1')
    assert admin.role == 'admin'

    # get access token
    access_token = loginHelper(testClient, 'a1', 'p1')

    participants = []
    params = {
        'userId': participants,
    }
    response = testClient.get('/clickapi/getParticipantsUserData', 
        query_string=params, 
        headers={"Authorization": "Bearer " + access_token})
    assert response.status_code == 400
    assert response.data == 'Select at least one participant'.encode('utf-8')

def testOneParticipantAdmin(testClient, initDatabase):
    '''
        Tests if an admin that selects one participant gets the user data of
        that participant.
        Attributes:
            admin: a user with the admin role.
            access_token: used for showing that user is logged in.
            participant: a user with the participant role.
            url: the url of the test click.
            eventType: the event type of the test click.
            participantClick: the test click related to the participant.
            participants: list containing the user ids of the participants user
            data will be downloaded for
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

    # make and check an admin
    admin = User(username='a1', password_plaintext='p1', role='admin')
    uploadToDatabase(admin)
    assert admin.username == 'a1'
    assert admin.check_password('p1')
    assert admin.role == 'admin'

    # get access token
    access_token = loginHelper(testClient, 'a1', 'p1')

    # make a participant
    participant = User(username='p1', password_plaintext='p1', role='participant')
    uploadToDatabase(participant)

    # check a participant
    assert participant.username == 'p1'
    assert participant.check_password('p1')
    assert participant.role == 'participant'

    # make a click
    url='somePage'
    eventType = 'someEventType'
    participantClick = Clicks(participant.id, url, eventType)
    uploadToDatabase(participantClick)

    # check the click
    assert participantClick.userId == participant.id
    assert participantClick.url == url
    assert participantClick.eventType == eventType

    # retrieve and check the data
    participants = [participant.id]
    params = {
        'userId': participants,
    }
    response = testClient.get('/clickapi/getParticipantsUserData', 
        query_string=params, 
        headers={"Authorization": "Bearer " + access_token})
    assert response.status_code == 200

    # make the csv file as String
    firstRow = 'clickId,userId,timestamp,url,eventType,actionId'
    secondRow = str(participantClick.clickId) + ',' + str(participantClick.userId) + ',' + participantClick.timestamp.strftime('%Y-%m-%d %H:%M:%S.%f') + ',' + participantClick.url + ',' + participantClick.eventType + ',' + (participantClick.actionId or '')
    participantsClickData = firstRow + '\n' + secondRow + '\n'
    assert response.data == participantsClickData.encode('utf-8')

def testTwoParticipantsAdmin(testClient, initDatabase):
    '''
        Tests if a admin that selects two participants gets the user data 
        of that participant.
        Attributes:
            admin: a user with the admin role.
            access_token: used for showing that user is logged in.
            participant: a user with the participant role.
            url: the url of the test click.
            eventType: the event type of the test click.
            participantClick: the test click related to the participant.
            participant1: a user with the participant role.
            url1: the url of the test click.
            eventType1: the event type of the test click.
            participantClick1: the test click related to the participant.
            participants: list containing the user ids of the participants user
            data will be downloaded for
            params: the data for the request.
            response: the response from the request.
            firstRow: the first row in the csv.
            secondRow: the second row in the csv.
            thirdRow: the third row in the csv.
            participantsClickData: the rows combined.
        Arguments:
            testClient: the test client we test this for.
            initDatabase: the database instance we test this for.
    '''
    del initDatabase

    # make and check an admin
    admin = User(username='a2', password_plaintext='p1', role='admin')
    uploadToDatabase(admin)
    assert admin.username == 'a2'
    assert admin.check_password('p1')
    assert admin.role == 'admin'

    # get access token
    access_token = loginHelper(testClient, 'a2', 'p1')

    # make two participants
    participant = User(username='p1', password_plaintext='p1', role='participant')
    participant1 = User(username='p2', password_plaintext='p1', role='participant')
    uploadToDatabase(participant)
    uploadToDatabase(participant1)

    # check two participants
    assert participant.username == 'p1'
    assert participant.check_password('p1')
    assert participant.role == 'participant'
    assert participant1.username == 'p2'
    assert participant1.check_password('p1')
    assert participant1.role == 'participant'

    # make the two clicks
    url='somePage'
    eventType = 'someEventType'
    participantClick = Clicks(participant.id, url, eventType)
    url1='somePage1'
    eventType1 = 'someEventType1'
    participantClick1 = Clicks(participant1.id, url1, eventType1)
    uploadToDatabase(participantClick)
    uploadToDatabase(participantClick1)

    # check the two clicks
    assert participantClick.userId == participant.id
    assert participantClick.url == url
    assert participantClick.eventType == eventType
    assert participantClick1.userId == participant1.id
    assert participantClick1.url == url1
    assert participantClick1.eventType == eventType1

    # retrieve and check the data
    participants = [participant.id, participant1.id]
    params = {
        'userId': participants,
    }
    response = testClient.get('/clickapi/getParticipantsUserData', 
        query_string=params, 
        headers={"Authorization": "Bearer " + access_token})
    assert response.status_code == 200

    # make the csv file as String
    firstRow = 'clickId,userId,timestamp,url,eventType,actionId'
    secondRow = str(participantClick.clickId) + ',' + str(participantClick.userId) + ',' + participantClick.timestamp.strftime('%Y-%m-%d %H:%M:%S.%f') + ',' + participantClick.url + ',' + participantClick.eventType + ',' + (participantClick.actionId or '')
    thirdRow = str(participantClick1.clickId) + ',' + str(participantClick1.userId) + ',' + participantClick1.timestamp.strftime('%Y-%m-%d %H:%M:%S.%f') + ',' + participantClick1.url + ',' + participantClick1.eventType + ',' + (participantClick1.actionId or '')
    participantsClickData = firstRow + '\n' + secondRow + '\n' + thirdRow + '\n'
    assert response.data == participantsClickData.encode('utf-8')