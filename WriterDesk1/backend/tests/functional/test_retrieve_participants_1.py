from app.models import User, Projects
from app import db
from werkzeug.security import check_password_hash

# from werkzeug.utils import secure_filename
import json

def testRetrieveNoParticipants(testClient, initDatabaseEmpty): 
    '''
        This tests checks that an error message is given when the specified
        user, here with user id 200, has no projects and there are no
        projects in the database.
        Attributes: 
            userId: the user for which the files are retrieved
            data: the information to be inserted in the request 
            researcher1: new researcher
            response: the result of retrieving the files in the specified order
        Arguments: 
            testClient:  the test client we test this for.
            initDatabase: the database instance we test this for.
    '''
    del initDatabaseEmpty
    # We define the user and the data
    userId = 201

    data = {
        'userId': userId,
    }

    # We do not add any projects to the database, nor participants, only the user themselves
    # We add a single project with a single user to the database, which is from the user
    researcher1 = User(username="Researcher1", password_plaintext="password2", role="researcher")
    researcher1.id = 201
    db.session.commit()

    # We try to retrieve the participants of the user
    response = testClient.get('/projectapi/viewParticipantsOfUser', query_string=data)
    
    # Check if the expected response has the correct status code    
    assert response.status_code == 404

    # Check if the expected response is correct:
    assert response.data == b'researcher has no participants'

def testRetrieveNoParticipantsOneProject(testClient, initDatabaseEmpty): 
    '''
        This tests checks that an error message is given when the specified
        user, here with user id 200, has a project with no participants 
        and there are no other projects/participants in the database.
        Attributes: 
            userId: the user for which the files are retrieved
            data: the information to be inserted in the request 
            researcher1: new researcher
            project1: new project
            response: the result of retrieving the files in the specified order
        Arguments: 
            testClient:  the test client we test this for.
            initDatabase: the database instance we test this for.
    '''
    del initDatabaseEmpty
    # We define the user and the data
    userId = 201

    data = {
        'userId': userId,
    }

    # We do not add any projects to the database, nor participants, only the user themselves
    # We add a single project with a single user to the database, which is from the user
    researcher1 = User(username="Researcher1", password_plaintext="password2", role="researcher")
    researcher1.id = 201
    db.session.add(researcher1)
    project1 = Projects(userId = 201, projectName = "Project1")
    project1.id = 10
    db.session.add(project1)
    db.session.commit()

    # We try to retrieve the participants of the user
    response = testClient.get('/projectapi/viewParticipantsOfUser', query_string=data)
    
    # Check if the expected response has the correct status code    
    assert response.status_code == 404

    # Check if the expected response is correct:
    assert response.data == b'researcher has no participants'

def testRetrieveNoParticipantsBuExistOtherParticipants(testClient, initDatabaseEmpty): 
    '''
        This tests checks that an error message is given when the specified
        user, here with user id 200, has no projects but there are other
        projects in the database.
        Attributes: 
            userId: the user for which the files are retrieved
            data: the information to be inserted in the request 
            researcher1: new researcher
            project1: new project of researcher
            participant1: new participant
            connection: connectio between participant1 and project1
            response: the result of retrieving the files in the specified order
        Arguments: 
            testClient:  the test client we test this for.
            initDatabase: the database instance we test this for.
    '''
    del initDatabaseEmpty
    # We define the user and the data
    userId = 201

    data = {
        'userId': userId,
    }

    # We do not add any projects to the database, nor participants, only the user themselves
    # We add a single project with a single user to the database, which is from the user
    researcher1 = User(username="Researcher1", password_plaintext="password2", role="researcher")
    researcher1.id = 201
    db.session.add(researcher1)
    researcher2 = User(username="Researcher2", password_plaintext="password3", role="researcher")
    researcher2.id = 202
    db.session.add(researcher1)
    project1 = Projects(userId = 202, projectName = "Project1")
    project1.id = 10
    db.session.add(project1)
    participant1 = User(username="Participant1", password_plaintext="password", role="participant", project=project1.id)
    participant1.id = 200
    db.session.add(participant1)
    db.session.commit()

    # We try to retrieve the participants of the user
    response = testClient.get('/projectapi/viewParticipantsOfUser', query_string=data)
    
    # Check if the expected response has the correct status code    
    assert response.status_code == 404

    # Check if the expected response is correct:
    assert response.data == b'researcher has no participants'

def testRetrieveNoParticipantsButExistOwnProject(testClient, initDatabaseEmpty): 
    '''
        This tests checks that an error message is given when the specified
        user, here with user id 200, has no projects but there are other
        projects in the database.
        Attributes: 
            data: the information to be inserted in the request 
            userId: the user for which the files are retrieved
            researcher1: new researcher
            project1: new project of researcher
            participant1: new participant
            connection: connectio between participant1 and some random project
            response: the result of retrieving the files in the specified order
        Arguments: 
            testClient:  the test client we test this for.
            initDatabase: the database instance we test this for.
    '''
    del initDatabaseEmpty
    # We define the user and the data
    userId = 201

    data = {
        'userId': userId,
    }

    # We do not add any projects to the database, nor participants, only the user themselves
    # We add a single project with a single user to the database, which is from the user
    researcher1 = User(username="Researcher1", password_plaintext="password2", role="researcher")
    researcher1.id = 201
    db.session.add(researcher1)
    researcher2 = User(username="Researcher2", password_plaintext="password3", role="researcher")
    researcher2.id = 202
    db.session.add(researcher1)
    project1 = Projects(userId = 201, projectName = "Project2")
    project1.id = 11
    db.session.add(project1)
    project1 = Projects(userId = 202, projectName = "Project1")
    project1.id = 10
    db.session.add(project1)
    participant1 = User(username="Participant1", password_plaintext="password", role="participant", project=project1.id)
    participant1.id = 200
    db.session.add(participant1)
    db.session.commit()

    # We try to retrieve the participants of the user
    response = testClient.get('/projectapi/viewParticipantsOfUser', query_string=data)
    
    # Check if the expected response has the correct status code    
    assert response.status_code == 404

    # Check if the expected response is correct:
    assert response.data == b'researcher has no participants'

def testRetrieveSingleProjectSingleUserOfUserNoOther(testClient, initDatabase): 
    '''
        This tests checks that a project is given when the specified
        user, here with user id 201, has one project with one participant
        and the database contains only one project.
        Attributes: 
            data: the information to be inserted in the request 
            userId: the user for which the files are retrieved
            researcher1: new researcher
            project1: new project of researcher
            participant1: new participant
            expected_response: response we except
            actual_response: response we get
            response: the result of retrieving the files in the specified order
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

    # We add a single project with a single user to the database, which is from the user
    researcher1 = User(username="Researcher1", password_plaintext="password2", role="researcher")
    researcher1.id = 201
    db.session.add(researcher1)
    project1 = Projects(userId = 201, projectName = "Project1")
    project1.id = 10
    db.session.add(project1)
    participant1 = User(username="Participant1", password_plaintext="password", role="participant", project=project1.id)
    participant1.id = 200
    db.session.add(participant1)
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
                        ), 
                        ]

    # Placing the response data into a variable
    actual_response = json.loads(response.data)
    # Check if the expected response is correct:
    for i in range(len(actual_response)):
        assert actual_response[i]['id'] == expected_response[i]['id']
        assert actual_response[i]['role'] == expected_response[i]['role']
        assert actual_response[i]['username'] == expected_response[i]['username']
        assert(check_password_hash(actual_response[i]['passwordHash'], expected_response[i]['password_plaintext']))

def testRetrieveSingleProjectMultipleParticipantsOfUserNoOther(testClient, initDatabase): 
    '''
        This test checks that multiple participants are given when the specified
        user, here with user id 201, has one project with multiple participants
        and the database contains only one project.
        Attributes: 
            data: the information to be inserted in the request 
            userId: the user for which the files are retrieved
            researcher1: new researcher
            project1: new project of researcher
            participant1: new participant
            participant2: new participant
            participant3: new participant
            connection: connection between participant1 and project1
            connection1: connection between participant2 and project1
            connection2: connection between participant3 and project1
            expected_response: response we except
            actual_response: response we get
            response: the result of retrieving the files in the specified order
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

    # We add a single project with a single user to the database, which is from the user
    researcher1 = User(username="Researcher1", password_plaintext="password2", role="researcher")
    researcher1.id = 201
    db.session.add(researcher1)
    project1 = Projects(userId = 201, projectName = "Project1")
    project1.id = 10
    db.session.add(project1)
    participant1 = User(username="Participant1", password_plaintext="password", role="participant", project=project1.id)
    participant1.id = 200
    db.session.add(participant1)
    participant2 = User(username="Participant2", password_plaintext="password3", role="participant", project=project1.id)
    participant2.id = 203
    db.session.add(participant2)
    participant3 = User(username="Participant3", password_plaintext="password4", role="participant", project=project1.id)
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
                        ), 
                        dict(id = 203,
                        password_plaintext="password3",
                        role = "participant", 
                        username = "Participant2", 
                        ), 
                        dict(id = 204,
                        password_plaintext="password4",
                        role = "participant", 
                        username = "Participant3", 
                        ), 
                        ]

    # Placing the response data into a variable
    actual_response = json.loads(response.data)
    # Check if the expected response is correct:
    for i in range(len(actual_response)):
        assert actual_response[i]['id'] == expected_response[i]['id']
        assert actual_response[i]['role'] == expected_response[i]['role']
        assert actual_response[i]['username'] == expected_response[i]['username']
        assert(check_password_hash(actual_response[i]['passwordHash'], expected_response[i]['password_plaintext']))
