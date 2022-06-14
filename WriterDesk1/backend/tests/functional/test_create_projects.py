from app.models import Projects
from app import db


def testAddToDatabase(testClient, initDatabase):
    '''
        Test if we can add a project to the database. We first check if the project does not exist yet.
        After the function has been executed, we check whether the project appears now in the database.
        Attributes:
            testClient: The test client we test this for.
            initDatabase: The database instance we test this for.
        Arguments:
            response: The response of the setProject backend call
            project: Project that is added to the database.
    '''
    del initDatabase
    # Check if the project is not yet in the database:
    assert Projects.query.filter_by(projectName='Project1').first() is None

    # Add the project to the database
    response = testClient.post('/projectapi/setProject', data={'userId': 1, 'projectName': 'Project1'})

    # Check if we get the correct status_code:
    assert response.status_code == 200

    # Check if the project is added to the database:
    project = Projects.query.filter_by(projectName='Project1').first()
    assert project.projectName == 'Project1'
    assert project.userId == 1
