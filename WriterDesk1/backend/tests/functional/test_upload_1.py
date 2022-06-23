import io
import os
from datetime import date, datetime
from app.models import Files
from werkzeug.utils import secure_filename

def generalTestStuff(testClient, fileName, userId, courseCode, date1, filetype):
    '''
        A general method to test if we can upload a file to the correct location and if we can then see that this has been added to the 
        disk in the correct location and if we can find the correct files, so the fileName, userId, courseCode and path in the datbase.
        Attributes: 
            BASEDIR: Location of the conftest.py file.
            fileDir: Location of the file we are testing the upload of.
            data: The data we are trying to test the upload with.
            response: Response of the post request.
        Arguments:
            testClient:  The test client we test this for.
            fileName: fileName of the file to be uploaded (which needs to be put in the correct location, so in the same folder as the conftest.py file).
            userId: userId of the user for which to test to upload the current file.
            courseCode: courseCode of the course for which we test to upload the current file.
            date1: date of the file which we are currently testing to upload.

    '''
    # Get the BASEDIR and set the fileDir with that:
    BASEDIR = os.path.abspath(os.path.dirname(__file__))
    fileDir = os.path.join(BASEDIR, fileName)
    # Create the data packet:
    data = {
        'files': (open(fileDir, 'rb'), fileName),
        'fileName': fileName,
        'courseCode': courseCode,
        'userId': userId,
        'date': date1
    }
    # Create the response by means of the post request:
    response = testClient.post('/fileapi/upload', data=data)
    # See if we indeed get code 200:
    assert response.status_code == 200
    # See if the correct data has been added to the database which we retrieve by the filename:
    file = Files.query.filter_by(filename=secure_filename(fileName)).first()
    # see if we get the correct response message:
    assert response.data == f'Uploaded file with ids: [{file.id}]'.encode('utf-8')
    assert file.filename == secure_filename(fileName)
    assert file.courseCode == courseCode
    assert file.userId == userId
    assert file.date == datetime.combine(date1, datetime.min.time())
    assert file.fileType == filetype
    # Check if the file has indeed been added to the disk:
    assert os.path.exists(file.path)
    # See if we can also retrieve the file by querying by userId:
    assert Files.query.filter_by(filename= secure_filename(fileName)).first() in Files.query.filter_by(userId=userId).all()

def testUploadTextStream(testClient, initDatabase):
    '''
        Test if the fileUpload works for a txt file, with as contents a text stream.
        Attributes:
            data: The data we are trying to test the upload with.
            response: Response of the post request.
            fileName: fileName of the fake txt file.
            userId: userId of the user for which to test to upload the current file.
            courseCode: courseCode of the course for which we test to upload the current file.
            date1: date of the file which we are currently testing to upload.
        Arguments:
            testClient:  The test client we test this for.
            initDatabase: the database instance we test this for. 
    '''
    del initDatabase
    # Create the attributes for the fileName, userId, courseCode and date:
    fileName = 'fake-text-stream.txt'
    userId = 123
    courseCode = '2IPE0'
    date1 = date(2022, 5, 11)
    filetype = '.txt'
    # Create the data packet:
    data = {
        'files': (io.BytesIO(b"some initial text data"), fileName),
        'fileName': 'fake-text-stream.txt',
        'courseCode': courseCode,
        'userId': userId,
        'date': date1
    }
    # Create the response by means of the post request:
    response = testClient.post('/fileapi/upload', data=data)
    # See if we indeed get code 200:
    assert response.status_code == 200
    # See if the correct data has been added to the database which we retrieve by the filename:
    file = Files.query.filter_by(filename=fileName).first()
    # see if we get the correct response message:
    assert response.data == f'Uploaded file with ids: [{file.id}]'.encode('utf-8')
    assert file.filename == fileName
    assert file.courseCode == courseCode
    assert file.userId == userId
    assert file.date == datetime.combine(date1, datetime.min.time())
    assert file.fileType == filetype
    # See if we can also retrieve the file by querying by userId:
    assert Files.query.filter_by(filename= secure_filename(fileName)).first() in Files.query.filter_by(userId=userId).all()
    # Check if the file has indeed been added to the disk:
    assert os.path.isfile(file.path)

def testUploadTextFile(testClient, initDatabase):
    '''
        Test the file upload with a txt file. 
        Attributes:
            fileName: filename of the file for which the upload is tested (in the same location as the conftest.py file).
            userId: userId of the user for which to test to upload the current file.
            courseCode: courseCode of the course for which we test to upload the current file.
            date1: date of the file which we are currently testing to upload.
        Arguments:
            testClient:  The test client we test this for.
            initDatabase: the database instance we test this for.
    '''
    del initDatabase
    fileName = 'test.txt'
    userId = 256
    courseCode = '2WBB0'
    date1 = date(1998, 10, 30)
    filetype = '.txt'
    generalTestStuff(testClient, fileName, userId, courseCode, date1, filetype)

def testUploadTxtMultiple(testClient, initDatabase):
    '''
        Test the file upload with multiple (2) txt files for one user.
        Attributes:
            fileName1: filename of the first file for which the upload is tested (in the same location as the conftest.py file).
            fileName2: filename of the second file for which the upload is tested (in the same location as the conftest.py file).
            userId: userId of the user for which to test to upload the current file.
            courseCode: courseCode of the course for which we test to upload the current file.
            date1: date of the first file which we are currently testing to upload.
            date2: date of the second file which we are currently testing to upload.
        Arguments:
            testClient:  The test client we test this for.
            initDatabase: the database instance we test this for.
    '''
    del initDatabase
    # Upload the first file:
    fileName1 = 'test.txt'
    userId = 256
    courseCode = '2WBB0'
    date1 = date(1998, 10, 30)
    filetype = '.txt'
    generalTestStuff(testClient, fileName1, userId, courseCode, date1, filetype)
    # Upload the second file:
    fileName2 = 'test1.txt'
    date2 = date(2008, 10, 30)
    generalTestStuff(testClient, fileName2, userId, courseCode, date2, filetype)
    
def testUploadTxtAgain(testClient, initDatabase):
    '''
        Test if we can upload a txt file multiple times and if we then update the date.
        Attributes:
            fileName: filename of the file for which the upload and replacing is tested (in the same location as the conftest.py file).
            userId: userId of the user for which to test to upload the current file.
            courseCode: courseCode of the course for which we test to upload the current file.
            date1: date of the file initially, which we are currently testing to upload.
            date2: date of the file if we upload it again, for which we are currently testing to upload.
        Arguments:
            testClient:  The test client we test this for.
            initDatabase: the database instance we test this for.
    '''
    fileName = 'test.txt'
    userId = 256
    courseCode = '2WBB0'
    date1 = date(1998, 10, 30)
    filetype = '.txt'
    generalTestStuff(testClient, fileName, userId, courseCode, date1, filetype)
    date2 = date(2000, 10, 30)
    generalTestStuff(testClient, fileName, userId, courseCode, date2, filetype)

def testUploadPDFFile(testClient, initDatabase):
    '''
        Test the file upload with a pdf file. 
        Attributes:
            fileName: filename of the file for which the upload is tested (in the same location as the conftest.py file).
            userId: userId of the user for which to test to upload the current file.
            courseCode: courseCode of the course for which we test to upload the current file.
            date1: date of the file which we are currently testing to upload.
        Arguments:
            testClient:  The test client we test this for.
            initDatabase: the database instance we test this for.
    '''
    del initDatabase
    fileName = 'SEP Intro.pdf'
    userId = 789
    courseCode = '1ABC2'
    date1 = date(2007, 1, 1)
    filetype = '.pdf'
    generalTestStuff(testClient, fileName, userId, courseCode, date1, filetype)

def testUploadPDFFileExtra(testClient, initDatabase):
    '''
        Test the file upload with another pdf file. 
        Attributes:
            fileName: filename of the file for which the upload is tested (in the same location as the conftest.py file).
            userId: userId of the user for which to test to upload the current file.
            courseCode: courseCode of the course for which we test to upload the current file.
            date1: date of the file which we are currently testing to upload.
        Arguments:
            testClient:  The test client we test this for.
            initDatabase: the database instance we test this for.
    '''
    fileName = 'Air_Pollution_Sources_Identification_Precisely_Based_on_Remotely_Sensed_Aerosol_and_Glowworm_Swarm_Optimization.pdf'
    userId = 564527
    courseCode = '5ABCBDHEH8'
    date1 = date(2005, 2, 27)
    filetype = '.pdf'
    generalTestStuff(testClient, fileName, userId, courseCode, date1, filetype)

def testUploadPDFMultiple(testClient, initDatabase):
    '''
        Test the file upload with multiple (2) pdf files for one user.
        Attributes:
            fileName1: filename of the first file for which the upload is tested (in the same location as the conftest.py file).
            fileName2: filename of the second file for which the upload is tested (in the same location as the conftest.py file).
            userId: userId of the user for which to test to upload the current file.
            courseCode: courseCode of the course for which we test to upload the current file.
            date1: date of the first file which we are currently testing to upload.
            date2: date of the second file which we are currently testing to upload.
        Arguments:
            testClient:  The test client we test this for.
            initDatabase: the database instance we test this for.
    '''
    del initDatabase
    # Upload the first file:
    fileName1 = 'SEP Intro.pdf'
    userId = 789
    courseCode = '1ABC2'
    date1 = date(2007, 1, 1)
    filetype = '.pdf'
    generalTestStuff(testClient, fileName1, userId, courseCode, date1, filetype)
    # Upload the second file:
    fileName2 = 'SEP_1.pdf'
    date2 = date(2008, 2, 1)
    filetype = '.pdf'
    generalTestStuff(testClient, fileName2, userId, courseCode, date2, filetype)

def testUploadPDFAgain(testClient, initDatabase):
    '''
        Test if we can upload a pdf file multiple times and if we then update the date.
        Attributes:
            fileName: filename of the file for which the upload and replacing is tested (in the same location as the conftest.py file).
            userId: userId of the user for which to test to upload the current file.
            courseCode: courseCode of the course for which we test to upload the current file.
            date1: date of the file initially, which we are currently testing to upload.
            date2: date of the file if we upload it again, for which we are currently testing to upload.
        Arguments:
            testClient:  The test client we test this for.
            initDatabase: the database instance we test this for.
    '''
    # Upload the file the first time:
    fileName = 'SEP Intro.pdf'
    userId = 789
    courseCode = '1ABC2'
    date1 = date(2007, 1, 1)
    filetype = '.pdf'
    generalTestStuff(testClient, fileName, userId, courseCode, date1, filetype)
    # Upload the file again with updated date:
    date2 = date(2008, 2, 1)
    generalTestStuff(testClient, fileName, userId, courseCode, date2, filetype)

def testUploadDOCXFile(testClient, initDatabase):
    '''
        Test the file upload with a docx file. 
        Attributes:
            fileName: filename of the file for which the upload is tested (in the same location as the conftest.py file).
            userId: userId of the user for which to test to upload the current file.
            courseCode: courseCode of the course for which we test to upload the current file.
            date1: date of the file which we are currently testing to upload.
        Arguments:
            testClient:  The test client we test this for.
            initDatabase: the database instance we test this for.
    '''
    del initDatabase
    fileName = 'test.docx'
    userId = 78267
    courseCode = '9ABCEHJDHD20'
    date1 = date(2016, 11, 8)
    filetype = '.docx'
    generalTestStuff(testClient, fileName, userId, courseCode, date1, filetype)

def testUploadDOCXFileMultiple(testClient, initDatabase):
    '''
        Test the file upload with multiple (2) docx files for one user.
        Attributes:
            fileName1: filename of the first file for which the upload is tested (in the same location as the conftest.py file).
            fileName2: filename of the second file for which the upload is tested (in the same location as the conftest.py file).
            userId: userId of the user for which to test to upload the current file.
            courseCode: courseCode of the course for which we test to upload the current file.
            date1: date of the first file which we are currently testing to upload.
            date2: date of the second file which we are currently testing to upload.
        Arguments:
            testClient:  The test client we test this for.
            initDatabase: the database instance we test this for.
    '''
    # Upload the first file:
    fileName1 = 'test.docx'
    userId = 78267
    courseCode = '9ABCEHJDHD20'
    date1 = date(2016, 11, 8)
    filetype = '.docx'
    generalTestStuff(testClient, fileName1, userId, courseCode, date1, filetype)
    # Upload the second file:
    fileName2 = 'test_1.docx'
    date2 = date(2018, 11, 8)
    generalTestStuff(testClient, fileName2, userId, courseCode, date2, filetype)

def testUploadDOCXFileAgain(testClient, initDatabase):
    '''
        Test if we can upload a docx file multiple times and if we then update the date.
        Attributes:
            fileName: filename of the file for which the upload and replacing is tested (in the same location as the conftest.py file).
            userId: userId of the user for which to test to upload the current file.
            courseCode: courseCode of the course for which we test to upload the current file.
            date1: date of the file initially, which we are currently testing to upload.
            date2: date of the file if we upload it again, for which we are currently testing to upload.
        Arguments:
            testClient:  The test client we test this for.
            initDatabase: the database instance we test this for.
    '''
    del initDatabase
    # Upload the file for the first time:
    fileName = 'test.docx'
    userId = 78267
    courseCode = '9ABCEHJDHD20'
    date1 = date(2016, 11, 8)
    filetype = '.docx'
    generalTestStuff(testClient, fileName, userId, courseCode, date1, filetype)
    # Update the file by uploading the file again:
    date2 = date(2018, 11, 8)
    generalTestStuff(testClient, fileName, userId, courseCode, date2, filetype)






