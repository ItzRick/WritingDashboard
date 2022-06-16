from distutils.command.upload import upload
from app.models import Projects
from app.database import uploadToDatabase, removeFromDatabase
from app import db


def testRemoveFromDatabase(testClient, initDatabase):
    '''
        Test if we can remove a project from the database. We first add a project to the database and then delete it.
        After we have removed this instance, we check that we can indeed not query on this project anymore.
        Attributes:
            testClient: The test client we test this for.
            initDatabase: The database instance we test this for.
        Arguments:
            project: Project we create to add and remove in the database.
            response: The response of the deleteProject backend call
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

    # Delete the project from the database
    response = testClient.delete('/projectapi/deleteProject', data={'projectId': project.id})

    # Check if we get the correct status_code:
    assert response.status_code == 200

    # Check if we can indeed not retrieve this project anymore:
    assert Projects.query.filter_by(projectName='Project1').first() is None


def testRemoveFromDatabaseMultiple(testClient, initDatabase):
    '''
        Test if we can remove multiple projects from the database. We first add the projects to the database and then
        delete it. After we have removed the instances, we check that we can indeed not query these projects anymore.
        Attributes:
            testClient: The test client we test this for.
            initDatabase: The database instance we test this for.
        Arguments:
            project1, project2: Projects we create to add and remove in the database.
            response: The response of the deleteProject backend call
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

    # Delete the projects from the database
    response = testClient.delete('/projectapi/deleteProject', data={'projectId': [project1.id, project2.id]})

    # Check if we get the correct status_code:
    assert response.status_code == 200

    # Check if we can indeed not retrieve the projects anymore:
    assert Projects.query.filter_by(projectName='Project1').first() is None
    assert Projects.query.filter_by(projectName='Project2').first() is None


def testRemoveFromDatabaseInvalidId(testClient, initDatabase):
    '''
        Test if we get a 404 status code response when we try to remove a project from the database with
        a project id that does not exist in the database.
        Attributes:
            testClient: The test client we test this for.
            initDatabase: The database instance we test this for.
        Arguments:
            response: The response of the deleteProject backend call
    '''
    del initDatabase

    # Check if the id does not exist in the database:
    assert Projects.query.filter_by(id=123).first() is None

    # Try to delete the project from the database
    response = testClient.delete('/projectapi/deleteProject', data={'projectId': 123})

    # Check if we get the correct status_code:
    assert response.status_code == 404

