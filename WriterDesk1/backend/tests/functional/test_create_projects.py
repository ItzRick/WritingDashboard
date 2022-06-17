from app.models import Projects, User
from app import db

from test_set_role import loginHelper

def testAddToDatabase(testClient, initDatabase):
    '''
        Test if we can add a project to the database. We first check if the project does not exist yet.
        After the function has been executed, we check whether the project appears now in the database.
        Arguments:
            testClient: The test client we test this for.
            initDatabase: The database instance we test this for.
        Attributes:
            response: The response of the setProject backend call
            project: Project that is added to the database.
            access_token: Access token for user Pietje Bell
    '''
    del initDatabase
    # Check if the project is not yet in the database:
    assert Projects.query.filter_by(projectName='Project1').first() is None

    # get access token for Pietje Bell
    access_token = loginHelper(testClient, 'Pietje', 'Bell')
    # Add the project to the database
    response = testClient.post('/projectapi/setProject', data={'projectName': 'Project1'},
                               headers = {"Authorization": "Bearer " + access_token})

    # Check if we get the correct status code:
    assert response.status_code == 200

    # Check if the project is added to the database:
    project = Projects.query.filter_by(projectName='Project1').first()
    assert project.projectName == 'Project1'
    assert project.userId == User.query.filter_by(username='Pietje').first().id


def testAddToDatabaseMultiple(testClient, initDatabase):
    '''
        Test if we can add multiple project to the database. We first check if the projects do not exist yet.
        After the function has been executed, we check whether the projects appear now in the database.
        Arguments:
            testClient: The test client we test this for.
            initDatabase: The database instance we test this for.
        Attributes:
            response1, response2: The responses of the setProject backend call
            project1, project2: Projects that are added to the database.
            access_token: Access token for user Pietje Bell
    '''
    del initDatabase
    # Check if the projects are not yet in the database:
    assert Projects.query.filter_by(projectName='Project1').first() is None
    assert Projects.query.filter_by(projectName='Project2').first() is None

    # get access token for Pietje Bell
    access_token = loginHelper(testClient, 'Pietje', 'Bell')

    # Add the projects to the database
    response1 = testClient.post('/projectapi/setProject', data={'projectName': 'Project1'},
                                headers = {"Authorization": "Bearer " + access_token})
    response2 = testClient.post('/projectapi/setProject', data={'projectName': 'Project2'},
                                headers = {"Authorization": "Bearer " + access_token})

    # Check if we get the correct status codes:
    assert response1.status_code == 200
    assert response2.status_code == 200

    # Check if the projects are added to the database:
    project1 = Projects.query.filter_by(projectName='Project1').first()
    assert project1.projectName == 'Project1'
    assert project1.userId == User.query.filter_by(username='Pietje').first().id

    project2 = Projects.query.filter_by(projectName='Project2').first()
    assert project2.projectName == 'Project2'
    assert project2.userId == User.query.filter_by(username='Pietje').first().id


def testAddToDatabaseEmptyProjectName(testClient, initDatabase):
    '''
        Test if we can add a project to the database with empty project name. We first check if the project does not exist yet.
        After the function has been executed, we check whether the project appears now in the database.
        Arguments:
            testClient: The test client we test this for.
            initDatabase: The database instance we test this for.
        Attributes:
            response: The response of the setProject backend call
            project: Project that is added to the database.
            access_token: Access token for user Pietje Bell
    '''
    del initDatabase
    # Check if the project is not yet in the database:
    assert Projects.query.filter_by(projectName='').first() is None

    # get access token for Pietje Bell
    access_token = loginHelper(testClient, 'Pietje', 'Bell')

    # Add the project to the database
    response = testClient.post('/projectapi/setProject', data={'userId': 1}, headers = {"Authorization": "Bearer " + access_token})

    # Check if we get the correct status code:
    assert response.status_code == 200

    # Check if the project is added to the database:
    project = Projects.query.filter_by(projectName='').first()
    assert project.projectName == ''
    assert project.userId == User.query.filter_by(username='Pietje').first().id


def testAddToDatabaseEmptyUserId(testClient, initDatabase):
    '''
        Test if we can not add a project to the database with empty user id. We first check if the project does not exist yet.
        After the function has been executed, we check if the project is still not added to the database.
        Arguments:
            testClient: The test client we test this for.
            initDatabase: The database instance we test this for.
        Attributes:
            response: The response of the setProject backend call
    '''
    del initDatabase
    # Check if the project is not yet in the database:
    assert Projects.query.filter_by(projectName='Project1').first() is None

    # Try to add the project to the database
    response = testClient.post('/projectapi/setProject', data={'projectName': 'Project1'})

    # Check if we get the correct status code:
    assert response.status_code == 401

    # Check if the project is still not added to the database:
    assert Projects.query.filter_by(projectName='Project1').first() is None
