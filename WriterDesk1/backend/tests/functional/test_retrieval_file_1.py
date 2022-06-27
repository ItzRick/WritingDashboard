from distutils.command.upload import upload
from app.models import Files, User
from app.database import uploadToDatabase, getFilesByUser, removeFromDatabase
from app import db
from datetime import datetime, date
import os
from werkzeug.utils import secure_filename
import json
from test_set_role import loginHelper

from test_set_role import loginHelper

def testRetrieveFilesOfUserDateAsc(testClient, initDatabase):
    '''
        This test checks the retrieval of of files in a specified order, namely
        date ascending, of a certain user, here with user id 200, in a json file.
        Arguments:
            testClient:  The test client we test this for.
            initDatabase: the database instance we test this for. 
        Attributes: 
            file, file2, file1, file3, file4: File to be added to the database.
            userId: the user for which the files are retrieved
            sortingAttribute: the specified order of the retrieved files
            access_token: access token
            data: data intended for the api
            response: the result fo retrieving the files in the specified order
            expected_response: the response we expect when we run the function.
    '''
    del initDatabase
    # We define the user and sorting order
    userId = User.query.filter_by(username='Pietje').first().id
    sortingAttribute = 'date.asc'

    # get access token for the regular user
    access_token = loginHelper(testClient, 'Pietje', 'Bell')

    data = {
        'userId': userId,
        'sortingAttribute': sortingAttribute,
    }

    # We add five files to the database session
    file = Files(path='C:/normal/path/File-1.pdf', filename='File-1.pdf', fileType='.pdf', date=datetime(2019, 2, 12), userId=userId, courseCode='2IPE0', id=101)
    db.session.add(file)
    file2 = Files(path='C:/normal/path/File-2.pdf', filename='File-2.pdf', fileType='.pdf', date=datetime(2019, 3, 4), userId=201, courseCode='2IPE0', id=102)
    db.session.add(file2)
    file1 = Files(path='C:/normal/path/File-3.pdf', filename='File-3.pdf', fileType='.pdf', date=datetime(1999, 2, 12), userId=userId, courseCode='2IPE0', id=103)
    db.session.add(file1)
    file3 = Files(path='C:/normal/path/File-4.pdf', filename='File-4.pdf', fileType='.pdf', date=datetime(2020, 5, 6), userId=userId, courseCode='2INC0', id=104)
    db.session.add(file3)
    file4 = Files(path='C:/normal/path/File-5.pdf', filename='File-5.pdf', fileType='.pdf', date=datetime(1980, 2, 12), userId=userId, courseCode='1ZV50', id=105)
    db.session.add(file4)
    db.session.commit()
        
    # Retrieve the files from the specified user
    response = testClient.get('/fileapi/fileretrieve', query_string=data, headers={"Authorization": "Bearer " + access_token})

    # Check if we get the correct status_code:
    assert response.status_code == 200
    # Create the expected response:
    expected_response = [dict(courseCode='1ZV50', 
                        date='12/02/80',
                        fileType='.pdf',
                        path='C:/normal/path/File-5.pdf', 
                        userId=userId, 
                        filename='File-5.pdf', 
                        id=105
                        ),
                        dict(courseCode='2IPE0', 
                        date='12/02/99',
                        fileType='.pdf',
                        path='C:/normal/path/File-3.pdf', 
                        userId=userId, 
                        filename='File-3.pdf', 
                        id=103
                        ),
                        dict(courseCode='2IPE0', 
                        date='12/02/19',
                        fileType='.pdf',
                        path='C:/normal/path/File-1.pdf', 
                        userId=userId, 
                        filename='File-1.pdf', 
                        id=101
                        ), 
                        dict(courseCode='2INC0', 
                        date='06/05/20',
                        fileType='.pdf',
                        path='C:/normal/path/File-4.pdf', 
                        userId=userId, 
                        filename='File-4.pdf', 
                        id=104
                        )]

    # Check if the expected response is correct:
    assert json.loads(response.data) == expected_response

def testRetrieveFilesOfUserDateDesc(testClient, initDatabase):
    '''
        This test checks the retrieval of of files in a specified order, namely
        date descending, of a certain user, here with user id 200, in a json file.
        Arguments:
            testClient:  The test client we test this for.
            initDatabase: the database instance we test this for. 
        Attributes: 
            file, file2, file1, file3, file4: File to be added to the database.
            userId: the user for which the files are retrieved
            sortingAttribute: the specified order of the retrieved files
            access_token: access token
            data: data intended for the api
            response: the result fo retrieving the files in the specified order
            expected_response: the response we expect when we run the function.
    '''
    del initDatabase
    # We define the user and sorting order
    userId = User.query.filter_by(username='Pietje').first().id
    sortingAttribute = 'date.desc'

    # get access token for the regular user
    access_token = loginHelper(testClient, 'Pietje', 'Bell')

    data = {
        'userId': userId,
        'sortingAttribute': sortingAttribute,
    }

    # We add five files to the database session
    file = Files(path='C:/normal/path/File-1.pdf', filename='File-1.pdf', fileType='.pdf', date=datetime(2019, 2, 12), userId = userId, courseCode = '2IPE0', id=101)
    db.session.add(file)
    file2 = Files(path='C:/normal/path/File-2.pdf', filename='File-2.pdf', fileType='.pdf', date=datetime(2019, 3, 4), userId = 201, courseCode = '2IPE0', id=102)
    db.session.add(file2)
    file1 = Files(path='C:/normal/path/File-3.pdf', filename='File-3.pdf', fileType='.pdf', date=datetime(1999, 2, 12), userId = userId, courseCode = '2IPE0', id=103)
    db.session.add(file1)
    file3 = Files(path='C:/normal/path/File-4.pdf', filename='File-4.pdf', fileType='.pdf', date=datetime(2020, 5, 6), userId = userId, courseCode = '2INC0', id=104)
    db.session.add(file3)
    file4 = Files(path='C:/normal/path/File-5.pdf', filename='File-5.pdf', fileType='.pdf', date=datetime(1980, 2, 12), userId = userId, courseCode = '1ZV50', id=105)
    db.session.add(file4)
    db.session.commit()
        
    # Retrieve the files from the specified user
    response = testClient.get('/fileapi/fileretrieve', query_string=data, headers={"Authorization": "Bearer " + access_token})

    # Check if we get the correct status_code:
    assert response.status_code == 200
    # Create the expected response: 
    expected_response = [dict(courseCode='2INC0', 
                        date='06/05/20',
                        fileType='.pdf',
                        path='C:/normal/path/File-4.pdf', 
                        userId=userId, 
                        filename='File-4.pdf', 
                        id=104
                        ), 
                        dict(courseCode='2IPE0', 
                        date='12/02/19',
                        fileType='.pdf',
                        path='C:/normal/path/File-1.pdf', 
                        userId=userId, 
                        filename='File-1.pdf', 
                        id=101
                        ), 
                        dict(courseCode='2IPE0', 
                        date='12/02/99',
                        fileType='.pdf',
                        path='C:/normal/path/File-3.pdf', 
                        userId=userId, 
                        filename='File-3.pdf', 
                        id=103
                        ),                                                
                        dict(courseCode='1ZV50', 
                        date='12/02/80',
                        fileType='.pdf',
                        path='C:/normal/path/File-5.pdf', 
                        userId=userId, 
                        filename='File-5.pdf', 
                        id=105
                        )]

    # Check if the expected response is correct:
    assert json.loads(response.data) == expected_response

def testRetrieveFilesOfUserFilenameAsc(testClient, initDatabase):
    '''
        This test checks the retrieval of of files in a specified order, namely
        file name ascending, of a certain user, here with user id 200, in a json file.
        Arguments:
            testClient:  The test client we test this for.
            initDatabase: the database instance we test this for. 
        Attributes: 
            file, file2, file1, file3, file4: File to be added to the database.
            userId: the user for which the files are retrieved
            sortingAttribute: the specified order of the retrieved files
            access_token: access token
            data: data intended for the api
            response: the result fo retrieving the files in the specified order
            expected_response: the response we expect when we run the function.
    '''
    del initDatabase
    # We define the user and sorting order
    userId = User.query.filter_by(username='Pietje').first().id
    sortingAttribute = 'filename.asc'

    # get access token for the regular user
    access_token = loginHelper(testClient, 'Pietje', 'Bell')

    data = {
        'userId': userId,
        'sortingAttribute': sortingAttribute,
    }

    # We add five files to the database session
    file = Files(path='C:/normal/path/File-1.pdf', filename='File-1.pdf', fileType='.pdf', date=datetime(2019, 2, 12), userId = userId, courseCode = '2IPE0', id=101)
    db.session.add(file)
    file2 = Files(path='C:/normal/path/File-2.pdf', filename='File-2.pdf', fileType='.pdf', date=datetime(2019, 3, 4), userId = 201, courseCode = '2IPE0', id=102)
    db.session.add(file2)
    file1 = Files(path='C:/normal/path/File-3.pdf', filename='File-3.pdf', fileType='.pdf', date=datetime(1999, 2, 12), userId = userId, courseCode = '2IPE0', id=103)
    db.session.add(file1)
    file3 = Files(path='C:/normal/path/File-4.pdf', filename='File-4.pdf', fileType='.pdf', date=datetime(2020, 5, 6), userId = userId, courseCode = '2INC0', id=104)
    db.session.add(file3)
    file4 = Files(path='C:/normal/path/File-5.pdf', filename='File-5.pdf', fileType='.pdf', date=datetime(1980, 2, 12), userId = userId, courseCode = '1ZV50', id=105)
    db.session.add(file4)
    db.session.commit()
        
    # Retrieve the files from the specified user
    response = testClient.get('/fileapi/fileretrieve', query_string=data, headers={"Authorization": "Bearer " + access_token})

    # Check if we get the correct status_code:
    assert response.status_code == 200
    # Create the expected response:
    expected_response = [dict(courseCode='2IPE0', 
                        date='12/02/19',
                        fileType='.pdf',
                        path='C:/normal/path/File-1.pdf', 
                        userId=userId, 
                        filename='File-1.pdf', 
                        id=101
                        ), 
                        dict(courseCode='2IPE0', 
                        date='12/02/99',
                        fileType='.pdf',
                        path='C:/normal/path/File-3.pdf', 
                        userId=userId, 
                        filename='File-3.pdf', 
                        id=103
                        ),
                        dict(courseCode='2INC0', 
                        date='06/05/20',
                        fileType='.pdf',
                        path='C:/normal/path/File-4.pdf', 
                        userId=userId, 
                        filename='File-4.pdf', 
                        id=104
                        ),
                        dict(courseCode='1ZV50', 
                        date='12/02/80',
                        fileType='.pdf',
                        path='C:/normal/path/File-5.pdf', 
                        userId=userId, 
                        filename='File-5.pdf', 
                        id=105
                        )]

    # Check if the expected response is correct:
    assert json.loads(response.data) == expected_response

def testRetrieveFilesOfUserFilenameDesc(testClient, initDatabase):
    '''
        This test checks the retrieval of of files in a specified order, namely
        filename descending, of a certain user, here with user id 200, in a json file.
        Arguments:
            testClient:  The test client we test this for.
            initDatabase: the database instance we test this for. 
        Attributes: 
            file, file2, file1, file3, file4: File to be added to the database.
            userId: the user for which the files are retrieved
            sortingAttribute: the specified order of the retrieved files
            access_token: access token
            data: data intended for the api
            response: the result fo retrieving the files in the specified order
            expected_response: the response we expect when we run the function.
    '''
    del initDatabase
    # We define the user and sorting order
    userId = User.query.filter_by(username='Pietje').first().id
    sortingAttribute = 'filename.desc'

    # get access token for the regular user
    access_token = loginHelper(testClient, 'Pietje', 'Bell')

    data = {
        'userId': userId,
        'sortingAttribute': sortingAttribute,
    }

    # We add five files to the database session
    file = Files(path='C:/normal/path/File-1.pdf', filename='File-1.pdf', fileType='.pdf', date=datetime(2019, 2, 12), userId = userId, courseCode = '2IPE0', id=101)
    db.session.add(file)
    file2 = Files(path='C:/normal/path/File-2.pdf', filename='File-2.pdf', fileType='.pdf', date=datetime(2019, 3, 4), userId = 201, courseCode = '2IPE0', id=102)
    db.session.add(file2)
    file1 = Files(path='C:/normal/path/File-3.pdf', filename='File-3.pdf', fileType='.pdf', date=datetime(1999, 2, 12), userId = userId, courseCode = '2IPE0', id=103)
    db.session.add(file1)
    file3 = Files(path='C:/normal/path/File-4.pdf', filename='File-4.pdf', fileType='.pdf', date=datetime(2020, 5, 6), userId = userId, courseCode = '2INC0', id=104)
    db.session.add(file3)
    file4 = Files(path='C:/normal/path/File-5.pdf', filename='File-5.pdf', fileType='.pdf', date=datetime(1980, 2, 12), userId = userId, courseCode = '1ZV50', id=105)
    db.session.add(file4)
    db.session.commit()
        
    # Retrieve the files from the specified user
    response = testClient.get('/fileapi/fileretrieve', query_string=data, headers={"Authorization": "Bearer " + access_token})

    # Check if we get the correct status_code:
    assert response.status_code == 200
    # Create the expected response:
    expected_response = [dict(courseCode='1ZV50', 
                        date='12/02/80',
                        fileType='.pdf',
                        path='C:/normal/path/File-5.pdf', 
                        userId=userId, 
                        filename='File-5.pdf', 
                        id=105
                        ),
                        dict(courseCode='2INC0', 
                        date='06/05/20',
                        fileType='.pdf',
                        path='C:/normal/path/File-4.pdf', 
                        userId=userId, 
                        filename='File-4.pdf', 
                        id=104
                        ),
                        dict(courseCode='2IPE0', 
                        date='12/02/99',
                        fileType='.pdf',
                        path='C:/normal/path/File-3.pdf', 
                        userId=userId, 
                        filename='File-3.pdf', 
                        id=103
                        ), 
                        dict(courseCode='2IPE0', 
                        date='12/02/19',
                        fileType='.pdf',
                        path='C:/normal/path/File-1.pdf', 
                        userId=userId, 
                        filename='File-1.pdf', 
                        id=101
                        )]

    # Check if the expected response is correct:
    assert json.loads(response.data) == expected_response