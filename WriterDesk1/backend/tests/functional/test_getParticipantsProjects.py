from app.models import User, Projects
import json
from app.database import postParticipant, uploadToDatabase

from test_set_role import loginHelper


def testDefaultPartPro(testClient, initDatabase):
    ''' 
    This function tests the api call getParticipantsProjects 
    when logged in as an admin with no projects
    Arguments:
        testClient:  The test client we test this for.
        initDatabase: the database instance we test this for.
    Attributes:
        access_token: admin's access token
        response: response of call
        data: data from response
    '''
    del initDatabase

    # test existance of ad min
    assert User.query.filter_by(username='ad').first() is not None
    # get access token for ad
    access_token = loginHelper(testClient, 'ad', 'min')

    # Retrieve the users except for those with the participant role
    response = testClient.get('/usersapi/getParticipantsProjects', headers={"Authorization": "Bearer " + access_token})

    # Check if we get the correct status_code:
    assert response.status_code == 200

    data = json.loads(response.data)
    assert data == []

def testNoAccessPartPro(testClient, initDatabase):
    ''' 
    This function tests the api call getParticipantsProjects 
    when logged in as a user that is not an admin or researcher
    Arguments:
        testClient:  The test client we test this for.
        initDatabase: the database instance we test this for.
    Attributes:
        access_token: Pietje's access token
        response: response of call
        data: data from response
    '''
    del initDatabase

    # test existance of Pietje
    assert User.query.filter_by(username='Pietje').first() is not None
    # get access token for Pietje
    access_token = loginHelper(testClient, 'Pietje', 'Bell')

    # Retrieve the users except for those with the participant role
    response = testClient.get('/usersapi/getParticipantsProjects', headers={"Authorization": "Bearer " + access_token})

    # Check if we get the correct status_code:
    assert response.status_code == 403

def testWithProjectsPartPro(testClient, initDatabase):
    ''' 
    This function tests the api call getParticipantsProjects 
    when logged in as an admin with some projects
    Arguments:
        testClient:  The test client we test this for.
        initDatabase: the database instance we test this for.
    Attributes:
        access_token: admin's access token
        response: response of call
        data: data from response
    '''
    del initDatabase

    # test existance of ad min
    assert User.query.filter_by(username='ad').first() is not None
    # get access token for ad
    access_token = loginHelper(testClient, 'ad', 'min')

    adId = User.query.filter_by(username='ad').first().id
    pietId = User.query.filter_by(username='Pietje').first().id
    
    # create project for the admin
    projectName1 = "Project1"
    project1 = Projects(adId, projectName1)
    uploadToDatabase(project1)
    pid1 = Projects.query.filter_by(projectName=projectName1).first().id
    
    # create different project for different user (Pietje)
    projectName2 = "Project2"
    project2 = Projects(pietId, projectName2)
    uploadToDatabase(project2)
    pid2 = Projects.query.filter_by(projectName=projectName2).first().id

    # create 2 participants
    pName1 = 'testPart1'
    pName2 = 'testPart2'
    postParticipant(pName1, 'pass', pid1)
    uid1 = User.query.filter_by(username=pName1, project=pid1).first().id
    postParticipant(pName2, 'pass', pid2)
    uid2 = User.query.filter_by(username=pName2, project=pid2).first().id
    
    # Retrieve the participants of all projects related to admin
    response = testClient.get('/usersapi/getParticipantsProjects', headers={"Authorization": "Bearer " + access_token})

    # Check if we get the correct status_code:
    assert response.status_code == 200

    data = json.loads(response.data)

    # should contain participant 1
    assert any(
            (d['id'] == uid1 and
            d['username'] == pName1 and
            d['role'] == 'participant' and
            d['projectid'] == pid1 and
            d['projectname'] == projectName1)
        for d in data)
    
    # should contain exactly one participant
    assert len(data) == 1
    # participant 2 (with uid2) is not in the data
    assert all(
            (d['id'] != uid2)
        for d in data)