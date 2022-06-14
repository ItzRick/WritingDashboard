from app import generateParticipants as gp
from app import db
from app.models import User, ParticipantToProject

def testGenerateParticipants(testClient, initDatabase):
    del testClient, initDatabase
    try:
        gp.generateParticipants(3,1)
        db.session.commit()
    except Exception as e:
        print(e)
        db.session.rollback()
    ptp = ParticipantToProject.query.all()
    
    assert len(ptp) == 3
    assert ptp[0].participant.username == "par_1"
    assert ptp[1].participant.username == "par_2"
    assert ptp[2].participant.username == "par_3"

def testGenerateParticipantUsername(testClient, initDatabase):
    assert gp.generateParticipantUsername(0) == "par_1"
