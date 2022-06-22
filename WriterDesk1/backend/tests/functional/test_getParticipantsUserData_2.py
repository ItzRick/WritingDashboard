from app.models import User, Clicks
from test_set_role import loginHelper
from app.database import uploadToDatabase

def testNoUserDataResearcher(testClient, initDatabase):
    '''
        Tests if a researcher that selects one participant gets the user data of
        that participant. The user data of the participant is None except for
        the user id of the participant.
        Attributes:
            researcher: a user with the researcher role.
            access_token: used for showing that user is logged in.
            participant: a user with the participant role.
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
    # all columns except for userId are None, so it will just have comma's
    secondRow = ',' + str(participant.id) + ',' + ',' + ',' + ','
    participantsClickData = firstRow + '\n' + secondRow + '\n'
    assert response.data == participantsClickData.encode('utf-8')

def testNoUserDataAdmin(testClient, initDatabase):
    '''
        Tests if an admin that selects one participant gets the user data of
        that participant. The user data of the participant is None except for
        the user id of the participant.
        Attributes:
            admin: a user with the admin role.
            access_token: used for showing that user is logged in.
            participant: a user with the participant role.
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
    participant = User(username='p1', password_plaintext='p1', role='participant')
    uploadToDatabase(participant)

    # check a participant
    assert participant.username == 'p1'
    assert participant.check_password('p1')
    assert participant.role == 'participant'

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
    # all columns except for userId are None, so it will just have comma's
    secondRow = ',' + str(participant.id) + ',' + ',' + ',' + ','
    participantsClickData = firstRow + '\n' + secondRow + '\n'
    assert response.data == participantsClickData.encode('utf-8')

def testNoAccessStudent(testClient, initDatabase):
    '''
        Tests if a student does not have access to retrieving the user data of
        participants.
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

    response = testClient.get('/clickapi/getParticipantsUserData', 
        headers={"Authorization": "Bearer " + access_token})
    assert response.status_code == 403
    assert response.data == 'Method only accessible for admin or researcher users'.encode('utf-8')

def testNoAccessParticipant(testClient, initDatabase):
    '''
        Tests if a participant does not have access to retrieving the user data 
        of participants.
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

    response = testClient.get('/clickapi/getParticipantsUserData', 
        headers={"Authorization": "Bearer " + access_token})
    assert response.status_code == 403
    assert response.data == 'Method only accessible for admin or researcher users'.encode('utf-8')