import os
from datetime import date
import io
from app.models import Files, User
from test_set_role import loginHelper

def testDirsCreated(testClient, initDatabase):
    '''
        Tests of the directory the actual file is put in gets created if this does not yet exist.
        So, test if a subdirectory is created with the name of an userId. This is tested by uploading a txt file 
        consisting of a datastream with some text.
        Attributes:
            data: The data we are trying to test the upload with.
            response: Response of the post request.
            fileName: fileName of the fake txt file.
            userId: userId of the user for which to test to upload the current file.
            courseCode: courseCode of the course for which we test to upload the current file.
            date1: date of the file which we are currently testing to upload.
            access_token: the access token
        Arguments:
            testClient:  The test client we test this for.
            initDatabase: the database instance we test this for. 
    '''
    del initDatabase
    # Create the actual file:
    fileName = 'test.txt'
    userId = User.query.filter_by(username="ad").first().id
    courseCode = '2WBB0'
    date1 = date(1998, 10, 30)
    data = {
        'files': (io.BytesIO(b"some initial text data"), fileName),
        'fileName': fileName,
        'courseCode': courseCode,
        'userId': userId,
        'date': date1
    }
    # Make sure this subdirectory with this user ID does not exist yet: 
    assert not os.path.isdir(os.path.join(testClient.application.config['UPLOAD_FOLDER'], str(userId)))
    # Upload this data:
    access_token = loginHelper(testClient, 'ad', 'min')
    response = testClient.post('/fileapi/upload', data=data,
                                headers={"Authorization": "Bearer " + access_token})
    # Check if this data is indeed correctly uploaded:
    file = Files.query.filter_by(filename=fileName).first()
    assert response.data == f'Uploaded file with ids: [{file.id}]'.encode('utf-8')
    assert response.status_code == 200
    # Check if this subdirectory with the name of the userId does indeed exist now: 
    assert os.path.isdir(testClient.application.config['UPLOAD_FOLDER'])
    assert os.path.isdir((os.path.join(testClient.application.config['UPLOAD_FOLDER'], str(userId))))

def testUploadTextFileIncorrect(testClient, initDatabase):
    '''
        Test if a file of the incorrect format does indeed not get accepted by the server. 
        In this case this is tested with an .xlsx file.
        Attributes:
            BASEDIR: Location of the conftest.py file.
            fileDir: Location of the file we are testing the upload of.
            data: The data we are trying to test the upload with.
            response: Response of the post request.
            access_token: the access token.
            fileName: The filename of the file we test this with.
        Arguments:
            testClient:  The test client we test this for.
            initDatabase: the database instance we test this for. 
    '''
    del initDatabase
    # Get the location and filename of this specific file:
    BASEDIR = os.path.abspath(os.path.dirname(__file__))
    fileName = 'SEP202122Q4.xlsx'
    fileDir = os.path.join(BASEDIR, fileName)
    # Create the data packet:
    data = {
        'files': (open(fileDir, 'rb'), fileName)
    }
    # Create push request:
    access_token = loginHelper(testClient, 'ad', 'min')
    response = testClient.post('/fileapi/upload', data=data,
                                headers={"Authorization": "Bearer " + access_token})
    # Check if the response is indeed of code 400 and has as text 'Incorrect filetype: SEP202122Q4.xlsx':
    assert response.data == f'Incorrect filetype: {fileName}'.encode('utf-8')
    assert response.status_code == 400

def testUploadTextFileCorrupt(testClient, initDatabase):
    '''
        Test if a corrupt file of does indeed not get accepted by the server. 
        In this case this is tested with a corrupt .txt file.
        Attributes:
            BASEDIR: Location of the conftest.py file.
            fileDir: Location of the file we are testing the upload of.
            data: The data we are trying to test the upload with.
            response: Response of the post request.
            access_token: the access token.
            fileName: The filename of the file we test this with.
        Arguments:
            testClient:  The test client we test this for.
            initDatabase: the database instance we test this for. 
    '''
    del initDatabase
    # Get the location and filename of this specific file:
    fileName = 'file_corrupt.txt'
    BASEDIR = os.path.abspath(os.path.dirname(__file__))
    fileDir = os.path.join(BASEDIR, fileName)
    # Create the data packet:
    data = {
        'files': (open(fileDir, 'rb'), fileName)
    }
    # Create push request:
    access_token = loginHelper(testClient, 'ad', 'min')
    response = testClient.post('/fileapi/upload', data=data,
                                headers={"Authorization": "Bearer " + access_token})
    # Check if the response is indeed of code 400 and has as text 'Corrupt file: file_corrupt.txt':
    
    assert response.data == f'Corrupt file: {fileName}'.encode('utf-8')
    assert response.status_code == 400

def testUploadTextFileNoFile(testClient, initDatabase):
    '''
        Test if we indeed get an error if we try to upload files without any file added. 
        Attributes:
            data: The data we are trying to test the upload with.
            response: Response of the post request.
            access_token: the access token
        Arguments:
            testClient:  The test client we test this for.
            initDatabase: the database instance we test this for. 
    '''
    del initDatabase
    # Create this data, with no file attached:
    data = {
        'files': '',
    }
    # Do the Post request and get the response:
    access_token = loginHelper(testClient, 'ad', 'min')
    response = testClient.post('/fileapi/upload', data=data,
                                headers={"Authorization": "Bearer " + access_token})
    # See that we indeed get a code 400 returned and get the correct text retrieved:
    assert response.data == b'No file uploaded'
    assert response.status_code == 400