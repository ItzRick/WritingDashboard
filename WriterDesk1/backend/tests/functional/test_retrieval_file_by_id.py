from app.models import Files
from app import db
from datetime import datetime
import json


def testRetrieveFileSingle(testClient, initDatabaseEmpty):
    '''
    This test checks the retrieval of a file when there is one file in the database.
    Attributes:
        testClient: The test client we test this for.
        initDatabaseEmpty: The database instance we test this for.
    Arguments:
        data: Data for the getFileById function containing fileId.
        file: File that is uploaded to the database.
        response: Response of the getFileById function.
        expected_response: The response we expect when running the getFileById function.
    '''
    del initDatabaseEmpty
    data = {'fileId': 200}  # Define file id

    # Add file to the database
    try:
        file = Files(path='C:/normal/path/File-1.pdf', filename='File-1.pdf', fileType='.pdf',
                     date=datetime(2019, 2, 12), userId=100, courseCode='2IPE0', id=200)
        db.session.add(file)
        db.session.commit()
    except:
        db.session.rollback()

    # Retrieve the file with the given file id
    response = testClient.get('/fileapi/getFileById', query_string=data)

    # Check if we get the correct status_code:
    assert response.status_code == 200
    # Create the expected response:
    expected_response = dict(courseCode='2IPE0', date='12/02/19', filetype='.pdf', path='C:/normal/path/File-1.pdf',
                             userId=100, filename='File-1.pdf', id=200)

    # Check if the expected response is correct:
    assert json.loads(response.data) == expected_response


def testRetrieveFileEmpty(testClient, initDatabaseEmpty):
    '''
    This test checks the retrieval of an empty database.
    Attributes:
        testClient: The test client we test this for.
        initDatabaseEmpty: The database instance we test this for.
    Arguments:
        data: Data for the getFileById function containing fileId.
        response: Response of the getFileById function.
        expected_response: The response we expect when we run the function.
    '''
    del initDatabaseEmpty
    data = {'fileId': 200}  # Define file id

    # Retrieve the file with the given file id
    response = testClient.get('/fileapi/getFileById', query_string=data)

    # Check if we get the correct status_code:
    assert response.status_code == 400
    # Create the expected response:
    expected_response = 'No file found with fileId'

    # Check if the expected response is correct:
    assert response.data.decode("utf-8") == expected_response


def testRetrieveFileMultiple(testClient, initDatabaseEmpty):
    '''
    This test checks the retrieval of a file when there are multiple files in the database.
    Attributes:
        testClient: The test client we test this for.
        initDatabaseEmpty: The database instance we test this for.
    Arguments:
        data: Data for the getFileById function containing fileId.
        file1, file2: Files that are uploaded to the database.
        response: Response of the getFileById function.
        expected_response: The response we expect when we run the function.
    '''
    del initDatabaseEmpty
    data = {'fileId': 201}  # Define file id

    # Add two files to the database
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

    # Retrieve the file with the given file id
    response = testClient.get('/fileapi/getFileById', query_string=data)

    # Check if we get the correct status_code:
    assert response.status_code == 200
    # Create the expected response:
    expected_response = dict(courseCode='2IPE0', date='12/08/19', filetype='.pdf', path='C:/normal/path/File-2.pdf',
                             userId=100, filename='File-2.pdf', id=201)

    # Check if the expected response is correct:
    assert json.loads(response.data) == expected_response


def testRetrieveFileNonExistent(testClient, initDatabaseEmpty):
    '''
    This test checks the retrieval of a file when the fileId does not exist in the database.
    Attributes:
        testClient: The test client we test this for.
        initDatabaseEmpty: The database instance we test this for.
    Arguments:
        data: Data for the getFileById function containing fileId.
        file1, file2: Files that are uploaded to the database.
        response: Response of the getFileById function.
        expected_response: The response we expect when we run the function.
    '''
    del initDatabaseEmpty
    data = {'fileId': 202}  # Define file id

    # Add two files to the database
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

    # Retrieve the file with the given file id
    response = testClient.get('/fileapi/getFileById', query_string=data)

    # Check if we get the correct status_code:
    assert response.status_code == 400
    # Create the expected response:
    expected_response = 'No file found with fileId'

    # Check if the expected response is correct:
    assert response.data.decode("utf-8") == expected_response


def testRetrieveFileDocx(testClient, initDatabaseEmpty):
    '''
    This test checks the retrieval of a docx file.
    Attributes:
        testClient: The test client we test this for.
        initDatabaseEmpty: The database instance we test this for.
    Arguments:
        data: Data for the getFileById function containing fileId.
        file: File that is uploaded to the database.
        response: Response of the getFileById function.
        expected_response: The response we expect when we run the function.
    '''
    del initDatabaseEmpty
    data = {'fileId': 200}  # Define file id

    # Add docx file to the database
    try:
        file = Files(path='C:/normal/path/File-1.docx', filename='File-1.docx', fileType='.docx',
                      date=datetime(2018, 12, 5), userId=100, courseCode='2ABC1', id=200)
        db.session.add(file)
        db.session.commit()
    except:
        db.session.rollback()

    # Retrieve the file with the given file id
    response = testClient.get('/fileapi/getFileById', query_string=data)

    # Check if we get the correct status_code:
    assert response.status_code == 200
    # Create the expected response:
    expected_response = dict(courseCode='2ABC1', date='05/12/18', filetype='.docx', path='C:/normal/path/File-1.docx',
                             userId=100, filename='File-1.docx', id=200)

    # Check if the expected response is correct:
    assert json.loads(response.data) == expected_response


def testRetrieveFileTxt(testClient, initDatabaseEmpty):
    '''
    This test checks the retrieval of a txt file.
    Attributes:
        testClient: The test client we test this for.
        initDatabaseEmpty: The database instance we test this for.
    Arguments:
        data: Data for the getFileById function containing fileId.
        file: File that is uploaded to the database.
        response: Response of the getFileById function.
        expected_response: The response we expect when we run the function.
    '''
    del initDatabaseEmpty
    data = {'fileId': 200}  # Define file id

    # Add txt file to the database
    try:
        file = Files(path='C:/normal/path/File-1.txt', filename='File-1.txt', fileType='.txt',
                      date=datetime(2014, 1, 1), userId=100, courseCode='2JRV11', id=200)
        db.session.add(file)
        db.session.commit()
    except:
        db.session.rollback()

    # Retrieve the file with the given file id
    response = testClient.get('/fileapi/getFileById', query_string=data)

    # Check if we get the correct status_code:
    assert response.status_code == 200
    # Create the expected response:
    expected_response = dict(courseCode='2JRV11', date='01/01/14', filetype='.txt', path='C:/normal/path/File-1.txt',
                             userId=100, filename='File-1.txt', id=200)

    # Check if the expected response is correct:
    assert json.loads(response.data) == expected_response
