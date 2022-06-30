from app.models import User, Projects
from app import db
from werkzeug.security import check_password_hash

import json

def testRetrieveMultipleProjectSingleParticipantOfUserNoOther(testClient, initDatabase): 
    '''
        This test checks that multiple participants are given when the specified
        user, here with user id 201, has multiple projects with one participant
        and the database contains only these projects.
        Attributes: 
            data: the information to be inserted in the request 
            userId: the user for which the files are retrieved
            researcher1: new user
            participant1: new user
            participant2: new user
            participant3: new user
            project1: new project
            project2: new project
            project3: new project
            connection: connection between project1 and participant1
            connection1: connection between project2 and participant2
            connection2: connection between project3 and participant3
            response: the result of retrieving the files in the specified order
            expected_response: response we expect
            actual_response: response we get
        Arguments: 
            testClient:  the test client we test this for.
            initDatabase: the database instance we test this for.
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
    participant1 = User(username="Participant1", password_plaintext="password", role="participant", project=project1.id)
    participant1.id = 200
    db.session.add(participant1)
    participant2 = User(username="Participant2", password_plaintext="password3", role="participant", project=project2.id)
    participant2.id = 203
    db.session.add(participant2)
    participant3 = User(username="Participant3", password_plaintext="password4", role="participant", project=project3.id)
    participant3.id = 204
    db.session.add(participant3)
    db.session.commit()

    # We try to retrieve the projects of the user
    response = testClient.get('/projectapi/viewParticipantsOfUser', query_string=data)

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
            userId: the user for which the files are retrieved
            researcher1: new user
            participant1: new user
            participant2: new user
            participant3: new user
            participant4: new user
            project1: new project
            project3: new project
            connection: connection between project1 and participant1
            connection1: connection between project1 and participant2
            connection2: connection between project3 and participant3
            connection3: connection between project3 and participant3
            response: the result of retrieving the files in the specified order
            expected_response: response we expect
            actual_response: response we get
        Arguments: 
            testClient:  the test client we test this for.
            initDatabase: the database instance we test this for.
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
    participant1 = User(username="Participant1", password_plaintext="password", role="participant", project=project1.id)
    participant1.id = 200
    db.session.add(participant1)
    participant2 = User(username="Participant2", password_plaintext="password3", role="participant", project=project1.id)
    participant2.id = 203
    db.session.add(participant2)
    participant3 = User(username="Participant3", password_plaintext="password4", role="participant", project=project3.id)
    participant3.id = 204
    db.session.add(participant3)
    participant4 = User(username="Participant4", password_plaintext="password6", role="participant", project=project3.id)
    participant4.id = 206
    db.session.add(participant4)
    db.session.commit()

    # We try to retrieve the projects of the user
    response = testClient.get('/projectapi/viewParticipantsOfUser', query_string=data)

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