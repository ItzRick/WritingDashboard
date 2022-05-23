from distutils.command.upload import upload
from app.models import Files
from app.database import uploadToDatabase, getFilesByUser, removeFromDatabase
from app import db
from datetime import datetime, date
import os
from werkzeug.utils import secure_filename

def testValidFile(testClient, initDatabase):
    '''
        Test if the files which are added in the database during setup are valid and all attributes
        can be correctly retrieved.
        Attributes:
            files: all files in the datbase of type Files.
            file1: The first file of this type in the database.
            file2: The second file of this type in the database.
        Arguments:
            testClient:  The test client we test this for.
            initDatabase: the database instance we test this for. 
    '''
    del testClient, initDatabase
    # Retrieve the files:
    files = Files.query.all()
    # Test if all attributes for the first file are still currently there:
    file = files[0]
    assert file.filename=='URD_Group3_vers03_Rc.pdf'
    assert file.path=='C:/Users/20192435/Downloads/SEP2021/WriterDesk1/backend/saved_documents/URD_Group3_vers03_Rc.pdf'
    assert file.date == datetime(2019, 2, 12)
    assert file.userId == 123
    assert file.courseCode == "2IPE0"
    # Test if all attributes for the file are still currently there: 
    file = files[1]
    assert file.filename=='SEP.pdf'
    assert file.path=='C:/Users/20192435/Downloads/SEP2021/WriterDesk1/backend/saved_documents/SEP.pdf'
    assert file.date == datetime(2020, 10, 2)
    assert file.userId == 567
    assert file.courseCode == "3NAB0"

def testUploadToDatabase(testClient, initDatabase):
    '''
        Test if the uploadToDatabase function form the database module works. To do this, an instance to be added to the Files table is created
        and it is checked that we can retrieve this file correctly. Furthermore, it is checked that all attributes are still the same.
        Attributes:
            file: File to be added to the database.
            file1: This same file, only then retrieved from the database.
        Arguments:
            testClient:  The test client we test this for.
            initDatabase: the database instance we test this for. 
    '''
    del testClient, initDatabase
    # Create a file instance of Files:
    file = Files(path='C:/Users/20192435/Downloads/SEP2021/WriterDesk1/backend/saved_documents/ScrumAndXpFromTheTrenchesonline07-31.pdf', 
    filename='ScrumAndXpFromTheTrenchesonline07-31.pdf', date=datetime(2019, 2, 12), userId = 123, courseCode = '2IPE0')
    # Call the uploadToDatabase function:
    uploadToDatabase(file)
    # Retrieve this file with query.filter_by and check if all attributes are retrieved correctly:
    file1 = Files.query.filter_by(filename='ScrumAndXpFromTheTrenchesonline07-31.pdf').first()
    assert file1.filename =='ScrumAndXpFromTheTrenchesonline07-31.pdf'
    assert file1.path =='C:/Users/20192435/Downloads/SEP2021/WriterDesk1/backend/saved_documents/ScrumAndXpFromTheTrenchesonline07-31.pdf'
    assert file1.date == datetime(2019, 2, 12)
    assert file1.userId == 123
    assert file1.courseCode == "2IPE0"
    # Check if we can also retrieve this with query.all() and can then retrieve it with the second element, 
    # check if all attributes are retrieved correctly:
    file2 = Files.query.all()[2]
    assert file2.filename=='ScrumAndXpFromTheTrenchesonline07-31.pdf'
    assert file2.path=='C:/Users/20192435/Downloads/SEP2021/WriterDesk1/backend/saved_documents/ScrumAndXpFromTheTrenchesonline07-31.pdf'
    assert file2.date == datetime(2019, 2, 12)
    assert file2.userId == 123
    assert file2.courseCode == "2IPE0"
    
def testGetFilesByUser(testClient, initDatabase):
    '''
        Test if we get the correct display if we run getFilesByUser(200, 'date.asc'), so the representation of '<File <filename>>'. 
        Attributes: 
            file, file2, file3: File to be added to the database.
        Arguments:
            testClient:  The test client we test this for.
    '''
    # This test case also includes testing getting files sorted by date ascending
    del testClient, initDatabase
    # We add three files to the database session
    try:
        db.session.commit()
    except:
        db.session.rollback()
    try: 
        file = Files(path='C:/normal/path/File-1.pdf', filename='File-1.pdf', date=datetime(2019, 2, 12), userId = 200, courseCode = '2IPE0')
        db.session.add(file)
        file2 = Files(path='C:/normal/path/File-2.pdf', filename='File-2.pdf', date=datetime(2019, 2, 12), userId = 201, courseCode = '2IPE0')
        db.session.add(file2)
        file3 = Files(path='C:/normal/path/File-3.pdf', filename='File-3.pdf', date=datetime(1999, 2, 12), userId = 200, courseCode = '2IPE0')
        db.session.add(file3)
        db.session.commit()
    except: 
        db.session.rollback()
    # We retrieve the files of the user with date ascending
    files = getFilesByUser(200, 'date.asc')
    # Check if the number of files is 2,
    # that the first file is the oldest file 
    # and that the userId for that file is correct.
    assert len(files) == 2
    assert files[0].get('filename') == 'File-3.pdf'
    assert files[0].get('userId') == 200

def testGetFilesSortedByFilenameAscending(testClient, initDatabaseEmpty):
    '''
        Test if we get the correct display if we run getFilesByUser(200, 'filename.asc'), so the representation of '<File <filename>>'. 
        Attributes: 
            file, file2, file1, file3, file4: File to be added to the database.
        Arguments:
            testClient:  The test client we test this for.
            initDatabase: the database instance we test this for. 
    '''
    del testClient, initDatabaseEmpty
    # We add five files to the database session
    try:
        db.session.commit()
    except:
        db.session.rollback()
    try: 
        file = Files(path='C:/normal/path/File-1.pdf', filename='File-1.pdf', date=datetime(2019, 2, 12), userId = 200, courseCode = '2IPE0')
        db.session.add(file)
        file2 = Files(path='C:/normal/path/File-2.pdf', filename='File-2.pdf', date=datetime(2019, 3, 4), userId = 201, courseCode = '2IPE0')
        db.session.add(file2)
        file1 = Files(path='C:/normal/path/File-3.pdf', filename='File-1.pdf', date=datetime(1999, 2, 12), userId = 200, courseCode = '2IPE0')
        db.session.add(file1)
        file3 = Files(path='C:/normal/path/File-3.pdf', filename='File-3.pdf', date=datetime(2020, 5, 6), userId = 200, courseCode = '2INC0')
        db.session.add(file3)
        file4 = Files(path='C:/normal/path/File-4.pdf', filename='File-4.pdf', date=datetime(1980, 2, 12), userId = 200, courseCode = '1ZV50')
        db.session.add(file4)
        db.session.commit()
    except:
        db.session.rollback()
    # We retrieve the files of the user with filename ascending
    files = getFilesByUser(200, 'filename.asc')
    # Check if the number of files is 4, 
    # that the first file is the file with alphabetically the first name, 
    # that the last file is the file with alphabetically the last name,
    # and that the userId for those files is correct.
    assert len(files) == 4
    assert files[0].get('filename') == 'File-1.pdf'
    assert files[0].get('userId') == 200
    assert files[3].get('filename') == 'File-4.pdf'
    assert files[3].get('userId') == 200

def testGetFilesSortedByFilenameDescending(testClient, initDatabaseEmpty):
    '''
        Test if we get the correct display if we run getFilesByUser(200, 'filename.desc'), so the representation of '<File <filename>>'. 
        Attributes: 
            file, file2, file1, file3, file4: File to be added to the database.
        Arguments:
            testClient:  The test client we test this for.
            initDatabase: the database instance we test this for. 
    '''
    del testClient, initDatabaseEmpty
    # We add five files to the database session
    try:
        db.session.commit()
    except:
        db.session.rollback()
    try: 
        file = Files(path='C:/normal/path/File-1.pdf', filename='File-1.pdf', date=datetime(2019, 2, 12), userId = 200, courseCode = '2IPE0')
        db.session.add(file)
        file2 = Files(path='C:/normal/path/File-2.pdf', filename='File-2.pdf', date=datetime(2019, 3, 4), userId = 201, courseCode = '2IPE0')
        db.session.add(file2)
        file1 = Files(path='C:/normal/path/File-3.pdf', filename='File-1.pdf', date=datetime(1999, 2, 12), userId = 200, courseCode = '2IPE0')
        db.session.add(file1)
        file3 = Files(path='C:/normal/path/File-3.pdf', filename='File-3.pdf', date=datetime(2020, 5, 6), userId = 200, courseCode = '2INC0')
        db.session.add(file3)
        file4 = Files(path='C:/normal/path/File-4.pdf', filename='File-4.pdf', date=datetime(1980, 2, 12), userId = 200, courseCode = '1ZV50')
        db.session.add(file4)
        db.session.commit()
    except: 
        db.session.rollback() 
    # We retrieve the files of the user with filename descending
    files = getFilesByUser(200, 'filename.desc')
    # Check if the number of files is 4, 
    # that the first file is the file with alphabetically the last name, 
    # that the last file is the file with alphabetically the first name,
    # and that the userId for those files is correct.
    assert len(files) == 4
    assert files[3].get('filename') == 'File-1.pdf'
    assert files[3].get('userId') == 200
    assert files[0].get('filename') == 'File-4.pdf'
    assert files[0].get('userId') == 200

def testGetFilesSortedByCourseNameDescending(testClient, initDatabaseEmpty):
    '''
        Test if we get the correct display if we run getFilesByUser(200, 'course.desc'), so the representation of '<File <filename>>'. 
        Attributes: 
            file, file2, file1, file3, file4: File to be added to the database.
        Arguments:
            testClient:  The test client we test this for.
            initDatabase: the database instance we test this for. 
    '''
    del testClient, initDatabaseEmpty
    # We add five files to the database session
    try:
        db.session.commit()
    except:
        db.session.rollback()
    try: 
        file = Files(path='C:/normal/path/File-1.pdf', filename='File-1.pdf', date=datetime(2019, 2, 12), userId = 200, courseCode = '2IPE0')
        db.session.add(file)
        file2 = Files(path='C:/normal/path/File-2.pdf', filename='File-2.pdf', date=datetime(2019, 3, 4), userId = 201, courseCode = '2IPE0')
        db.session.add(file2)
        file1 = Files(path='C:/normal/path/File-3.pdf', filename='File-1.pdf', date=datetime(1999, 2, 12), userId = 200, courseCode = '2IPE0')
        db.session.add(file1)
        file3 = Files(path='C:/normal/path/File-3.pdf', filename='File-3.pdf', date=datetime(2020, 5, 6), userId = 200, courseCode = '2INC0')
        db.session.add(file3)
        file4 = Files(path='C:/normal/path/File-4.pdf', filename='File-4.pdf', date=datetime(1980, 2, 12), userId = 200, courseCode = '1ZV50')
        db.session.add(file4)
        db.session.commit()
    except:
        db.session.rollback()
    # We retrieve the files of the user with course descending
    files = getFilesByUser(200, 'course.desc')
    # Check if the number of files is 5, 
    # that the first file is the file with alphabetically the first name, 
    # that the last file is the file with alphabetically the last name,
    # and that the userId for those files is correct.
    assert len(files) == 4
    assert files[3].get('filename') == 'File-4.pdf'
    assert files[3].get('userId') == 200
    assert files[3].get('courseCode') == '1ZV50'
    assert files[0].get('filename') == 'File-1.pdf'
    assert files[0].get('userId') == 200
    assert files[0].get('courseCode') == '2IPE0'

def testGetFilesSortedByCourseNameAscending(testClient, initDatabaseEmpty):
    '''
        Test if we get the correct display if we run getFilesByUser(200, 'course.asc'), so the representation of '<File <filename>>'. 
        Attributes: 
            file, file2, file1, file3, file4: File to be added to the database.
        Arguments:
            testClient:  The test client we test this for.
            initDatabase: the database instance we test this for. 
    '''
    del testClient, initDatabaseEmpty
    # We add five files to the database session
    try:
        db.session.commit()
    except:
        db.session.rollback()
    try: 
        file = Files(path='C:/normal/path/File-1.pdf', filename='File-1.pdf', date=datetime(2019, 2, 12), userId = 200, courseCode = '2IPE0')
        db.session.add(file)
        file2 = Files(path='C:/normal/path/File-2.pdf', filename='File-2.pdf', date=datetime(2019, 3, 4), userId = 201, courseCode = '2IPE0')
        db.session.add(file2)
        file1 = Files(path='C:/normal/path/File-3.pdf', filename='File-1.pdf', date=datetime(1999, 2, 12), userId = 200, courseCode = '2IPE0')
        db.session.add(file1)
        file3 = Files(path='C:/normal/path/File-3.pdf', filename='File-3.pdf', date=datetime(2020, 5, 6), userId = 200, courseCode = '2INC0')
        db.session.add(file3)
        file4 = Files(path='C:/normal/path/File-4.pdf', filename='File-4.pdf', date=datetime(1980, 2, 12), userId = 200, courseCode = '1ZV50')
        db.session.add(file4)
        db.session.commit()
    except:
        db.session.rollback() 
    # We retrieve the files of the user with course ascending
    files = getFilesByUser(200, 'course.asc')
    # Check if the number of files is 4, 
    # that the first file is the file with alphabetically the first name, 
    # that the last file is the file with alphabetically the last name,
    # and that the userId for those files is correct.
    assert len(files) == 4
    assert files[0].get('filename') == 'File-4.pdf'
    assert files[0].get('userId') == 200
    assert files[0].get('courseCode') == '1ZV50'
    assert files[3].get('filename') == 'File-1.pdf'
    assert files[3].get('userId') == 200
    assert files[3].get('courseCode') == '2IPE0'

def testGetFilesSortedByDateDescending(testClient, initDatabaseEmpty):
    '''
        Test if we get the correct display if we run getFilesByUser(200, 'date.desc'), so the representation of '<File <filename>>'. 
        Attributes: 
            file, file2, file1, file3, file4: File to be added to the database.
        Arguments:
            testClient:  The test client we test this for.
            initDatabase: the database instance we test this for. 
    '''
    del testClient, initDatabaseEmpty
    # We add five files to the database session
    try:
        db.session.commit()
    except:
        db.session.rollback()
    try: 
        file = Files(path='C:/normal/path/File-1.pdf', filename='File-1.pdf', date=datetime(2019, 2, 12), userId = 200, courseCode = '2IPE0')
        db.session.add(file)
        file2 = Files(path='C:/normal/path/File-2.pdf', filename='File-2.pdf', date=datetime(2019, 3, 4), userId = 201, courseCode = '2IPE0')
        db.session.add(file2)
        file1 = Files(path='C:/normal/path/File-3.pdf', filename='File-1.pdf', date=datetime(1999, 2, 12), userId = 200, courseCode = '2IPE0')
        db.session.add(file1)
        file3 = Files(path='C:/normal/path/File-3.pdf', filename='File-3.pdf', date=datetime(2020, 5, 6), userId = 200, courseCode = '2INC0')
        db.session.add(file3)
        file4 = Files(path='C:/normal/path/File-4.pdf', filename='File-4.pdf', date=datetime(1980, 2, 12), userId = 200, courseCode = '1ZV50')
        db.session.add(file4)
        db.session.commit()
    except:
        db.session.rollback()
    # We retrieve the files of the user with date descending
    files = getFilesByUser(200, 'date.desc')
    # Check if the number of files is 4, 
    # that the first file is the file with alphabetically the first name, 
    # that the last file is the file with alphabetically the last name,
    # and that the userId for those files is correct.
    assert len(files) == 4
    assert files[0].get('filename') == 'File-3.pdf'
    assert files[0].get('userId') == 200
    assert files[0].get('date') == datetime(2020, 5, 6)
    assert files[3].get('filename') == 'File-4.pdf'
    assert files[3].get('userId') == 200
    assert files[3].get('date') == datetime(1980, 2, 12)

def testCreateDatabase(testClient):
    '''
        Test if we don't get any errors if we run db.create_all()
        Arguments:
            testClient:  The test client we test this for.
    '''
    del testClient
    db.create_all()

def testFiles(testClient, initDatabase):
    '''
        Test if we get the correct display if we run Files.query.all(), so the representation of '<File <filename>>'. 
        Attributes: 
            files: all files of the type Files in the database.
        Arguments:
            testClient:  The test client we test this for.
            initDatabase: the database instance we test this for. 
    '''
    del testClient, initDatabase
    files = Files.query.all()
    assert str(files[0]) == '<File URD_Group3_vers03_Rc.pdf>'
    assert str(files[1]) == '<File SEP.pdf>'

def testRemoveFromDatabase(testClient, initDatabase):
    '''
        Test if we can remove a file from the database using the removeFromDatabase method. We first add a file to the database and then delete it. 
        After we have removed this file, we check that we can indeed not query on this file. 
        Attributes:
            file: File we create to add and remove in the database.
        Arguments:
            testClient:  The test client we test this for.
            initDatabase: the database instance we test this for. 
    '''
    del testClient, initDatabase
    # Create the file instance to be added:
    file = Files(path='C:/Users/20192435/Downloads/SEP2021/WriterDesk1/backend/saved_documents/ScrumAndXpFromTheTrenchesonline07-31.pdf', 
    filename='ScrumAndXpFromTheTrenchesonline07-31.pdf', date=datetime(2019, 2, 12), userId = 123, courseCode = '2IPE0')
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
    id = 1

    # Get the BASEDIR and set the fileDir with that:
    BASEDIR = os.path.abspath(os.path.dirname(__file__))
    fileDir = os.path.join(BASEDIR, fileName)
    # open(fileDir, 'rb')
    # Create the data packet:
    data = {
        'files': (open(fileDir, 'rb'), fileName),
        'id': id,
        'fileName': fileName,
        'courseCode': courseCode,
        'userId': userId,
        'date': date1
    }
    # print(data)

    # Create the response by means of the post request:
    response = testClient.post('/fileapi/upload', data=data)

    # # See if we indeed get code 200 and the correct message from this request:
    # assert response.data == b'success'
    # assert response.status_code == 200

    # See if the correct data has been added to the database which we retrieve by the filename:
    file = Files.query.filter_by(filename=secure_filename(fileName)).first()

    # assert file.filename == secure_filename(fileName)
    # assert file.id == id
    # assert file.courseCode == courseCode
    # assert file.userId == userId
    # assert file.date == datetime.combine(date1, datetime.min.time())
    # # Check if the file has indeed been added to the disk:
    # assert os.path.exists(file.path)
    # # See if we can also retrieve the file by querying by userId:
    # assert Files.query.filter_by(filename= secure_filename(fileName)).first() in Files.query.filter_by(userId=userId).all()
    ###
    # print(file)
    # print("HEEYY1")
    # print(data)
    # if data.get('files').open:
    #     print('file is closed')
    # else:
    #     print("uuuh")
    # Delete the file
    print(data) 
    response2 = testClient.post('/fileapi/filedelete', data=data)
    print("HEEYY2")
    # Check if the file has been deleted of the disk
    assert not os.path.exists(file.path)
    # See if we also cannot retrieve the file by querying the userId
    assert Files.query.filter_by(filename= secure_filename(fileName)).first() not in Files.query.filter_by(userId=userId).all()