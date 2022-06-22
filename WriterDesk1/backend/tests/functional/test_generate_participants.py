from app import generateParticipants as gp
from app import db
from app.models import User, ParticipantToProject, Projects

def testGenerateParticipants(testClient, initDatabase):
    '''
        Test if generateParticipants() correctly creates participants the database.
        Attributes:
            project: project entry that will be linked with a participant
            ptp: all entries in ParticipantToProject 
        Arguments:
            testClient: the test client we test this for
            initDatabase: the database instance we test this for
    '''

    del testClient, initDatabase
    project = Projects(userId=0, projectName="Project")
    db.session.add(project)
    db.session.commit()
    try:
        gp.generateParticipants(3,project.id)
        db.session.commit()
    except Exception as e:
        print(e)
        db.session.rollback()
    ptp = ParticipantToProject.query.filter_by(projectId=project.id).all()
    
    assert len(ptp) == 3
    assert ptp[0].participant.username == "par_" + str(ptp[0].participant.id)
    assert ptp[1].participant.username == "par_" + str(ptp[1].participant.id)
    assert ptp[2].participant.username == "par_" + str(ptp[2].participant.id)

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
            project: project entry that will be linked with a participant
            data: count and projectId input for the post request
            response: response of the post request
            ptp: all entries in ParticipantToProject with the projectId of the project
        Arguments:
            testClient: the test client we test this for
            initDatabase: the database instance we test this for
    '''

    del initDatabase
    project = Projects(userId=0, projectName="Project")
    db.session.add(project)
    db.session.commit()
    data = {
        'count': 2,
        'projectid': project.id,
    }
    response = testClient.post('/projectapi/addparticipants', json=data, headers={"Content-Type": "application/json"})
    assert response.status_code == 200
    ptp = ParticipantToProject.query.filter_by(projectId=project.id).all()
    assert len(ptp) == 2

def testAddParticipantsInvalid(testClient, initDatabase):
    '''
        Test if adding participants fails correctly with a non-existing project.
        Attributes:
            project: project entry that will be linked with a participant
            projectId: id of the project
            data: count and projectId input for the post request
            response: response of the post request
            ptp: all entries in ParticipantToProject with the projectId of the project
        Arguments:
            testClient: the test client we test this for
            initDatabase: the database instance we test this for
    '''

    del initDatabase
    project = Projects(userId=0, projectName="Project")
    db.session.add(project)
    db.session.commit()

    projectId = project.id
    db.session.delete(project)
    db.session.commit()
    data = {
        'count': 5,
        'projectid': projectId,
    }
    response = testClient.post('/projectapi/addparticipants', json=data, headers={"Content-Type": "application/json"})
    assert response.status_code == 400
    ptp = ParticipantToProject.query.filter_by(projectId=projectId).all()
    assert len(ptp) == 0
