from app.models import Projects
from app import db
import json


def testRetrieveNoProjects(testClient, initDatabaseEmpty): 
    '''
        This tests checks that an error message is given when the specified
        user, here with user id 200, has no projects and there are no
        projects in the database.
        Attributes: 
            data: the information to be inserted in the request
            userId: the user for which the files are retrieved
            response: the result of retrieving the files in the specified order
        Arguments: 
            testClient:  the test client we test this for.
            initDatabase: the database instance we test this for. 
    '''
    del initDatabaseEmpty
    # We define the user and the data
    userId = 200

    data = {
        'userId': userId,
    }

    # We do not add any projects to the database

    # We try to retrieve the projects of the user
    response = testClient.get('/projectapi/viewProjectsOfUser', query_string=data)
    
    # Check if the expected response has the correct status code    
    assert response.status_code == 4041

    # Check if the expected response is correct:
    assert response.data == b'researcher has no projects'


def testRetrieveNoProjectsOfUser(testClient, initDatabaseEmpty): 
    '''
        This tests checks that an error message is given when the specified
        user, here with user id 200, has no projects and there are
        projects in the database.
        Attributes: 
            data: the information to be inserted in the request
            userId: the user for which the files are retrieved
            response: the result of retrieving the files in the specified order
        Arguments: 
            testClient:  the test client we test this for.
            initDatabase: the database instance we test this for. 
    '''
    del initDatabaseEmpty
    # We define the user and the data
    userId = 200

    data = {
        'userId': userId,
    }

    # We add a single project to the database, which is not from the user
    project1 = Projects(201, "Project1")
    db.session.add(project1)
    db.session.commit()

    # We try to retrieve the projects of the user
    response = testClient.get('/projectapi/viewProjectsOfUser', query_string=data)

    # Check if the expected response has the correct status code
    assert response.status_code == 4041

    # Check if the expected response is correct:
    assert response.data == b'researcher has no projects'


def testRetrieveSingleProjectOfUser(testClient, initDatabaseEmpty): 
    '''
        This tests checks that a project is given when the specified
        user, here with user id 200, has one project and the database
        contains only one project.
        Attributes: 
            data: the information to be inserted in the request
            userId: the user for which the files are retrieved
            response: the result of retrieving the files in the specified order
        Arguments: 
            testClient:  the test client we test this for.
            initDatabase: the database instance we test this for. 
    '''
    del initDatabaseEmpty
    # We define the user and the data
    userId = 200

    data = {
        'userId': userId,
    }

    # We add a single project to the database, which is from the user
    project1 = Projects(200, "Project1")
    db.session.add(project1)
    db.session.commit()

    # We try to retrieve the projects of the user
    response = testClient.get('/projectapi/viewProjectsOfUser', query_string=data)

    # Check if the expected response has the correct status code
    assert response.status_code == 200

    # Create the expected response:
    expected_response = [dict(userId=200,
                        projectName='Project1', 
                        id=1
                        ), 
                        ]
    # Check if the expected response is correct:
    assert json.loads(response.data) == expected_response


def testRetrieveMultipleProjectsOfUser(testClient, initDatabaseEmpty): 
    '''
        This tests checks that multiple projects are given when the 
        specified user, here with user id 200, has multiple projects.
        Their projects are the only ones in the database.
        Attributes: 
            data: the information to be inserted in the request
            userId: the user for which the files are retrieved
            response: the result of retrieving the files in the specified order
        Arguments: 
            testClient:  the test client we test this for.
            initDatabase: the database instance we test this for. 
    '''
    del initDatabaseEmpty
    # We define the user and the data
    userId = 200

    data = {
        'userId': userId,
    }

    # We add multiple projects to the database, which are all from the user
    project1 = Projects(200, "Project1")
    db.session.add(project1)
    project2 = Projects(200, "Project2")
    db.session.add(project2)
    project3 = Projects(200, "Project3")
    db.session.add(project3)
    db.session.commit()

    # We try to retrieve the projects of the user
    response = testClient.get('/projectapi/viewProjectsOfUser', query_string=data)

    # Check if the expected response has the correct status code
    assert response.status_code == 200

    # Create the expected response:
    expected_response = [dict(userId=200, 
                        projectName='Project1', 
                        id=1
                        ), 
                        dict(userId=200, 
                        projectName='Project2', 
                        id=2
                        ), 
                        dict(userId=200, 
                        projectName='Project3', 
                        id=3
                        ), 
                        ]
    # Check if the expected response is correct:
    assert json.loads(response.data) == expected_response


def testRetrieveOnlyProjectsOfUser(testClient, initDatabaseEmpty): 
    '''
        This tests checks that multiple projects are given when the 
        specified user, here with user id 200, has multiple projects.
        Their projects are not the only ones in the database.
        Attributes: 
            data: the information to be inserted in the request
            userId: the user for which the files are retrieved
            response: the result of retrieving the files in the specified order
        Arguments: 
            testClient:  the test client we test this for.
            initDatabase: the database instance we test this for. 
    '''
    del initDatabaseEmpty
    # We define the user and the data
    userId = 200

    data = {
        'userId': userId,
    }

    # We add multiple projects to the database, which are not all from the user
    project1 = Projects(200, "Project1")
    db.session.add(project1)
    project2 = Projects(201, "Project2")
    db.session.add(project2)
    project3 = Projects(200, "Project3")
    db.session.add(project3)
    db.session.commit()

    # We try to retrieve the projects of the user
    response = testClient.get('/projectapi/viewProjectsOfUser', query_string=data)

    # Check if the expected response has the correct status code    
    assert response.status_code == 200

    # Create the expected response:
    expected_response = [dict(userId=200, 
                        projectName='Project1', 
                        id=1
                        ), 
                        dict(userId=200, 
                        projectName='Project3', 
                        id=3
                        ), 
                        ]
    # Check if the expected response is correct:
    assert json.loads(response.data) == expected_response


