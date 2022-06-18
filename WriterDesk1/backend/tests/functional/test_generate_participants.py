from app import generateParticipants as gp
from app import db
from app.models import User, ParticipantToProject, Projects
from test_set_role import loginHelper

def testGenerateParticipants(testClient, initDatabase):
    '''
        Test if generateParticipants() correctly creates participants the database.
        Attributes:
            project: project entry that will be linked with a participant
            ptp: all entries in ParticipantToProject 
            data: dict with usernames and passwords returned by generateParticipants()
        Arguments:
            testClient: the test client we test this for
            initDatabase: the database instance we test this for
    '''

    del testClient, initDatabase
    project = Projects(userId=0, projectName="Project")
    db.session.add(project)
    db.session.commit()
    try:
        data = gp.generateParticipants(3,project.id)
        db.session.commit()
    except Exception as e:
        print(e)
        db.session.rollback()
    ptp = ParticipantToProject.query.filter_by(projectId=project.id).all()
    
    assert len(ptp) == 3
    assert ptp[0].participant.username == "par_" + str(ptp[0].participant.id)
    assert ptp[1].participant.username == "par_" + str(ptp[1].participant.id)
    assert ptp[2].participant.username == "par_" + str(ptp[2].participant.id)

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
    project = Projects(userId=0, projectName="Project")
    db.session.add(project)
    db.session.commit()
    try:
        data = gp.generateParticipants(3,project.id)
        db.session.commit()
    except Exception as e:
        print(e)
        db.session.rollback()
    
    assert len(data) == 3
    for row in data:
        assert row["username"].startswith("par_")
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
    password = gp.generateParticipantPassword(10)
    assert len(password) == 10
    assert any(x.isupper() for x in password) 
    assert any(x.islower() for x in password) 
    assert any(x.isdigit() for x in password)

def testAddParticipantsValid(testClient, initDatabase):
    '''
        Test if adding participants works correctly with an existing project.
        Attributes:
            userid: id of user to create project and participants for
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
    userid = User.query.filter_by(username="Pietje").first()
    project = Projects(userId=userid.id, projectName="Project")
    db.session.add(project)
    db.session.commit()
    data = {
        'count': 2,
        'projectid': project.id,
    }
    access_token = loginHelper(testClient, 'Pietje', 'Bell')
    response = testClient.post('/projectapi/addparticipants', json=data, headers={"Content-Type": "application/json", "Authorization": "Bearer " + access_token})
    assert response.status_code == 200
    ptp = ParticipantToProject.query.filter_by(projectId=project.id).all()
    assert len(ptp) == 2

def testAddParticipantsInvalid(testClient, initDatabase):
    '''
        Test if adding participants fails correctly with a non-existing project.
        Attributes:
            userid: id of user to create project and participants for
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
    userid = User.query.filter_by(username="Pietje").first()
    project = Projects(userId=userid.id, projectName="Project")
    db.session.add(project)
    db.session.commit()

    projectId = project.id
    db.session.delete(project)
    db.session.commit()
    data = {
        'count': 5,
        'projectid': projectId,
    }
    access_token = loginHelper(testClient, 'Pietje', 'Bell')
    response = testClient.post('/projectapi/addparticipants', json=data, headers={"Content-Type": "application/json", "Authorization": "Bearer " + access_token})
    assert response.status_code == 400
    ptp = ParticipantToProject.query.filter_by(projectId=projectId).all()
    assert len(ptp) == 0
