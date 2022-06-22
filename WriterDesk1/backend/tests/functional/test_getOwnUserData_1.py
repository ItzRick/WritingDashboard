from app.models import User, Clicks
from app.database import uploadToDatabase
from test_set_role import loginHelper
from datetime import datetime

def testStudentOneClick(testClient, initDatabase):
    '''
        Tests if a user with the student role and one click made can download 
        their corresponding user data.
        Attributes:
            student: a user with the student role.
            access_token: used for showing that user is logged in.
            url: the url of the test click.
            eventType: the event type of the test click.
            studentClick: the test click related to the student.
            userId: the id of the student.
            params: the data for the request.
            response: the response from the request.
            firstRow: the first row in the csv.
            secondRow: the second row in the csv.
            studentClickData: the rows combined.
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

    # make a click
    url='somePage'
    eventType = 'someEventType'
    studentClick = Clicks(student.id, url, eventType)
    uploadToDatabase(studentClick)

    # check the click
    assert studentClick.userId == student.id
    assert studentClick.url == url
    assert studentClick.eventType == eventType

    # retreive and check the user data
    userId = student.id
    params = {
        'userId': userId,
    }
    response = testClient.get('/clickapi/getOwnUserData', query_string=params, 
        headers={"Authorization": "Bearer " + access_token})
    assert response.status_code == 200

    # make the csv file as String
    firstRow = 'clickId,userId,timestamp,url,eventType,actionId'
    secondRow = str(studentClick.clickId) + ',' + str(studentClick.userId) + ',' + studentClick.timestamp.strftime('%Y-%m-%d %H:%M:%S.%f') + ',' + studentClick.url + ',' + studentClick.eventType + ',' + (studentClick.actionId or '')
    studentClickData = firstRow + '\n' + secondRow + '\n'
    assert response.data == studentClickData.encode('utf-8')

def testStudentTwoClicks(testClient, initDatabase):
    '''
        Tests if a user with the student role and two clicks made can download 
        their corresponding user data.
        Attributes:
            student: a user with the student role.
            access_token: used for showing that user is logged in.
            url: the url of the test click.
            eventType: the event type of the test click.
            studentClick: the test click related to the student.
            url1: the url of the test click.
            eventType1: the event type of the test click.
            studentClick1: the test click related to the student.
            userId: the id of the student.
            params: the data for the request.
            response: the response from the request.
            firstRow: the first row in the csv.
            secondRow: the second row in the csv.
            thirdRow: the third row in the csv.
            studentClickData: the rows combined.
        Arguments:
            testClient: the test client we test this for.
            initDatabase: the database instance we test this for.
    '''
    del initDatabase

    # make a student
    student = User(username='s2', password_plaintext='p1', role='student')
    uploadToDatabase(student)

    # check a student
    assert student.username == 's2'
    assert student.check_password('p1')
    assert student.role == 'student'

    # get access token
    access_token = loginHelper(testClient, 's2', 'p1')

    # make the two clicks
    url='somePage'
    eventType = 'someEventType'
    studentClick = Clicks(student.id, url, eventType)
    url1='somePage1'
    eventType1 = 'someEventType1'
    studentClick1 = Clicks(student.id, url1, eventType1)
    uploadToDatabase(studentClick)
    uploadToDatabase(studentClick1)

    # check the two clicks
    assert studentClick.userId == student.id
    assert studentClick.url == url
    assert studentClick.eventType == eventType
    assert studentClick1.userId == student.id
    assert studentClick1.url == url1
    assert studentClick1.eventType == eventType1

    # retreive and check the user data
    userId = student.id
    params = {
        'userId': userId,
    }
    response = testClient.get('/clickapi/getOwnUserData', query_string=params, 
        headers={"Authorization": "Bearer " + access_token})
    assert response.status_code == 200

    # make the csv file as String
    firstRow = 'clickId,userId,timestamp,url,eventType,actionId'
    secondRow = str(studentClick.clickId) + ',' + str(studentClick.userId) + ',' + studentClick.timestamp.strftime('%Y-%m-%d %H:%M:%S.%f') + ',' + studentClick.url + ',' + studentClick.eventType + ',' + (studentClick.actionId or '')
    thirdRow = str(studentClick1.clickId) + ',' + str(studentClick1.userId) + ',' + studentClick1.timestamp.strftime('%Y-%m-%d %H:%M:%S.%f') + ',' + studentClick1.url + ',' + studentClick1.eventType + ',' + (studentClick1.actionId or '')
    studentClickData = firstRow + '\n' + secondRow + '\n' + thirdRow + '\n'
    assert response.data == studentClickData.encode('utf-8')

def testParticipantOneClick(testClient, initDatabase):
    '''
        Tests if a user with the participant role and one click made can 
        download their corresponding user data.
        Attributes:
            participant: a user with the participant role.
            access_token: used for showing that user is logged in.
            url: the url of the test click.
            eventType: the event type of the test click.
            participantClick: the test click related to the participant.
            userId: the id of the participant.
            params: the data for the request.
            response: the response from the request.
            firstRow: the first row in the csv.
            secondRow: the second row in the csv.
            participantClickData: the rows combined.
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

    # make a click
    url='somePage'
    eventType = 'someEventType'
    participantClick = Clicks(participant.id, url, eventType)
    uploadToDatabase(participantClick)

    # check the click
    assert participantClick.userId == participant.id
    assert participantClick.url == url
    assert participantClick.eventType == eventType

    # retreive and check the user data
    userId = participant.id
    params = {
        'userId': userId,
    }
    response = testClient.get('/clickapi/getOwnUserData', query_string=params, 
        headers={"Authorization": "Bearer " + access_token})
    assert response.status_code == 200

    # make the csv file as String
    firstRow = 'clickId,userId,timestamp,url,eventType,actionId'
    secondRow = str(participantClick.clickId) + ',' + str(participantClick.userId) + ',' + participantClick.timestamp.strftime('%Y-%m-%d %H:%M:%S.%f') + ',' + participantClick.url + ',' + participantClick.eventType + ',' + (participantClick.actionId or '')
    participantClickData = firstRow + '\n' + secondRow + '\n'
    assert response.data == participantClickData.encode('utf-8')

def testParticipantTwoClicks(testClient, initDatabase):
    '''
        Tests if a user with the participant role and two clicks made can download 
        their corresponding user data.
        Attributes:
            participant: a user with the participant role.
            access_token: used for showing that user is logged in.
            url: the url of the test click.
            eventType: the event type of the test click.
            participantClick: the test click related to the participant.
            url1: the url of the test click.
            eventType1: the event type of the test click.
            participantClick1: the test click related to the participant.
            userId: the id of the participant.
            params: the data for the request.
            response: the response from the request.
            firstRow: the first row in the csv.
            secondRow: the second row in the csv.
            thirdRow: the third row in the csv.
            participantClickData: the rows combined.
        Arguments:
            testClient: the test client we test this for.
            initDatabase: the database instance we test this for.
    '''
    del initDatabase

    # make a participant
    participant = User(username='p2', password_plaintext='p1', role='participant')
    uploadToDatabase(participant)

    # check a participant
    assert participant.username == 'p2'
    assert participant.check_password('p1')
    assert participant.role == 'participant'

    # get access token
    access_token = loginHelper(testClient, 'p2', 'p1')

    # make the two clicks
    url='somePage'
    eventType = 'someEventType'
    participantClick = Clicks(participant.id, url, eventType)
    url1='somePage1'
    eventType1 = 'someEventType1'
    participantClick1 = Clicks(participant.id, url1, eventType1)
    uploadToDatabase(participantClick)
    uploadToDatabase(participantClick1)

    # check the two clicks
    assert participantClick.userId == participant.id
    assert participantClick.url == url
    assert participantClick.eventType == eventType
    assert participantClick1.userId == participant.id
    assert participantClick1.url == url1
    assert participantClick1.eventType == eventType1

    # retreive and check the user data
    userId = participant.id
    params = {
        'userId': userId,
    }
    response = testClient.get('/clickapi/getOwnUserData', query_string=params, 
        headers={"Authorization": "Bearer " + access_token})
    assert response.status_code == 200

    # make the csv file as String
    firstRow = 'clickId,userId,timestamp,url,eventType,actionId'
    secondRow = str(participantClick.clickId) + ',' + str(participantClick.userId) + ',' + participantClick.timestamp.strftime('%Y-%m-%d %H:%M:%S.%f') + ',' + participantClick.url + ',' + participantClick.eventType + ',' + (participantClick.actionId or '')
    thirdRow = str(participantClick1.clickId) + ',' + str(participantClick1.userId) + ',' + participantClick1.timestamp.strftime('%Y-%m-%d %H:%M:%S.%f') + ',' + participantClick1.url + ',' + participantClick1.eventType + ',' + (participantClick1.actionId or '')
    participantClickData = firstRow + '\n' + secondRow + '\n' + thirdRow + '\n'
    assert response.data == participantClickData.encode('utf-8')

def testResearcherOneClick(testClient, initDatabase):
    '''
        Tests if a user with the researcher role and one click made can 
        download their corresponding user data.
        Attributes:
            researcher: a user with the researcher role.
            access_token: used for showing that user is logged in.
            url: the url of the test click.
            eventType: the event type of the test click.
            researcherClick: the test click related to the researcher.
            userId: the id of the researcher.
            params: the data for the request.
            response: the response from the request.
            firstRow: the first row in the csv.
            secondRow: the second row in the csv.
            researcherClickData: the rows combined.
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

    # make a click
    url='somePage'
    eventType = 'someEventType'
    researcherClick = Clicks(researcher.id, url, eventType)
    uploadToDatabase(researcherClick)

    # check the click
    assert researcherClick.userId == researcher.id
    assert researcherClick.url == url
    assert researcherClick.eventType == eventType

    # retreive and check the user data
    userId = researcher.id
    params = {
        'userId': userId,
    }
    response = testClient.get('/clickapi/getOwnUserData', query_string=params, 
        headers={"Authorization": "Bearer " + access_token})
    assert response.status_code == 200

    # make the csv file as String
    firstRow = 'clickId,userId,timestamp,url,eventType,actionId'
    secondRow = str(researcherClick.clickId) + ',' + str(researcherClick.userId) + ',' + researcherClick.timestamp.strftime('%Y-%m-%d %H:%M:%S.%f') + ',' + researcherClick.url + ',' + researcherClick.eventType + ',' + (researcherClick.actionId or '')
    researcherClickData = firstRow + '\n' + secondRow + '\n'
    assert response.data == researcherClickData.encode('utf-8')

def testResearcherTwoClicks(testClient, initDatabase):
    '''
        Tests if a user with the researcher role and two clicks made can 
        download their corresponding user data.
        Attributes:
            researcher: a user with the researcher role.
            access_token: used for showing that user is logged in.
            url: the url of the test click.
            eventType: the event type of the test click.
            researcherClick: the test click related to the researcher.
            url1: the url of the test click.
            eventType1: the event type of the test click.
            researcherClick1: the test click related to the researcher.
            userId: the id of the researcher.
            params: the data for the request.
            response: the response from the request.
            firstRow: the first row in the csv.
            secondRow: the second row in the csv.
            thirdRow: the third row in the csv.
            researcherClickData: the rows combined.
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

    # make the two clicks
    url='somePage'
    eventType = 'someEventType'
    researcherClick = Clicks(researcher.id, url, eventType)
    url1='somePage1'
    eventType1 = 'someEventType1'
    researcherClick1 = Clicks(researcher.id, url1, eventType1)
    uploadToDatabase(researcherClick)
    uploadToDatabase(researcherClick1)

    # check the two clicks
    assert researcherClick.userId == researcher.id
    assert researcherClick.url == url
    assert researcherClick.eventType == eventType
    assert researcherClick1.userId == researcher.id
    assert researcherClick1.url == url1
    assert researcherClick1.eventType == eventType1

    # retreive and check the user data
    userId = researcher.id
    params = {
        'userId': userId,
    }
    response = testClient.get('/clickapi/getOwnUserData', query_string=params, 
        headers={"Authorization": "Bearer " + access_token})
    assert response.status_code == 200

    # make the csv file as String
    firstRow = 'clickId,userId,timestamp,url,eventType,actionId'
    secondRow = str(researcherClick.clickId) + ',' + str(researcherClick.userId) + ',' + researcherClick.timestamp.strftime('%Y-%m-%d %H:%M:%S.%f') + ',' + researcherClick.url + ',' + researcherClick.eventType + ',' + (researcherClick.actionId or '')
    thirdRow = str(researcherClick1.clickId) + ',' + str(researcherClick1.userId) + ',' + researcherClick1.timestamp.strftime('%Y-%m-%d %H:%M:%S.%f') + ',' + researcherClick1.url + ',' + researcherClick1.eventType + ',' + (researcherClick1.actionId or '')
    researcherClickData = firstRow + '\n' + secondRow + '\n' + thirdRow + '\n'
    assert response.data == researcherClickData.encode('utf-8')