from app.models import Projects, User, ParticipantToProject, Files
from app.database import uploadToDatabase, removeFromDatabase
from app import db
import os

from datetime import date

from flask import current_app

from test_set_role import loginHelper


def testRemoveFromDatabase(testClient, initDatabase):
    '''
        Test if we can remove a project from the database. We first add a project to the database and then delete it.
        After we have removed this instance, we check that we can indeed not query on this project anymore.
        Arguments:
            testClient: The test client we test this for.
            initDatabase: The database instance we test this for.
        Attributes:
            project: Project we create to add and remove in the database.
            response: The response of the deleteProject backend call
            access_token: Access token for user Pietje Bell
    '''
    del initDatabase
    # Create the project instance to be added:
    project = Projects(userId=1, projectName='Project1')

    # Add the project to the database:
    uploadToDatabase(project)

    # See if we can retrieve this project instance with the correct attributes:
    project = Projects.query.filter_by(projectName='Project1').first()
    assert project.projectName == 'Project1'
    assert project.userId == 1

    # get access token for Pietje Bell
    access_token = loginHelper(testClient, 'Pietje', 'Bell')

    # Delete the project from the database
    response = testClient.delete('/projectapi/deleteProject', data={'projectId': project.id},
                                 headers={"Authorization": "Bearer " + access_token})

    # Check if we get the correct status_code:
    assert response.status_code == 200

    # Check if we can indeed not retrieve this project anymore:
    assert Projects.query.filter_by(projectName='Project1').first() is None


def testRemoveFromDatabaseMultiple(testClient, initDatabase):
    '''
        Test if we can remove multiple projects from the database. We first add the projects to the database and then
        delete it. After we have removed the instances, we check that we can indeed not query these projects anymore.
        Arguments:
            testClient: The test client we test this for.
            initDatabase: The database instance we test this for.
        Attributes:
            project1, project2: Projects we create to add and remove in the database.
            response: The response of the deleteProject backend call
            access_token: Access token for user Pietje Bell
    '''
    del initDatabase
    # Create the project instances to be added:
    project1 = Projects(userId=1, projectName='Project1')
    project2 = Projects(userId=1, projectName='Project2')

    # Add the projects to the database:
    uploadToDatabase(project1)
    uploadToDatabase(project2)

    # See if we can retrieve both projects instance with the correct attributes:
    project1 = Projects.query.filter_by(projectName='Project1').first()
    assert project1.projectName == 'Project1'
    assert project1.userId == 1

    project2 = Projects.query.filter_by(projectName='Project2').first()
    assert project2.projectName == 'Project2'
    assert project2.userId == 1

    # get access token for Pietje Bell
    access_token = loginHelper(testClient, 'Pietje', 'Bell')

    # Delete the projects from the database
    response = testClient.delete('/projectapi/deleteProject', data={'projectId': [project1.id, project2.id]},
                                 headers={"Authorization": "Bearer " + access_token})

    # Check if we get the correct status_code:
    assert response.status_code == 200

    # Check if we can indeed not retrieve the projects anymore:
    assert Projects.query.filter_by(projectName='Project1').first() is None
    assert Projects.query.filter_by(projectName='Project2').first() is None


def testRemoveFromDatabaseInvalidId(testClient, initDatabase):
    '''
        Test if we get a 404 status code response when we try to remove a project from the database with
        a project id that does not belong to the current user.
        Arguments:
            testClient: The test client we test this for.
            initDatabase: The database instance we test this for.
        Attributes:
            project: Project we create to add and remove in the database.
            response: The response of the deleteProject backend call
            access_token: Access token for user Pietje Bell
    '''
    del initDatabase

    # Create the project instance to be added:
    project = Projects(userId=5, projectName='Project1')

    # Add the project to the database:
    uploadToDatabase(project)

    # See if we can retrieve this project instance with the correct attributes:
    project = Projects.query.filter_by(projectName='Project1').first()
    assert project.projectName == 'Project1'
    assert project.userId == 5

    # get access token for Pietje Bell
    access_token = loginHelper(testClient, 'Pietje', 'Bell')

    # Try to delete the project from the database
    response = testClient.delete('/projectapi/deleteProject', data={'projectId': project.id},
                                 headers={"Authorization": "Bearer " + access_token})
    # Check if we get the correct status_code:
    assert response.status_code == 400


def testRemoveFromDatabaseInvalidProject(testClient, initDatabase):
    '''
        Test if we get a 400 status code response when we try to remove a project with a project id
        that does not exist in the database.
        Arguments:
            testClient: The test client we test this for.
            initDatabase: The database instance we test this for.
        Attributes:
            response: The response of the deleteProject backend call
            access_token: Access token for user Pietje Bell
    '''
    del initDatabase

    # See if the project id does not exist in the database:
    assert Projects.query.filter_by(id=1).first() is None

    # get access token for Pietje Bell
    access_token = loginHelper(testClient, 'Pietje', 'Bell')

    # Try to delete the project from the database
    response = testClient.delete('/projectapi/deleteProject', data={'projectId': 1},
                                 headers={"Authorization": "Bearer " + access_token})

    # Check if we get the correct status_code:
    assert response.status_code == 404


def testDeleteFilesFromProject(testClient, initDatabase):
    '''
        Test if the files folder of a participant is removed when the project of the participant is removed.
        Arguments:
            testClient: The test client we test this for.
            initDatabase: The database instance we test this for.
        Attributes:
            response: The response of the deleteProject backend call
            access_token: Access token for user ad min
            adId: ID of the user ad min
            participant: participant that is added to the database
            project: project that is added to the database
            partToProject: ParticipantToProject instance that is added the database
            filepath: Path of the files folder for the participant par_1
    '''
    del initDatabase

    # Get access token for ad min
    access_token = loginHelper(testClient, 'ad', 'min')
    # Get userId for ad min
    adId = User.query.filter_by(username='ad').first().id

    # Create participant in the database
    participant = User(username='par_1', password_plaintext='par_1', role='participant')
    uploadToDatabase(participant)

    # Create the project in the database
    project = Projects(userId=adId, projectName='Project1')
    uploadToDatabase(project)

    # Create the ParticipantToProject instance in the database
    partToProject = ParticipantToProject(userId=participant.id, projectId=project.id)
    uploadToDatabase(partToProject)

    # Path of the folder for the participant
    filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], str(participant.id))

    # Create directory
    os.mkdir(filepath)

    # Check if directory exists
    assert os.path.exists(filepath)

    # Try to delete the project from the database
    response = testClient.delete('/projectapi/deleteProject', data={'projectId': project.id},
                                 headers={"Authorization": "Bearer " + access_token})

    # Check if the everything is removed from the database
    assert Projects.query.filter_by(projectName='Project1').first() is None
    assert User.query.filter_by(username='par_1').first() is None
    assert ParticipantToProject.query.filter_by(projectId=project.id).first() is None

    # Check status code
    assert response.status_code == 200
    assert response.data == b'success'

    # Check if path is removed
    assert not os.path.exists(filepath)
