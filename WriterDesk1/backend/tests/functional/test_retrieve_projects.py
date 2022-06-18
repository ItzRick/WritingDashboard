# from distutils.command.upload import upload
from app.models import User, ParticipantToProject, Projects
from app.database import getProjectsByResearcher
from app import db
# from datetime import datetime #, date
import os
# from werkzeug.utils import secure_filename
import json

# Possible tests in this file for project retrieval 
# error if no projects
# error if user no projects but project in database
# retrieve one project if user has only one project and one project in db
# retrieve all projects if user has all projects in db
# retrieve only projects of user, db also has project of other users


def testRetrieveNoProjects(testClient, initDatabaseEmpty): 
    '''
        This tests checks that an error message is given when the specified
        user, here with user id 200, has no projects and there are no
        projects in the database.
        Attributes: 
            data: the information to be inserted in the request
        Arguments: 
            testClient:  the test client we test this for.
            initDatabase: the database instance we test this for. 
            userId: the user for which the files are retrieved
            response: the result of retrieving the files in the specified order
    '''
    del initDatabaseEmpty
    # We define the user and the data
    userId = 200

    data = {
        'userId': userId,
    }

    # We do not add any projects to the database

    # We try to retrieve the projects of the user
    response = testClient.get('/projectapi/viewprojectsofuser', query_string=data)
    
    # Check if the expected response has the correct status code    
    assert response.status_code == 4041

    # Create the expected response:
    expected_response = b'researcher has no projects'

    # Check if the expected response is correct:
    assert response.data == expected_response


def testRetrieveNoProjectsOfUser(testClient, initDatabaseEmpty): 
    '''
        This tests checks that an error message is given when the specified
        user, here with user id 200, has no projects and there are
        projects in the database.
        Attributes: 
            data: the information to be inserted in the request
        Arguments: 
            testClient:  the test client we test this for.
            initDatabase: the database instance we test this for. 
            userId: the user for which the files are retrieved
            response: the result of retrieving the files in the specified order
    '''
    del initDatabaseEmpty
    # We define the user and the data
    userId = 200

    data = {
        'userId': userId,
    }

    # We add a single project to the database, which is not from the user
    try:
        db.session.commit()
    except:
        db.session.rollback()
    try: 
        project1 = Projects(201, "Project1")
        db.session.add(project1)
        db.session.commit()
    except:
        db.session.rollback()

    # We try to retrieve the projects of the user
    response = testClient.get('/projectapi/viewprojectsofuser', query_string=data)

    # Check if the expected response has the correct status code
    assert response.status_code == 4041

    # Create the expected response:
    expected_response = b'researcher has no projects'

    # Check if the expected response is correct:
    assert response.data == expected_response


def testRetrieveSingleProjectOfUser(testClient, initDatabaseEmpty): 
    '''
        This tests checks that a project is given when the specified
        user, here with user id 200, has one project and the database
        contains only one project.
        Attributes: 
            data: the information to be inserted in the request
        Arguments: 
            testClient:  the test client we test this for.
            initDatabase: the database instance we test this for. 
            userId: the user for which the files are retrieved
            response: the result of retrieving the files in the specified order
    '''
    del initDatabaseEmpty
    # We define the user and the data
    userId = 200

    data = {
        'userId': userId,
    }

    # We add a single project to the database, which is from the user
    try:
        db.session.commit()
    except:
        db.session.rollback()
    try: 
        project1 = Projects(200, "Project1")
        db.session.add(project1)
        db.session.commit()
    except:
        db.session.rollback()

    # We try to retrieve the projects of the user
    response = testClient.get('/projectapi/viewprojectsofuser', query_string=data)

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
        Arguments: 
            testClient:  the test client we test this for.
            initDatabase: the database instance we test this for. 
            userId: the user for which the files are retrieved
            response: the result of retrieving the files in the specified order
    '''
    del initDatabaseEmpty
    # We define the user and the data
    userId = 200

    data = {
        'userId': userId,
    }

    # We add multiple projects to the database, which are all from the user
    try:
        db.session.commit()
    except:
        db.session.rollback()
    try: 
        project1 = Projects(200, "Project1")
        db.session.add(project1)
        project2 = Projects(200, "Project2")
        db.session.add(project2)
        project3 = Projects(200, "Project3")
        db.session.add(project3)
        db.session.commit()
    except:
        db.session.rollback()

    # We try to retrieve the projects of the user
    response = testClient.get('/projectapi/viewprojectsofuser', query_string=data)

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
        Arguments: 
            testClient:  the test client we test this for.
            initDatabase: the database instance we test this for. 
            userId: the user for which the files are retrieved
            response: the result of retrieving the files in the specified order
    '''
    del initDatabaseEmpty
    # We define the user and the data
    userId = 200

    data = {
        'userId': userId,
    }

    # We add multiple projects to the database, which are not all from the user
    try:
        db.session.commit()
    except:
        db.session.rollback()
    try: 
        project1 = Projects(200, "Project1")
        db.session.add(project1)
        project2 = Projects(201, "Project2")
        db.session.add(project2)
        project3 = Projects(200, "Project3")
        db.session.add(project3)
        db.session.commit()
    except:
        db.session.rollback()

    # We try to retrieve the projects of the user
    response = testClient.get('/projectapi/viewprojectsofuser', query_string=data)

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
    print(expected_response)
    # Check if the expected response is correct:
    assert json.loads(response.data) == expected_response


