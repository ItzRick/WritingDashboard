from app.models import Files, User, Projects, ParticipantToProject
from app import db
from datetime import datetime
from werkzeug.utils import secure_filename
import json

from test_set_role import loginHelper

def testRetrieveFilesOtherNoAdmin(testClient, initDatabase):
    '''
        This test checks the retrieval of files from another user when the current_user is not
        an admin or researcher
        Arguments:
            testClient:  The test client we test this for.
            initDatabase: the database instance we test this for. 
        Atributes:
            userId: the user for which the files are retrieved
            sortingAttribute: the specified order of the retrieved files
            access_token: access token
            data: data to be sent to the api
            response: the result fo retrieving the files in the specified order
    '''
    del initDatabase
    # We define the user and sorting order
    userId = User.query.filter_by(username='ad').first().id
    sortingAttribute = 'course.asc'

    # get access token for the regular user
    access_token = loginHelper(testClient, 'Pietje', 'Bell')

    data = {
        'userId': userId,
        'sortingAttribute': sortingAttribute,
    }
        
    # Retrieve the files from the specified user
    response = testClient.get('/fileapi/fileretrieve', query_string=data, headers={"Authorization": "Bearer " + access_token})

    # Check if we get the correct status_code and message:
    assert response.status_code == 403
    assert response.data == b'You must be researcher or admin, or retrieve your own data'

def testRetrieveFilesOtherNoPartOf(testClient, initDatabase):
    '''
        This test checks the retrieval of files from another user that is not a participant of the current_user
        Arguments:
            testClient:  The test client we test this for.
            initDatabase: the database instance we test this for. 
        Atributes:
            userId: the user for which the files are retrieved
            sortingAttribute: the specified order of the retrieved files
            access_token: access token
            data: data to be sent to the api
            response: the result fo retrieving the files in the specified order
    '''
    del initDatabase
    # We define the user and sorting order
    userId = User.query.filter_by(username='Pietje').first().id
    sortingAttribute = 'course.asc'

    # get access token for the regular user
    access_token = loginHelper(testClient, 'ad', 'min')

    data = {
        'userId': userId,
        'sortingAttribute': sortingAttribute,
    }
        
    # Retrieve the files from the specified user
    response = testClient.get('/fileapi/fileretrieve', query_string=data, headers={"Authorization": "Bearer " + access_token})

    # Check if we get the correct status_code and message:
    assert response.status_code == 403
    assert response.data == b'You can only retrieve data from your participants or yourself'

def testRetrieveFilesOfPart(testClient, initDatabase):
    '''
        This test checks the retrieval of files from another user that IS a participant of the current_user
        Arguments:
            testClient:  The test client we test this for.
            initDatabase: the database instance we test this for. 
        Atributes:
            file, file2, file1, file3, file4: File to be added to the database.
            userId: the user for which the files are retrieved
            sortingAttribute: the specified order of the retrieved files
            proj: project of ad
            ptp: ParticipantToProject instance related to proj and user Pietje
            access_token: access token
            data: data to be sent to the api
            response: the result fo retrieving the files in the specified order
    '''
    del initDatabase
    # We define the user and sorting order
    userId = User.query.filter_by(username='Pietje').first().id
    sortingAttribute = 'course.asc'

    adId = User.query.filter_by(username='ad').first().id

    # We add five files to the database session for Pietje
    file = Files(path='C:/normal/path/File-1.pdf', filename='File-1.pdf', fileType='.pdf', date=datetime(2019, 2, 12), userId = userId, courseCode = '2IPE0', id=101)
    db.session.add(file)
    file2 = Files(path='C:/normal/path/File-2.pdf', filename='File-2.pdf', fileType='.pdf', date=datetime(2019, 3, 4), userId = 201, courseCode = '2IPE0', id=102)
    db.session.add(file2)
    file1 = Files(path='C:/normal/path/File-3.pdf', filename='File-3.pdf', fileType='.pdf', date=datetime(1999, 2, 12), userId = userId, courseCode = '2IPE0', id=103)
    db.session.add(file1)
    file3 = Files(path='C:/normal/path/File-4.pdf', filename='File-4.pdf', fileType='.pdf', date=datetime(2020, 5, 6), userId = userId, courseCode = '2INC0', id=104)
    db.session.add(file3)
    file4 = Files(path='C:/normal/path/File-5.pdf', filename='File-5.pdf', fileType='.pdf', date=datetime(1980, 2, 12), userId = userId, courseCode = '1ZV50', id=105)
    db.session.add(file4)

    # add project for ad min
    proj = Projects(userId=adId, projectName='test')
    db.session.add(proj)
    db.session.commit()

    assert proj.id is not None

    # add Pietje to project
    ptp = ParticipantToProject(userId=userId, projectId=proj.id)
    db.session.add(ptp)
    db.session.commit()

    ptp = ParticipantToProject.query.filter_by(userId=userId).first()
    assert ptp is not None
    assert ptp.projectId is not None
    assert Projects.query.filter_by(id=proj.id).first() is not None

    # get access token for the regular user
    access_token = loginHelper(testClient, 'ad', 'min')

    data = {
        'userId': userId,
        'sortingAttribute': sortingAttribute,
    }
        
    # Retrieve the files from the specified user
    response = testClient.get('/fileapi/fileretrieve', query_string=data, headers={"Authorization": "Bearer " + access_token})

    # Check if we get the correct status_code and message:
    assert response.status_code == 200
    # Create the expected response:
    expected_response = [dict(courseCode='1ZV50', 
                        date='12/02/80',
                        fileType='.pdf',
                        path='C:/normal/path/File-5.pdf', 
                        progress=0,
                        userId=userId, 
                        filename='File-5.pdf', 
                        id=105
                        ),
                        dict(courseCode='2INC0', 
                        date='06/05/20',
                        fileType='.pdf',
                        path='C:/normal/path/File-4.pdf', 
                        progress=0,
                        userId=userId, 
                        filename='File-4.pdf', 
                        id=104
                        ),
                        dict(courseCode='2IPE0', 
                        date='12/02/19',
                        fileType='.pdf',
                        path='C:/normal/path/File-1.pdf', 
                        progress=0,
                        userId=userId, 
                        filename='File-1.pdf', 
                        id=101
                        ),
                        dict(courseCode='2IPE0', 
                        date='12/02/99',
                        fileType='.pdf',
                        path='C:/normal/path/File-3.pdf', 
                        progress=0,
                        userId=userId, 
                        filename='File-3.pdf', 
                        id=103
                        )]

    # Check if the expected response is correct:
    assert json.loads(response.data) == expected_response
