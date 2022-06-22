from app.models import User, ParticipantToProject, Projects
from app import db
from werkzeug.security import check_password_hash

import json

def testRetrieveSingleProjectMultiplearticipantOfUserWithOther(testClient, initDatabase): 
    '''
        This test checks that a single participant is given when the specified
        user, here with user id 201, has one project with one participant
        and the database contains other projects.
        Attributes: 
            data: the information to be inserted in the request
        Arguments: 
            testClient:  the test client we test this for.
            initDatabase: the database instance we test this for. 
            userId: the user for which the files are retrieved
            response: the result of retrieving the files in the specified order
    '''
    del initDatabase
    # We define the user and the data
    userId = 201

    data = {
        'userId': userId,
    }

    researcher1 = User(username="Researcher1", password_plaintext="password2", role="researcher")
    researcher1.id = 201
    db.session.add(researcher1)
    project1 = Projects(userId = 201, projectName = "Project1")
    project1.id = 10
    db.session.add(project1)
    researcher2 = User(username="Researcher2", password_plaintext="password5", role="researcher")
    researcher2.id = 205
    db.session.add(researcher2)
    project2 = Projects(userId = 205, projectName = "Project2")
    project2.id = 11
    db.session.add(project2)
    participant1 = User(username="Participant1", password_plaintext="password", role="participant")
    participant1.id = 200
    db.session.add(participant1)
    participant2 = User(username="Participant2", password_plaintext="password3", role="participant")
    participant2.id = 203
    db.session.add(participant2)
    participant3 = User(username="Participant3", password_plaintext="password4", role="participant")
    participant3.id = 204
    db.session.add(participant3)
    participant4 = User(username="Participant4", password_plaintext="password6", role="participant")
    participant4.id = 206
    db.session.add(participant4)
    connection = ParticipantToProject(200, 10)
    db.session.add(connection)
    connection1 = ParticipantToProject(203, 11)
    db.session.add(connection1)
    connection2 = ParticipantToProject(204, 11)
    db.session.add(connection2)
    connection3 = ParticipantToProject(206, 10)
    db.session.add(connection3)
    db.session.commit()

    # We try to retrieve the projects of the user
    response = testClient.get('/projectapi/viewparticipantsofuser', query_string=data)

    # Check if the expected response has the correct status code
    assert response.status_code == 200

    # Create the expected response:
    expected_response = [dict(id = 200,
                        password_plaintext="password",
                        role = "participant", 
                        username = "Participant1", 
                        projectid = 10, 
                        projectname = "Project1", 
                        ), 
                        dict(id = 206,
                        password_plaintext="password6",
                        role = "participant", 
                        username = "Participant4", 
                        projectid = 10, 
                        projectname = "Project1", 
                        ), 
                        ]

    # Placing the response data into a variable
    actual_response = json.loads(response.data)
    # Check if the expected response is correct:
    for i in range(len(actual_response)):
        assert actual_response[i]['id'] == expected_response[i]['id']
        assert actual_response[i]['role'] == expected_response[i]['role']
        assert actual_response[i]['username'] == expected_response[i]['username']
        assert actual_response[i]['projectid'] == expected_response[i]['projectid']
        assert actual_response[i]['projectname'] == expected_response[i]['projectname']
        assert(check_password_hash(actual_response[i]['passwordHash'], expected_response[i]['password_plaintext']))

def testRetrieveMultipleProjectsSingleParticipantOfUserNoOther(testClient, initDatabase): 
    '''
        This test checks that a single participant is given when the specified
        user, here with user id 201, has multiple projects where only one has one 
        participant and the database contains no other projects.
        Attributes: 
            data: the information to be inserted in the request
        Arguments: 
            testClient:  the test client we test this for.
            initDatabase: the database instance we test this for. 
            userId: the user for which the files are retrieved
            response: the result of retrieving the files in the specified order
    '''
    del initDatabase
    # We define the user and the data
    userId = 201

    data = {
        'userId': userId,
    }

    researcher1 = User(username="Researcher1", password_plaintext="password2", role="researcher")
    researcher1.id = 201
    db.session.add(researcher1)
    project1 = Projects(userId = 201, projectName = "Project1")
    project1.id = 10
    db.session.add(project1)
    project2 = Projects(userId = 201, projectName = "Project2")
    project2.id = 11
    db.session.add(project2)
    project3 = Projects(userId = 201, projectName = "Project3")
    project3.id = 12
    db.session.add(project3)
    participant1 = User(username="Participant1", password_plaintext="password", role="participant")
    participant1.id = 200
    db.session.add(participant1)
    connection = ParticipantToProject(200, 10)
    db.session.add(connection)
    db.session.commit()

    # We try to retrieve the projects of the user
    response = testClient.get('/projectapi/viewparticipantsofuser', query_string=data)

    # Check if the expected response has the correct status code
    assert response.status_code == 200

    # Create the expected response:
    expected_response = [dict(id = 200,
                        password_plaintext="password",
                        role = "participant", 
                        username = "Participant1", 
                        projectid = 10, 
                        projectname = "Project1", 
                        ), 
                        ]

    # Placing the response data into a variable
    actual_response = json.loads(response.data)
    # Check if the expected response is correct:
    for i in range(len(actual_response)):
        assert actual_response[i]['id'] == expected_response[i]['id']
        assert actual_response[i]['role'] == expected_response[i]['role']
        assert actual_response[i]['username'] == expected_response[i]['username']
        assert actual_response[i]['projectid'] == expected_response[i]['projectid']
        assert actual_response[i]['projectname'] == expected_response[i]['projectname']
        assert(check_password_hash(actual_response[i]['passwordHash'], expected_response[i]['password_plaintext']))

def testRetrieveMultipleProjectSingleParticipantOfUserWithOther(testClient, initDatabase): 
    '''
        This test checks that a single participant is given when the specified
        user, here with user id 201, has one project with one participant
        and other projects without participants and the database contains other projects.
        Attributes: 
            data: the information to be inserted in the request
        Arguments: 
            testClient:  the test client we test this for.
            initDatabase: the database instance we test this for. 
            userId: the user for which the files are retrieved
            response: the result of retrieving the files in the specified order
    '''
    del initDatabase
    # We define the user and the data
    userId = 201

    data = {
        'userId': userId,
    }

    researcher1 = User(username="Researcher1", password_plaintext="password2", role="researcher")
    researcher1.id = 201
    db.session.add(researcher1)
    project1 = Projects(userId = 201, projectName = "Project1")
    project1.id = 10
    db.session.add(project1)
    project3 = Projects(userId = 201, projectName = "Project3")
    project3.id = 12
    db.session.add(project3)
    researcher2 = User(username="Researcher2", password_plaintext="password5", role="researcher")
    researcher2.id = 205
    db.session.add(researcher2)
    project2 = Projects(userId = 205, projectName = "Project2")
    project2.id = 11
    db.session.add(project2)
    project4 = Projects(userId = 205, projectName = "Project4")
    project4.id = 13
    db.session.add(project4)
    participant1 = User(username="Participant1", password_plaintext="password", role="participant")
    participant1.id = 200
    db.session.add(participant1)
    participant2 = User(username="Participant2", password_plaintext="password3", role="participant")
    participant2.id = 203
    db.session.add(participant2)
    participant3 = User(username="Participant3", password_plaintext="password4", role="participant")
    participant3.id = 204
    db.session.add(participant3)
    participant4 = User(username="Participant4", password_plaintext="password6", role="participant")
    participant4.id = 206
    db.session.add(participant4)
    connection = ParticipantToProject(200, 10)
    db.session.add(connection)
    connection1 = ParticipantToProject(203, 11)
    db.session.add(connection1)
    connection2 = ParticipantToProject(204, 11)
    db.session.add(connection2)
    connection3 = ParticipantToProject(206, 13)
    db.session.add(connection3)
    db.session.commit()

    # We try to retrieve the projects of the user
    response = testClient.get('/projectapi/viewparticipantsofuser', query_string=data)

    # Check if the expected response has the correct status code
    assert response.status_code == 200

    # Create the expected response:
    expected_response = [dict(id = 200,
                        password_plaintext="password",
                        role = "participant", 
                        username = "Participant1", 
                        projectid = 10, 
                        projectname = "Project1", 
                        ), 
                        ]

    # Placing the response data into a variable
    actual_response = json.loads(response.data)
    # Check if the expected response is correct:
    for i in range(len(actual_response)):
        assert actual_response[i]['id'] == expected_response[i]['id']
        assert actual_response[i]['role'] == expected_response[i]['role']
        assert actual_response[i]['username'] == expected_response[i]['username']
        assert actual_response[i]['projectid'] == expected_response[i]['projectid']
        assert actual_response[i]['projectname'] == expected_response[i]['projectname']
        assert(check_password_hash(actual_response[i]['passwordHash'], expected_response[i]['password_plaintext']))

def testRetrieveMultipleProjectSingleParticipantOfUserNoOther(testClient, initDatabase): 
    '''
        This test checks that multiple participants are given when the specified
        user, here with user id 201, has multiple projects with one participant
        and the database contains only these projects.
        Attributes: 
            data: the information to be inserted in the request
        Arguments: 
            testClient:  the test client we test this for.
            initDatabase: the database instance we test this for. 
            userId: the user for which the files are retrieved
            response: the result of retrieving the files in the specified order
    '''
    del initDatabase
    # We define the user and the data
    userId = 201

    data = {
        'userId': userId,
    }

    researcher1 = User(username="Researcher1", password_plaintext="password2", role="researcher")
    researcher1.id = 201
    db.session.add(researcher1)
    project1 = Projects(userId = 201, projectName = "Project1")
    project1.id = 10
    db.session.add(project1)
    project3 = Projects(userId = 201, projectName = "Project3")
    project3.id = 12
    db.session.add(project3)
    project2 = Projects(userId = 201, projectName = "Project2")
    project2.id = 11
    db.session.add(project2)
    participant1 = User(username="Participant1", password_plaintext="password", role="participant")
    participant1.id = 200
    db.session.add(participant1)
    participant2 = User(username="Participant2", password_plaintext="password3", role="participant")
    participant2.id = 203
    db.session.add(participant2)
    participant3 = User(username="Participant3", password_plaintext="password4", role="participant")
    participant3.id = 204
    db.session.add(participant3)
    connection = ParticipantToProject(200, 10)
    db.session.add(connection)
    connection1 = ParticipantToProject(203, 11)
    db.session.add(connection1)
    connection2 = ParticipantToProject(204, 12)
    db.session.add(connection2)
    db.session.commit()

    # We try to retrieve the projects of the user
    response = testClient.get('/projectapi/viewparticipantsofuser', query_string=data)

    # Check if the expected response has the correct status code
    assert response.status_code == 200

    # Create the expected response:
    expected_response = [dict(id = 200,
                        password_plaintext="password",
                        role = "participant", 
                        username = "Participant1", 
                        projectid = 10, 
                        projectname = "Project1", 
                        ), 
                        dict(id = 203,
                        password_plaintext="password3",
                        role = "participant", 
                        username = "Participant2", 
                        projectid = 11, 
                        projectname = "Project2", 
                        ), 
                        dict(id = 204,
                        password_plaintext="password4",
                        role = "participant", 
                        username = "Participant3", 
                        projectid = 12, 
                        projectname = "Project3", 
                        ), 
                        ]

    # Placing the response data into a variable
    actual_response = json.loads(response.data)
    # Check if the expected response is correct:
    for i in range(len(actual_response)):
        assert actual_response[i]['id'] == expected_response[i]['id']
        assert actual_response[i]['role'] == expected_response[i]['role']
        assert actual_response[i]['username'] == expected_response[i]['username']
        assert actual_response[i]['projectid'] == expected_response[i]['projectid']
        assert actual_response[i]['projectname'] == expected_response[i]['projectname']
        assert(check_password_hash(actual_response[i]['passwordHash'], expected_response[i]['password_plaintext']))

def testRetrieveMultipleProjectMultipleParticipantsOfUserNoOther(testClient, initDatabase): 
    '''
        This test checks that multiple participants are given when the specified
        user, here with user id 201, has multiple projects with multiple participants
        and the database contains only these projects.
        Attributes: 
            data: the information to be inserted in the request
        Arguments: 
            testClient:  the test client we test this for.
            initDatabase: the database instance we test this for. 
            userId: the user for which the files are retrieved
            response: the result of retrieving the files in the specified order
    '''
    del initDatabase
    # We define the user and the data
    userId = 201

    data = {
        'userId': userId,
    }

    researcher1 = User(username="Researcher1", password_plaintext="password2", role="researcher")
    researcher1.id = 201
    db.session.add(researcher1)
    project1 = Projects(userId = 201, projectName = "Project1")
    project1.id = 10
    db.session.add(project1)
    project3 = Projects(userId = 201, projectName = "Project3")
    project3.id = 12
    db.session.add(project3)
    participant1 = User(username="Participant1", password_plaintext="password", role="participant")
    participant1.id = 200
    db.session.add(participant1)
    participant2 = User(username="Participant2", password_plaintext="password3", role="participant")
    participant2.id = 203
    db.session.add(participant2)
    participant3 = User(username="Participant3", password_plaintext="password4", role="participant")
    participant3.id = 204
    db.session.add(participant3)
    participant4 = User(username="Participant4", password_plaintext="password6", role="participant")
    participant4.id = 206
    db.session.add(participant4)
    connection = ParticipantToProject(200, 10)
    db.session.add(connection)
    connection1 = ParticipantToProject(203, 10)
    db.session.add(connection1)
    connection2 = ParticipantToProject(204, 12)
    db.session.add(connection2)
    connection3 = ParticipantToProject(206, 12)
    db.session.add(connection3)
    db.session.commit()

    # We try to retrieve the projects of the user
    response = testClient.get('/projectapi/viewparticipantsofuser', query_string=data)

    # Check if the expected response has the correct status code
    assert response.status_code == 200

    # Create the expected response:
    expected_response = [dict(id = 200,
                        password_plaintext="password",
                        role = "participant", 
                        username = "Participant1", 
                        projectid = 10, 
                        projectname = "Project1", 
                        ), 
                        dict(id = 203,
                        password_plaintext="password3",
                        role = "participant", 
                        username = "Participant2", 
                        projectid = 10, 
                        projectname = "Project1", 
                        ), 
                        dict(id = 204,
                        password_plaintext="password4",
                        role = "participant", 
                        username = "Participant3", 
                        projectid = 12, 
                        projectname = "Project3", 
                        ), 
                        dict(id = 206,
                        password_plaintext="password6",
                        role = "participant", 
                        username = "Participant4", 
                        projectid = 12, 
                        projectname = "Project3", 
                        ), 
                        ]

    # Placing the response data into a variable
    actual_response = json.loads(response.data)
    # Check if the expected response is correct:
    for i in range(len(actual_response)):
        assert actual_response[i]['id'] == expected_response[i]['id']
        assert actual_response[i]['role'] == expected_response[i]['role']
        assert actual_response[i]['username'] == expected_response[i]['username']
        assert actual_response[i]['projectid'] == expected_response[i]['projectid']
        assert actual_response[i]['projectname'] == expected_response[i]['projectname']
        assert(check_password_hash(actual_response[i]['passwordHash'], expected_response[i]['password_plaintext']))
