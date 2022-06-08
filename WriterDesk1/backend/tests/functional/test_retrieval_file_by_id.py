from app.models import Files
from app import db
from datetime import datetime
import json


def testRetrieveFileSingle(testClient, initDatabaseEmpty):
    '''
        This test checks the retrieval of of files in a specified order, namely
        course name ascending, of a certain user, here with user id 200, in a json file.
        Attributes: 
            file, file2, file1, file3, file4: File to be added to the database.
        Arguments:
            testClient:  The test client we test this for.
            initDatabase: the database instance we test this for. 
            userId: the user for which the files are retrieved
            sortingAttribute: the specified order of the retrieved files
            response: the result fo retrieving the files in the specified order
            expected_response: the response we expect when we run the function.
    '''
    del initDatabaseEmpty
    # We define the user and sorting order
    fileId = 200
    data = {
        'fileId': fileId,
    }

    # We add five files to the database session
    try:
        db.session.commit()
    except:
        db.session.rollback()
    try:
        file = Files(path='C:/normal/path/File-1.pdf', filename='File-1.pdf', fileType='.pdf',
                     date=datetime(2019, 2, 12), userId=100, courseCode='2IPE0', id=200)
        db.session.add(file)
        db.session.commit()
    except:
        db.session.rollback()

    # Retrieve the files from the specified user
    response = testClient.get('/fileapi/getFileById', query_string=data)

    # Check if we get the correct status_code:
    assert response.status_code == 200
    # Create the expected response:
    expected_response = dict(courseCode='2IPE0',
                             date='12/02/19',
                             filetype='.pdf',
                             path='C:/normal/path/File-1.pdf',
                             userId=100,
                             filename='File-1.pdf',
                             id=200
                             )

    # Check if the expected response is correct:
    assert json.loads(response.data) == expected_response


def testRetrieveFileEmpty(testClient, initDatabaseEmpty):
    del initDatabaseEmpty
    # We define the user and sorting order
    fileId = 200
    data = {
        'fileId': fileId,
    }

    # Retrieve the files from the specified user
    response = testClient.get('/fileapi/getFileById', query_string=data)

    # Check if we get the correct status_code:
    assert response.status_code == 400
    # Create the expected response:
    expected_response = dict(courseCode='2IPE0',
                             date='12/02/19',
                             filetype='.pdf',
                             path='C:/normal/path/File-1.pdf',
                             userId=100,
                             filename='File-1.pdf',
                             id=200
                             )

    # Check if the expected response is correct:
    assert response.data.decode("utf-8") == 'No file found with fileId'


def testRetrieveFileMultiple(testClient, initDatabaseEmpty):
    del initDatabaseEmpty
    # We define the file id
    fileId = 201
    data = {
        'fileId': fileId,
    }

    # We add five files to the database session
    try:
        db.session.commit()
    except:
        db.session.rollback()
    try:
        file1 = Files(path='C:/normal/path/File-1.pdf', filename='File-1.pdf', fileType='.pdf',
                     date=datetime(2019, 2, 12), userId=100, courseCode='2IPE0', id=200)
        db.session.add(file1)
        file2 = Files(path='C:/normal/path/File-2.pdf', filename='File-2.pdf', fileType='.pdf',
                     date=datetime(2019, 8, 12), userId=100, courseCode='2IPE0', id=201)
        db.session.add(file2)
        db.session.commit()
    except:
        db.session.rollback()

    # Retrieve the files from the specified user
    response = testClient.get('/fileapi/getFileById', query_string=data)

    # Check if we get the correct status_code:
    assert response.status_code == 200
    # Create the expected response:
    expected_response = dict(courseCode='2IPE0',
                             date='12/08/19',
                             filetype='.pdf',
                             path='C:/normal/path/File-2.pdf',
                             userId=100,
                             filename='File-2.pdf',
                             id=201
                             )

    # Check if the expected response is correct:
    assert json.loads(response.data) == expected_response