from distutils.command.upload import upload
from app.models import Files
from app.database import uploadToDatabase, getFilesByUser, removeFromDatabase
from app import db
from datetime import datetime, date
import os
from werkzeug.utils import secure_filename

def testRetrieveListOfIds(testClient, initDatabase):
    '''
        A general method to test whether the application can retrieve a list of ids 
        from the application, using the database with two files.
        Attributes:
            testClient: the new instance of the flask application
            initDatabase: the new database within the new instance of the flask application,
                          has two files
        Argument:
            response: the result by retrieving the list of file ids
    '''
    del testClient, initDatabase

    # Create the response by means of the get request:
    response = testClient.get('/fileapi/searchId') 

    print(response)

    # Check whether the expected result is the same as the received result. 
    assert response == "1    2    "

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
    del testClient, initDatabaseEmpty

    # Create the response by means of the get request:
    response = testClient.get('/fileapi/searchId') 

    print(response)

    # Check whether the expected result is the same as the received result. 
    assert response == ""

def testRetrieveListOfIdsOneDeleted(testClient, initDatabase):
    '''
        A general method to test whether the application can retrieve a list of ids 
        from the application, using the database with two files where one is deleted later.
        Attributes:
            testClient: the new instance of the flask application
            initDatabaseEmpty: the new database within the new instance of the flask application, 
                               is empty
        Argument:
            response1: the result by deleting the first file with file id 1
            response2: the result by retrieving the list of file ids    
    '''
    del testClient, initDatabase

    response1 = testClient.delete('/fileapi/filedelete', query_string=1)

    # Create the response by means of the get request:
    response2 = testClient.get('/fileapi/searchId') 

    print(response2)

    # Check whether the expected result is the same as the received result. 
    assert response2 == "2    "