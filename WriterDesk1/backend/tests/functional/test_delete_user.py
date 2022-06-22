from datetime import datetime

from app import db
from app.models import User, Files, Explanations, Projects, ParticipantToProject, Scores
from app.usersapi.routes import deleteUser
from test_set_role import loginHelper


def testDeleteUser(testClient, initDatabase):
    '''
        Test if we can remove a user from the database using the deleteUser(userID) method and whether everything
        related to said user gets deleted properly.
        We first add an entry to every table and make sure all of them relate to one user,
        we also create a participant user that belongs to a project that the user to be deleted owns.
        This participant should also get deleted.
        After we have removed this user, we check that we can indeed not query on this user and all the related
            entries.
        Attributes:
            user: the user to be deleted
            userID: id belonging to user
            file: file owned by user
            fileID: id beloning to file
            explanation: explanation of feedback belonging to file
            project: project owned by user
            projectID: id belonging to project
            participant: participant user in project
            participantID: id belonging to participant
            participantToProject: participantToProject entry relating participant to project
            scores: scores of file
        Arguments:
            testClient:  The test client we test this for.
            initDatabase: the database instance we test this for.
    '''
    del testClient, initDatabase
    try:
        db.session.commit()
    except:
        db.session.rollback()
        assert False
    try:
        user = User(username='John', password_plaintext='test')
        db.session.add(user)
        userID = User.query.filter_by(username='John').first().id
        file = Files(
            path='C:/Users/20192435/Downloads/SEP2021/WriterDesk1/backend/saved_documents/ScrumAndXpFromTheTrenchesonline07-31.pdf',
            filename='ScrumAndXpFromTheTrenchesonline07-31.pdf', date=datetime(2019, 2, 12), userId=userID,
            courseCode='2IPE0', fileType='.pdf')
        # Add the file to the database:
        db.session.add(file)
        fileID = Files.query.filter_by(userId=userID).first().id
        explanation = Explanations(fileId=fileID)
        db.session.add(explanation)
        project = Projects(userId=userID, projectName='test')
        db.session.add(project)
        projectID = Projects.query.filter_by(userId=userID).first().id
        participant = User(username='Kevin', role='participant', password_plaintext='test')
        db.session.add(participant)
        participantID = User.query.filter_by(username='Kevin').first().id
        participantToProject = ParticipantToProject(userId=participantID, projectId=projectID)
        db.session.add(participantToProject)
        scores = Scores(fileId=fileID)
        db.session.add(scores)
        db.session.commit()
    except:
        db.session.rollback()
        assert False
    deleteUser(userID)
    assert User.query.filter_by(username='John').first() is None
    assert Files.query.filter_by(userId=userID).first() is None
    assert Explanations.query.filter_by(fileId=fileID).first() is None
    assert Projects.query.filter_by(userId=userID).first() is None
    assert User.query.filter_by(username='Kevin').first() is None
    assert ParticipantToProject.query.filter_by(userId=participantID).first() is None
    assert Scores.query.filter_by(fileId=fileID).first() is None
    assert User.query.filter_by(id=participantID).first() is None


def testNotAdmin(testClient, initDatabase):
    '''
        Test whether the correct error is thrown when trying to to delete an user using the deleteUserAdmin
        api call while logged in with an account that does not have the admin role.
        Attributes:
            user: the user to be deleted
            userID: id belonging to user
            access_token: the access token
            response: the response of the api call
        Arguments:
            testClient:  The test client we test this for.
            initDatabase: the database instance we test this for.
    '''
    del initDatabase
    user = User.query.filter_by(username='Pietje').first()
    # get his user id
    userId = user.id

    assert User.query.filter_by(id=userId).first() is not None

    # get access token for Pietje Bell
    access_token = loginHelper(testClient, 'Pietje', 'Bell')

    response = testClient.post('/usersapi/deleteUserAdmin', data={'userID': -1},
                               headers={"Authorization": "Bearer " + access_token})
    assert response.status_code == 403
    assert response.data == b'Method only accessible for admin users'


def testAdmin(testClient, initDatabase):
    '''
        Test if we can remove a user from the database using the deleteUserAdmin api call while logged in as an admin
        and whether the correct error is thrown when trying to delete a non existent user.
        We also check if we receive the correct http code when the deletion is successful.
        Attributes:
            user: the user to be deleted
            userID: id belonging to user
            access_token: the access token
            response: the response of the api call
        Arguments:
            testClient:  The test client we test this for.
            initDatabase: the database instance we test this for.
    '''
    del initDatabase
    try:
        db.session.commit()
    except:
        db.session.rollback()
        assert False
    try:
        user = User(username='John', password_plaintext='test')
        db.session.add(user)
        db.session.commit()
    except:
        db.session.rollback()
        assert False
    userID = User.query.filter_by(username='John').first().id
    userId = User.query.filter_by(username='ad').first().id

    assert User.query.filter_by(id=userId).first() is not None

    # get access token for Ad
    access_token = loginHelper(testClient, 'ad', 'min')

    # attempt to delete user with id -1, which does not exist
    response = testClient.post('/usersapi/deleteUserAdmin', json={'userID': -1},
                               headers={"Authorization": "Bearer " + access_token})
    assert response.status_code == 404
    assert response.data == b'User does not exist'

    response = testClient.post('/usersapi/deleteUserAdmin', json={'userID': userID},
                               headers={"Authorization": "Bearer " + access_token})
    assert response.status_code == 200
    assert response.data == b'Account deleted!'


def testNotResearcher(testClient, initDatabase):
    '''
        Test whether the correct error is thrown when trying to to delete a participant using the deleteUserResearcher
        api call while logged in with an account that does not have the admin or researcher role.
        Attributes:
            user: the user to be deleted
            userID: id belonging to user
            access_token: the access token
            response: the response of the api call
        Arguments:
            testClient:  The test client we test this for.
            initDatabase: the database instance we test this for.
        '''
    del initDatabase
    user = User.query.filter_by(username='Pietje').first()
    # get his user id
    userId = user.id

    assert User.query.filter_by(id=userId).first() is not None

    # get access token for Pietje Bell
    access_token = loginHelper(testClient, 'Pietje', 'Bell')

    response = testClient.post('/usersapi/deleteUserResearcher', json={'userID': -1},
                               headers={"Authorization": "Bearer " + access_token})
    assert response.status_code == 403
    assert response.data == b'Method only accessible for researcher and admin users'


def testResearcher(testClient, initDatabase):
    '''
        Test if we can remove a participant user from the database using the deleteUserResearcher api call.
        We also create a participant user that belongs to a project that the user to be deleted owns.
        This participant and the participantToProject entry should also get deleted.
        After we have removed this user, we check whether the response is correct.
        We also test whether the correct error is thrown when trying to delete a non existent participant and when
        trying to delete a participant that does not belong to a project owned by the logged in researcher.
        Attributes:
            user: the user to be deleted
            userID: id belonging to user
            project: project owned by user
            projectID: id belonging to project
            unrelatedProject: project not owned by user
            unrelatedProjectID: id belonging to unrelatedProject
            participant: participant user in project
            participantID: id belonging to participant
            urelatedParticipant: participant user in unrelatedProject
            unrelatedParticipantID: id belonging to unrelatedParticipant
            participantToProject: participantToProject entry relating participant to project
            unrelatedParticipantToProject: participantToProject entry relating unrelatedParticipant to unrelatedProject
            access_token: the access token
            response: the response of the api call
        Arguments:
            testClient:  The test client we test this for.
            initDatabase: the database instance we test this for.
    '''
    del initDatabase
    try:
        db.session.commit()
    except:
        db.session.rollback()
        assert False
    try:
        user = User.query.filter_by(username='ad').first()
        # get his user id
        userId = user.id
        project = Projects(userId=userId, projectName='test')
        db.session.add(project)
        unrelatedProject = Projects(userId=-1, projectName='test2')
        db.session.add(unrelatedProject)
        projectID = Projects.query.filter_by(userId=userId).first().id
        unrelatedProjectID = Projects.query.filter_by(userId=-1).first().id
        participant = User(username='Kevin', role='participant', password_plaintext='test')
        db.session.add(participant)
        participantID = User.query.filter_by(username='Kevin').first().id
        unrelatedParticipant = User(username='David', role='participant', password_plaintext='test')
        db.session.add(unrelatedParticipant)
        unrelatedParticipantID = User.query.filter_by(username='David').first().id
        participantToProject = ParticipantToProject(userId=participantID, projectId=projectID)
        db.session.add(participantToProject)
        unrelatedParticipantToProject = ParticipantToProject(userId=unrelatedParticipantID,
                                                             projectId=unrelatedProjectID)
        db.session.add(unrelatedParticipantToProject)
        db.session.commit()
    except:
        db.session.rollback()
        assert False

    assert User.query.filter_by(id=userId).first() is not None

    # get access token for Ad
    access_token = loginHelper(testClient, 'ad', 'min')

    # attempt to delete user with id -1, which does not exist
    response = testClient.post('/usersapi/deleteUserResearcher', json={'userID': -1},
                               headers={"Authorization": "Bearer " + access_token})
    assert response.status_code == 404
    assert response.data == b'User does not exist'

    response = testClient.post('/usersapi/deleteUserResearcher', json={'userID': participantID},
                               headers={"Authorization": "Bearer " + access_token})
    assert response.status_code == 200
    assert response.data == b'Account deleted!'

    response = testClient.post('/usersapi/deleteUserResearcher', json={'userID': unrelatedParticipantID},
                               headers={"Authorization": "Bearer " + access_token})
    assert response.status_code == 403
    assert response.data == b'Participant is not created by this researcher'


def testDeleteSelf(testClient, initDatabase):
    '''
        Test if we can remove a user from the database using the deleteUserSelf api call while logged in as the user
        to be deleted.
        We also check if we receive the correct response when the deletion is successful.
        Attributes:
            user: the user to be deleted
            access_token: the access token
            response: the response of the api call
        Arguments:
            testClient:  The test client we test this for.
            initDatabase: the database instance we test this for.
    '''
    del initDatabase
    try:
        db.session.commit()
    except:
        db.session.rollback()
        assert False
    try:
        user = User(username='Bob', password_plaintext='pass')
        db.session.add(user)
        db.session.commit()
    except:
        db.session.rollback()
        assert False

    access_token = loginHelper(testClient, 'Bob', 'pass')

    response = testClient.post('/usersapi/deleteUserSelf',
                               headers={"Authorization": "Bearer " + access_token})
    assert response.status_code == 200
    assert response.data == b'Account deleted!'
