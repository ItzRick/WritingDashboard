from app import generateParticipants as gp
from app import db
from app.models import User, ParticipantToProject, Projects

def testGenerateParticipants(testClient, initDatabase):
    del testClient, initDatabase
    project = Projects(field=0)
    db.session.add(project)
    db.session.commit()
    try:
        gp.generateParticipants(3,project.id)
        db.session.commit()
    except Exception as e:
        print(e)
        db.session.rollback()
    ptp = ParticipantToProject.query.all()
    
    assert len(ptp) == 3
    assert ptp[0].participant.username == "par_" + str(ptp[0].participant.id)
    assert ptp[1].participant.username == "par_" + str(ptp[1].participant.id)
    assert ptp[2].participant.username == "par_" + str(ptp[2].participant.id)

def testGenerateParticipantUsername(testClient, initDatabase):
    del testClient, initDatabase
    assert gp.generateParticipantUsername(1) == "par_1"

def testGenerateParticipantPassword(testClient, initDatabase):
    del testClient, initDatabase
    password = gp.generateParticipantPassword(10)
    assert len(password) == 10
    assert any(x.isupper() for x in password) 
    assert any(x.islower() for x in password) 
    assert any(x.isdigit() for x in password)

def testAddParticipantsValid(testClient, initDatabase):
    del initDatabase
    project = Projects(field=0)
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
    del initDatabase
    project = Projects(field=0)
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
