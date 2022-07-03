from distutils.command.upload import upload
from app.models import Files
from app.database import uploadToDatabase, getFilesByUser, removeFromDatabase
from app import db
from datetime import datetime, date
import os
from werkzeug.utils import secure_filename
 
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