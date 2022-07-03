from app.models import Projects, User
from test_set_role import loginHelper
from app import db
import json

def testRetrieveNoProjects(testClient, initDatabase): 
    '''
        This tests checks that an error message is given when the specified
        user, has no projects and there are no projects in the database.
        Attributes: 
            access_token: access token for ad min
            response: the result of retrieving the files in the specified order
        Arguments: 
            testClient:  the test client we test this for.
            initDatabase: the database instance we test this for. 
    '''
    del initDatabase
    assert User.query.filter_by(username='ad').first().role == 'admin'
    # get access token for ad min
    access_token = loginHelper(testClient, 'ad', 'min')

    # We do not add any projects to the database

    # We try to retrieve the projects of the user
    response = testClient.get('/projectapi/viewProjectsOfUser', headers = {"Authorization": "Bearer " + access_token})
    
    # Check if the expected response has the correct status code    
    assert response.status_code == 200

    # Check if the expected response is correct:
    assert response.data == b'[]\n'


def testRetrieveNoProjectsOfUser(testClient, initDatabase): 
    '''
        This tests checks that an error message is given when the specified
        user, here with user id 200, has no projects and there are
        projects in the database.
        Attributes: 
            access_token: access token for ad min
            project1: new project
            response: the result of retrieving the files in the specified order
        Arguments: 
            testClient:  the test client we test this for.
            initDatabase: the database instance we test this for. 
    '''
    del initDatabase
    # get access token for ad min
    access_token = loginHelper(testClient, 'ad', 'min')

    # We add a single project to the database, which is not from the user
    project1 = Projects(201, "Project1")
    db.session.add(project1)
    db.session.commit()

    # We try to retrieve the projects of the user
    response = testClient.get('/projectapi/viewProjectsOfUser', headers = {"Authorization": "Bearer " + access_token})

    # Check if the expected response has the correct status code
    assert response.status_code == 200

    # Check if the expected response is correct:
    assert response.data == b'[]\n'


def testRetrieveSingleProjectOfUser(testClient, initDatabase): 
    '''
        This tests checks that a project is given when the specified
        user, here with user id 200, has one project and the database
        contains only one project.
        Attributes: 
            access_token: access token for ad min
            adId: userId of the admin
            project1: new project
            response: the result of retrieving the files in the specified order
            expected_response: response we expect
        Arguments: 
            testClient:  the test client we test this for.
            initDatabase: the database instance we test this for. 
    '''
    del initDatabase
    # get access token for ad min
    access_token = loginHelper(testClient, 'ad', 'min')

    adId = User.query.filter_by(username='ad').first().id

    # We add a single project to the database, which is from the user
    project1 = Projects(adId, "Project1")
    db.session.add(project1)
    db.session.commit()

    # We try to retrieve the projects of the user
    response = testClient.get('/projectapi/viewProjectsOfUser', headers = {"Authorization": "Bearer " + access_token})

    # Check if the expected response has the correct status code
    assert response.status_code == 200

    # Create the expected response:
    expected_response = [dict(userId=adId,
                        projectName='Project1', 
                        partCount=0,
                        id=1
                        ), 
                        ]
    # Check if the expected response is correct:
    assert json.loads(response.data) == expected_response


def testRetrieveMultipleProjectsOfUser(testClient, initDatabase): 
    '''
        This tests checks that multiple projects are given when the 
        specified user, here with user id 200, has multiple projects.
        Their projects are the only ones in the database.
        Attributes: 
            access_token: access token for ad min
            adId: userId of the admin
            project1: new project
            project2: new project
            project3: new project
            response: the result of retrieving the files in the specified order
            expected_response: response we expected
        Arguments: 
            testClient:  the test client we test this for.
            initDatabase: the database instance we test this for. 
    '''
    del initDatabase
    # get access token for ad min
    access_token = loginHelper(testClient, 'ad', 'min')

    adId = User.query.filter_by(username='ad').first().id

    # We add multiple projects to the database, which are all from the user
    project1 = Projects(adId, "Project1")
    db.session.add(project1)
    project2 = Projects(adId, "Project2")
    db.session.add(project2)
    project3 = Projects(adId, "Project3")
    db.session.add(project3)
    db.session.commit()

    # We try to retrieve the projects of the user
    response = testClient.get('/projectapi/viewProjectsOfUser', headers = {"Authorization": "Bearer " + access_token})

    # Check if the expected response has the correct status code
    assert response.status_code == 200

    # Create the expected response:
    expected_response = [dict(userId=adId, 
                        projectName='Project1', 
                        partCount=0,
                        id=1
                        ), 
                        dict(userId=adId, 
                        projectName='Project2', 
                        partCount=0,
                        id=2
                        ), 
                        dict(userId=adId, 
                        projectName='Project3', 
                        partCount=0,
                        id=3
                        ), 
                        ]
    # Check if the expected response is correct:
    assert json.loads(response.data) == expected_response


def testRetrieveOnlyProjectsOfUser(testClient, initDatabase): 
    '''
        This tests checks that multiple projects are given when the 
        specified user, here with user id 200, has multiple projects.
        Their projects are not the only ones in the database.
        Attributes: 
            access_token: access token for ad min
            adId: userId of the admin
            project1: new project
            project2: new project
            project3: new project
            response: the result of retrieving the files in the specified order
            expected_response: response we expected
        Arguments: 
            testClient:  the test client we test this for.
            initDatabase: the database instance we test this for. 
    '''
    del initDatabase
    # get access token for ad min
    access_token = loginHelper(testClient, 'ad', 'min')

    adId = User.query.filter_by(username='ad').first().id

    # We add multiple projects to the database, which are not all from the user
    project1 = Projects(adId, "Project1")
    db.session.add(project1)
    project2 = Projects(201, "Project2")
    db.session.add(project2)
    project3 = Projects(adId, "Project3")
    db.session.add(project3)
    db.session.commit()

    # We try to retrieve the projects of the user
    response = testClient.get('/projectapi/viewProjectsOfUser', headers = {"Authorization": "Bearer " + access_token})

    # Check if the expected response has the correct status code    
    assert response.status_code == 200

    # Create the expected response:
    expected_response = [dict(userId=adId, 
                        projectName='Project1', 
                        partCount=0,
                        id=1
                        ), 
                        dict(userId=adId, 
                        projectName='Project3', 
                        partCount=0,
                        id=3
                        ), 
                        ]
    # Check if the expected response is correct:
    assert json.loads(response.data) == expected_response

def testRetrieveOnlyProjectsOfUser(testClient, initDatabase):
    '''
        This tests checks that multiple projects are given when the
        specified user, here with user id 200, has multiple projects.
        Their projects are not the only ones in the database.
        Attributes:
            access_token: access token for ad min
            adId: userId of the admin
            project1: new project
            project2: new project
            project3: new project
            response: the result of retrieving the files in the specified order
            expected_response: response we expected
        Arguments:
            testClient:  the test client we test this for.
            initDatabase: the database instance we test this for.
    '''
    del initDatabase
    # get access token for ad min
    access_token = loginHelper(testClient, 'Pietje', 'Bell')
    pietId = User.query.filter_by(username='Pietje').first().id

    # We add multiple projects to the database, which are not all from the user
    project1 = Projects(pietId, "Project1")
    db.session.add(project1)
    db.session.commit()

    # We try to retrieve the projects of the user
    response = testClient.get('/projectapi/viewProjectsOfUser', headers = {"Authorization": "Bearer " + access_token})

    # Check if the expected response has the correct status code
    assert response.status_code == 403

    # Check if the expected response is correct:
    assert response.data == b'Method only accessible for researcher and admin users'
