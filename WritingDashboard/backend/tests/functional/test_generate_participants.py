from app import generateParticipants as gp
from app import db
from app.models import User, ParticipantToProject, Projects
from test_set_role import loginHelper
from pytest import raises
from flask import current_app
from os.path import exists, join

def testGenerateParticipants(testClient, initDatabase):
    '''
        Test if generateParticipants() correctly creates participants in the database.
        Attributes:
            project: project entry that will be linked with a participant
            ptps: all entries in ParticipantToProject for the project
            data: dict with usernames and passwords returned by generateParticipants()
        Arguments:
            testClient: the test client we test this for
            initDatabase: the database instance we test this for
    '''
    del testClient, initDatabase
    
    # Create a new project
    project = Projects(userId=0, projectName="Project")
    db.session.add(project)
    db.session.commit()

    # Try to add participants to the project
    data = gp.generateParticipants(3, project.id)
    db.session.commit()

    # Check if particpants are created: check for ParticipantToProject entries,
    # and the username and role of corresponsing User entries
    ptps = ParticipantToProject.query.filter_by(projectId=project.id).all()
    assert len(ptps) == 3
    for ptp in ptps:
        assert ptp.participant.username == "par_" + str(ptp.participant.id)
        assert ptp.participant.role == "participant"

def testGenerateParticipantsData(testClient, initDatabase):
    '''
        Test if generateParticipants() correctly returns a dictionary with usernames and passwords.
        Attributes:
            project: project entry that will be linked with a participant
            data: dict with usernames and passwords returned by generateParticipants()
        Arguments:
            testClient: the test client we test this for
            initDatabase: the database instance we test this for
    '''
    del testClient, initDatabase

    # Create a new project
    project = Projects(userId=0, projectName="Project")
    db.session.add(project)
    db.session.commit()

    # Try to add participants to the project
    data = gp.generateParticipants(3,project.id)
    db.session.commit()
    
    # Check if dictionary with correct data is returned
    # every row should have a valid username and a password of at least 
    # 8 characters with a lowercase and uppercase character and number
    assert len(data) == 3
    for row in data:
        assert row["username"].startswith("par_")
        assert len(row["password"]) >= 8
        assert any(x.isupper() for x in row["password"]) 
        assert any(x.islower() for x in row["password"]) 
        assert any(x.isdigit() for x in row["password"])

def testGenerateParticipantUsername(testClient, initDatabase):
    '''
        Test if generateParticipantUsername() correctly returns a username from the given id.
        Arguments:
            testClient: the test client we test this for
            initDatabase: the database instance we test this for
    '''

    del testClient, initDatabase
    assert gp.generateParticipantUsername(1) == "par_1"

def testGenerateParticipantPassword(testClient, initDatabase):
    '''
        Test if generateParticipantPassword() correctly returns a valid password.
        Attributes:
            password: string returned by generateParticipantPassword
        Arguments:
            testClient: the test client we test this for
            initDatabase: the database instance we test this for
    '''

    del testClient, initDatabase

    # Generate a password
    password = gp.generateParticipantPassword(10)

    # Check if password has length 10 and contains at least 1 lowercase and uppercase character and a number
    assert len(password) == 10
    assert any(x.isupper() for x in password) 
    assert any(x.islower() for x in password) 
    assert any(x.isdigit() for x in password)

def testGenerateParticipantPasswordInvalidLength(testClient, initDatabase):
    '''
        Test if generateParticipantPassword() correctly raises an exception when the given password length is too short.
        Attributes:
            password: string returned by generateParticipantPassword
            e: exception raised by generateParticipantPassword
        Arguments:
            testClient: the test client we test this for
            initDatabase: the database instance we test this for
    '''

    del testClient, initDatabase

    # Generate a password with length < 8
    with raises(Exception) as e:
        password = gp.generateParticipantPassword(7)

    # Check for the correct error message
    assert str(e.value) == "Password should be at least 8 characters long"

def testAddParticipantsValid(testClient, initDatabase):
    '''
        Test if adding participants works correctly with an existing project.
        Attributes:
            user: user to create project and participants for
            project: project entry that will be linked with a participant
            data: count and projectId input for the post request
            access_token: login token to allow the request to be done
            response: response of the post request
            ptp: all entries in ParticipantToProject with the projectId of the project
        Arguments:
            testClient: the test client we test this for
            initDatabase: the database instance we test this for
    '''

    del initDatabase

    # Retrieve user and create project for them
    user = User.query.filter_by(username="Pietje").first()
    project = Projects(userId=user.id, projectName="Project")
    db.session.add(project)
    db.session.commit()

    # Post http request as user to add participants to the project
    data = {
        'nrOfParticipants': 2,
        'projectid': project.id,
    }
    access_token = loginHelper(testClient, 'Pietje', 'Bell')
    response = testClient.post('/projectapi/addParticipants', json=data, headers={"Content-Type": "application/json", "Authorization": "Bearer " + access_token})
    
    # Loop through generator to reach the removal of the file
    for i in response.response:
        pass

    # Check if file was removed
    assert not exists(join(current_app.config['UPLOAD_FOLDER'], str(user.id), "downloadParticipants.csv"))

    # Check if particpants were added
    assert response.status_code == 200
    ptp = ParticipantToProject.query.filter_by(projectId=project.id).all()
    assert len(ptp) == 2

def testAddParticipantsInvalidProject(testClient, initDatabase):
    '''
        Test if adding participants fails correctly with a non-existing project.
        Attributes:
            user: id of user to create project and participants for
            project: project entry that will be linked with a participant
            projectId: id of the project
            data: count and projectId input for the post request
            access_token: login token to allow the request to be done
            response: response of the post request
            ptp: all entries in ParticipantToProject with the projectId of the project
        Arguments:
            testClient: the test client we test this for
            initDatabase: the database instance we test this for
    '''

    del initDatabase
    
    # Retrieve user and create project for them
    user = User.query.filter_by(username="Pietje").first()
    project = Projects(userId=user.id, projectName="Project")
    db.session.add(project)
    db.session.commit()

    # Delete the project; no participants should be able te be added
    projectId = project.id
    db.session.delete(project)
    db.session.commit()

    # Post http request as user to add participants to the project
    data = {
        'nrOfParticipants': 5,
        'projectid': projectId,
    }
    access_token = loginHelper(testClient, 'Pietje', 'Bell')
    response = testClient.post('/projectapi/addParticipants', json=data, headers={"Content-Type": "application/json", "Authorization": "Bearer " + access_token})

    # Check if particpants were not added
    assert response.status_code == 400
    ptp = ParticipantToProject.query.filter_by(projectId=projectId).all()
    assert len(ptp) == 0
