from distutils.command.upload import upload
from app.models import Files
from app.database import uploadToDatabase, getFilesByUser, removeFromDatabase
from app import db
from datetime import datetime, date
import os
from werkzeug.utils import secure_filename
from test_set_role import loginHelper


def testRemoveFromDatabase(testClient, initDatabase):
    '''
        Test if we can remove a file from the database using the removeFromDatabase method. We first add a file to the database and then delete it. 
        After we have removed this file, we check that we can indeed not query on this file. 
        Attributes:
            file: File we create to add and remove in the database.
            access_token: the access token
        Arguments:
            testClient:  The test client we test this for.
            initDatabase: the database instance we test this for. 
    '''
    del testClient, initDatabase
    # Create the file instance to be added:
    file = Files(path='C:/Users/20192435/Downloads/SEP2021/WriterDesk1/backend/saved_documents/ScrumAndXpFromTheTrenchesonline07-31.pdf', 
    filename='ScrumAndXpFromTheTrenchesonline07-31.pdf', date=datetime(2019, 2, 12), userId = 123, courseCode = '2IPE0', fileType = '.pdf')
    # Add the file to the database:
    db.session.add(file)
    db.session.commit()
    # See if we can retrieve this file instance with the correct attributes:
    file = Files.query.filter_by(filename='ScrumAndXpFromTheTrenchesonline07-31.pdf').first()
    assert file.filename =='ScrumAndXpFromTheTrenchesonline07-31.pdf'
    assert file.path =='C:/Users/20192435/Downloads/SEP2021/WriterDesk1/backend/saved_documents/ScrumAndXpFromTheTrenchesonline07-31.pdf'
    assert file.date == datetime(2019, 2, 12)
    assert file.userId == 123
    assert file.courseCode == "2IPE0"
    assert file.fileType == '.pdf'
    # Remove this file instance from the database:
    removeFromDatabase(file)
    # Check if we can indeed not retrieve this file anymore:
    assert Files.query.filter_by(filename='ScrumAndXpFromTheTrenchesonline07-31.pdf').first() == None

def testRouteRemoveFileFromDatabase(testClient, initDatabaseEmpty):
    '''
        A general method to test when we uploaded a file to the correct location with the correct information, 
        that we can remove the file from the database as well. 
        Note: The first part of this test case is from the test generalTestStuff in test_upload_1 which 
              is about uploading a file to the correct location with the correct information. 
        Attributes: 
            BASEDIR: Location of the conftest.py file.
            fileDir: Location of the file we are testing the upload of.
            data: The data we are trying to test the upload with.
            response: Response of the post request.
        Arguments:
            testClient:  The test client we test this for.
            fileName: fileName of the file to be deleted (which needs to be put in the correct location, so in the same folder as the conftest.py file).
            userId: userId of the user for which to test to delete the current file.
            courseCode: courseCode of the course for which we test to delete the current file.
            date1: date of the file which we are currently testing to delete.

    '''
    del initDatabaseEmpty
    ### This part is already from test case test_upload_1 
    # Define variables
    fileName='SEP_1.pdf'
    date1=date(2019, 2, 12)
    userId = 123
    courseCode = '2IPE0'
    id1 = 1

    # Get the BASEDIR and set the fileDir with that:
    BASEDIR = os.path.abspath(os.path.dirname(__file__))
    fileDir = os.path.join(BASEDIR, 'testFiles', fileName)
    # Create the data packet:
    data = {
        'files': (open(fileDir, 'rb'), fileName),
        'id': id1,
        'fileName': fileName,
        'courseCode': courseCode,
        'userId': userId,
        'date': date1
    }

    # Create the response by means of the post request:
    access_token = loginHelper(testClient, 'ad', 'min')
    testClient.post('/fileapi/upload', data=data,
                    headers={"Authorization": "Bearer " + access_token})

    # See if the correct data has been added to the database which we retrieve by the filename:
    file = Files.query.filter_by(filename=secure_filename(fileName)).first()
    assert file.filename == fileName
    ###

    # Define a string with the id to use in response2
    data1 = {
        'id': id1,
    }

    # Delete the file
    testClient.delete('/fileapi/filedelete', data=data1,
                        headers={"Authorization": "Bearer " + access_token})

    # Check if the file has been deleted of the disk
    assert not os.path.exists(file.path)
    # See if we also cannot retrieve the file by querying the userId
    # i.e. whether the file does not exists on the database
    assert Files.query.filter_by(filename= secure_filename(fileName)).first() not in Files.query.filter_by(userId=userId).all()

def testRouteRemoveFileFromDatabaseMultiple(testClient, initDatabaseEmpty):
    '''
        A general method to test when we uploaded a file to the correct location with the correct information, 
        that we can remove the file from the database as well. 
        Note: The first part of this test case is from the test generalTestStuff in test_upload_1 which 
              is about uploading a file to the correct location with the correct information. 
        Attributes: 
            BASEDIR: Location of the conftest.py file.
            fileDir: Location of the file we are testing the upload of.
            data: The data we are trying to test the upload with.
            response: Response of the post request.
        Arguments:
            testClient:  The test client we test this for.
            fileName: fileName of the file to be deleted (which needs to be put in the correct location, so in the same folder as the conftest.py file).
            userId: userId of the user for which to test to delete the current file.
            courseCode: courseCode of the course for which we test to delete the current file.
            date1: date of the file which we are currently testing to delete.

    '''
    del initDatabaseEmpty
    ### This part is already from test case test_upload_1 
    # Define variables
    fileName1='test.docx'
    date1=date(2019, 2, 12)
    userId = 123
    courseCode = '2IPE0'
    id1 = 1

    # Get the BASEDIR and set the fileDir with that:
    BASEDIR = os.path.abspath(os.path.dirname(__file__))
    fileDir = os.path.join(BASEDIR, 'testFiles', fileName1)
    # Create the data packet:
    data = {
        'files': (open(fileDir, 'rb'), fileName1),
        'id': id1,
        'fileName': fileName1,
        'courseCode': courseCode,
        'userId': userId,
        'date': date1
    }

    # Create the response by means of the post request:
    access_token = loginHelper(testClient, 'ad', 'min')
    testClient.post('/fileapi/upload', data=data,
                    headers={"Authorization": "Bearer " + access_token})

    # See if the correct data has been added to the database which we retrieve by the filename:
    file1 = Files.query.filter_by(filename=secure_filename(fileName1)).first()
    assert file1.filename == fileName1

    fileName2='SEP_1.pdf'
    date1=date(2019, 2, 12)
    userId = 123
    courseCode = '2IPE0'
    id2 = 2

    # Get the BASEDIR and set the fileDir with that:
    BASEDIR = os.path.abspath(os.path.dirname(__file__))
    fileDir = os.path.join(BASEDIR, 'testFiles', fileName2)
    # Create the data packet:
    data = {
        'files': (open(fileDir, 'rb'), fileName2),
        'id': id2,
        'fileName': fileName2,
        'courseCode': courseCode,
        'userId': userId,
        'date': date1
    }

    # Create the response by means of the post request:
    testClient.post('/fileapi/upload', data=data,
                    headers={"Authorization": "Bearer " + access_token})

    # See if the correct data has been added to the database which we retrieve by the filename:
    file2 = Files.query.filter_by(filename=secure_filename(fileName2)).first()
    assert file2.filename == fileName2
    ###

    # Define a string with the id to use in response2
    data1 = {
        'id': [id1, id2],
    }

    # Delete the file
    testClient.delete('/fileapi/filedelete', data=data1,
                        headers={"Authorization": "Bearer " + access_token})

    # Check if the file has been deleted of the disk
    assert not os.path.exists(file1.path)
    assert not os.path.exists(file2.path)
    # See if we also cannot retrieve the file by querying the userId
    # i.e. whether the file does not exists on the database
    assert Files.query.filter_by(filename= secure_filename(fileName1)).first() not in Files.query.filter_by(userId=userId).all()
    assert Files.query.filter_by(filename= secure_filename(fileName2)).first() not in Files.query.filter_by(userId=userId).all()

def testRouteRemoveNonexistingFileFromDatabase(testClient, initDatabaseEmpty):
    '''
        A general method to test when didn't upload a file to the database but do request the file to be deleted, 
        that the system gives a message. 
        Attributes: 
            BASEDIR: Location of the conftest.py file.
            fileDir: Location of the file we are testing the upload of.
            data: The data we are trying to test the upload with.
            response: Response of the post request.
        Arguments:
            testClient:  The test client we test this for.
            fileName: fileName of the file to be deleted (which needs to be put in the correct location, so in the same folder as the conftest.py file).
            userId: userId of the user for which to test to delete the current file.
            courseCode: courseCode of the course for which we test to delete the current file.
            date1: date of the file which we are currently testing to delete.

    '''
    del initDatabaseEmpty

    # Define variables
    fileName='SEP_1.pdf'
    userId = 123
    id1 = 1

    # Define a string with the id to use in response2
    data1 = {
        'id': id1,
    }

    # See if we cannot retrieve the file by querying the userId
    # i.e. whether the file does not exists on the database
    assert Files.query.filter_by(filename= secure_filename(fileName)).first() not in Files.query.filter_by(userId=userId).all()

    # Delete the file
    access_token = loginHelper(testClient, 'ad', 'min')
    response2 = testClient.delete('/fileapi/filedelete', data=data1,
                                    headers={"Authorization": "Bearer " + access_token})

    # Check that the correct error message is given 
    assert response2.status_code == 404
