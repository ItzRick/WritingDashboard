from distutils.command.upload import upload
from app.models import Files
from app.database import uploadToDatabase, getFilesByUser, removeFromDatabase
from app import db
from datetime import datetime, date
import os
from werkzeug.utils import secure_filename
import io
from test_set_role import loginHelper

def testRetrieveListOfIds(testClient, initDatabaseEmpty):
    '''
        A general method to test whether the application can retrieve a list of ids 
        from the application, after having uploaded one file.
        Attributes:
            testClient: the new instance of the flask application
            initDatabaseEmpty: empty instance of the database, to which the files can be uploaded.
            data: The data we are trying to test the upload with.
            response: Response of the post request.
            fileName: fileName of the fake txt file.
            userId: userId of the user for which to test to upload the current file.
            courseCode: courseCode of the course for which we test to upload the current file.
            date1: date of the file which we are currently testing to upload.
            id1: id of the file we are testing the method with.
            access_token: the access token
        Argument:
            response: the result by retrieving the list of file ids
    '''
    del initDatabaseEmpty
    # Create the file with which this method will be tested:
    fileName = 'fake-text-stream.txt'
    userId = 123
    courseCode = '2IPE0'
    date1 = date(2022, 5, 11)
    id1 = 1
    # Create the data packet:
    data = {
        'files': (io.BytesIO(b"some initial text data"), fileName),
        'fileName': 'fake-text-stream.txt',
        'courseCode': courseCode,
        'userId': userId,
        'date': date1,
        'id': id1
    }
    # Upload this file:
    access_token = loginHelper(testClient, 'ad', 'min')
    testClient.post('/fileapi/upload', data=data,
                    headers={"Authorization": "Bearer " + access_token})

    # Create the response by means of the get request:
    response = testClient.get('/fileapi/searchId') 
    # Check whether the expected result is the same as the received result. 
    assert response.status_code == 200
    assert response.data == f'{id1} '.encode('utf-8') 

def testRetrieveListOfIdsMultiple(testClient, initDatabaseEmpty):
    '''
        A general method to test whether the application can retrieve a list of ids 
        from the application, after having uploaded two files.
        Attributes:
            testClient: the new instance of the flask application.
            initDatabase: empty instance of the database, to which the files can be uploaded.
            data: The data we are trying to test the upload with.
            response: Response of the post request.
            fileName: fileName of the fake txt file.
            userId: userId of the user for which to test to upload the current file.
            courseCode: courseCode of the course for which we test to upload the current file.
            date1: date of the file which we are currently testing to upload.
            id1: id of the first file we are testing the method with.
            id2: id of the second file we are testing the method with. 
            access_token: the access token
        Argument:
            response: the result by retrieving the list of file ids
    '''
    del initDatabaseEmpty
    # Upload the first file:
    fileName = 'fake-text-stream.txt'
    userId = 123
    courseCode = '2IPE0'
    date1 = date(2022, 5, 11)
    id1 = 1
    # Create the data packet:
    data = {
        'files': (io.BytesIO(b"some initial text data"), fileName),
        'fileName': 'fake-text-stream.txt',
        'courseCode': courseCode,
        'userId': userId,
        'date': date1,
        'id': id1
    }
    # Upload the file by means of a post request:
    access_token = loginHelper(testClient, 'ad', 'min')
    testClient.post('/fileapi/upload', data=data,
                    headers={"Authorization": "Bearer " + access_token})
    # Upload the second file:
    fileName = 'fake-text-stream1.txt'
    id2 = 2
    data = {
        'files': (io.BytesIO(b"some initial text data"), fileName),
        'fileName': 'fake-text-stream.txt',
        'courseCode': courseCode,
        'userId': userId,
        'date': date1,
        'id': id2
    }
    # Upload the file by means of a post request:
    testClient.post('/fileapi/upload', data=data,
                    headers={"Authorization": "Bearer " + access_token})
    
    # Create the response by means of the get request:
    response = testClient.get('/fileapi/searchId') 
    # Check whether the expected result is the same as the received result. 
    assert response.status_code == 200
    assert response.data == f'{id1} {id2} '.encode('utf-8') 

def testRetrieveEmptyListOfIds(testClient, initDatabaseEmpty):
    '''
        A general method to test whether the application can retrieve a list of ids 
        from the application, using the database without files.
        Attributes:
            testClient: the new instance of the flask application
            initDatabaseEmpty: the new database within the new instance of the flask application, 
                               is empty
        Argument:
            response: the result by retrieving the list of file ids    
    '''
    del initDatabaseEmpty

    # Create the response by means of the get request:
    response = testClient.get('/fileapi/searchId') 
    # Check whether the expected result is the same as the received result. 
    assert response.data == b''

def testRetrieveListOfIdsOneDeleted(testClient, initDatabaseEmpty):
    '''
        A general method to test whether the application can retrieve a list of ids 
        from the application, after having uploaded two files to the database and deleting the first file.
            testClient: the new instance of the flask application
            initDatabaseEmpty: empty instance of the database, to which the files can be uploaded.
            data: The data we are trying to test the upload with.
            response: Response of the post request.
            fileName: fileName of the fake txt file.
            userId: userId of the user for which to test to upload the current file.
            courseCode: courseCode of the course for which we test to upload the current file.
            date1: date of the file which we are currently testing to upload.
            id1: id of the first file we are testing the method with.
            id2: id of the second file we are testing the method with. 
        Argument:
            response1: the result by deleting the first file with file id 1
            response2: the result by retrieving the list of file ids    
    '''
    del initDatabaseEmpty
    # Upload the first file:
    fileName = 'fake-text-stream.txt'
    userId = 123
    courseCode = '2IPE0'
    date1 = date(2022, 5, 11)
    id1 = 1
    # Create the data packet:
    data = {
        'files': (io.BytesIO(b"some initial text data"), fileName),
        'fileName': 'fake-text-stream.txt',
        'courseCode': courseCode,
        'userId': userId,
        'date': date1,
        'id': id1
    }
    # Upload the file by means of a post request:
    access_token = loginHelper(testClient, 'ad', 'min')
    testClient.post('/fileapi/upload', data=data,
                    headers={"Authorization": "Bearer " + access_token})
    fileName = 'fake-text-stream1.txt'
    id2 = 2
    data = {
        'files': (io.BytesIO(b"some initial text data"), fileName),
        'fileName': 'fake-text-stream.txt',
        'courseCode': courseCode,
        'userId': userId,
        'date': date1,
        'id': id2
    }
    # Create the response by means of the post request:
    testClient.post('/fileapi/upload', data=data,
                    headers={"Authorization": "Bearer " + access_token})
    # Remove the file with the first file id:
    data1 = {
        'id': id1,
    }
    testClient.delete('/fileapi/filedelete', data=data1,
                       headers={"Authorization": "Bearer " + access_token})

    # Create the response by means of the get request:
    response = testClient.get('/fileapi/searchId') 
    # Check whether the expected result is the same as the received result. 
    assert response.status_code == 200
    assert response.data == f'{id2} '.encode('utf8')