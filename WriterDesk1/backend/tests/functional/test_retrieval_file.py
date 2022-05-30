from distutils.command.upload import upload
from app.models import Files
from app.database import uploadToDatabase, getFilesByUser, removeFromDatabase
from app import db
from datetime import datetime, date
import os
from werkzeug.utils import secure_filename

def testRetrieveFilesOfUser(testClient, initDatabaseEmpty):
    '''
        This test checks the retrieval of of files in a specified order, namely
        date ascending, of a certain user, here with user id 200, in a json file.
        Attributes: 
            file, file2, file1, file3, file4: File to be added to the database.
        Arguments:
            testClient:  The test client we test this for.
            initDatabase: the database instance we test this for. 
            userId: the user for which the files are retrieved
            sortingAttribute: the specified order of the retrieved files
            response: the result fo retrieving the files in the specified order
    '''
    del testClient, initDatabaseEmpty
    # We define the user and sorting order
    userId = 200
    sortingAttribute = date.asc

    data = {
        'userId': userId,
        'sortingAttribute': sortingAttribute,
    }

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
        
    # Retrieve the files from the specified user
    response = testClient.get('/fileapi/fileretrieve', data=data)

    assert True


def testRetrieveFilesOfUserWithoutFiles(testClient, initDatabaseEmpty):
    '''
        This test checks the retrieval of files in a specified order, namely date ascending, 
        of a certain user that has not uploaded any files, here with user id 202, in a json file.
        Attributes: 
            file, file2, file1, file3, file4: File to be added to the database.
        Arguments:
            testClient:  The test client we test this for.
            initDatabase: the database instance we test this for. 
            userId: the user for which the files are retrieved
            sortingAttribute: the specified order of the retrieved files
            response: the result fo retrieving the files in the specified order
    '''
    del testClient, initDatabaseEmpty
    # We define the user and sorting order
    userId = 202
    sortingAttr = date.asc

    data = {
        'userId': userId,
        'sortingAttribute': sortingAttr,
    }

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
        
    # Retrieve the files from the specified user
    response = testClient.get('/fileapi/fileretrieve', data=data)

    assert True