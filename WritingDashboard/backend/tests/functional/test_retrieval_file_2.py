from app.models import Files, User, Scores
from app import db
from datetime import datetime
from werkzeug.utils import secure_filename
import json
from test_set_role import loginHelper
from decimal import Decimal

def testRetrieveFilesOfUserCourseAsc(testClient, initDatabase):
    '''
        This test checks the retrieval of of files in a specified order, namely
        course name ascending, of a certain user, here with user id 200, in a json file.
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
    sortingAttribute = 'course.asc'

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
                        progress=0,
                        userId=userId, 
                        filename='File-5.pdf', 
                        id=105
                        ),
                        dict(courseCode='2INC0', 
                        date='06/05/20',
                        fileType='.pdf',
                        path='C:/normal/path/File-4.pdf', 
                        progress=0,
                        userId=userId, 
                        filename='File-4.pdf', 
                        id=104
                        ),
                        dict(courseCode='2IPE0', 
                        date='12/02/19',
                        fileType='.pdf',
                        path='C:/normal/path/File-1.pdf',
                        progress=0, 
                        userId=userId, 
                        filename='File-1.pdf', 
                        id=101
                        ),
                        dict(courseCode='2IPE0', 
                        date='12/02/99',
                        fileType='.pdf',
                        path='C:/normal/path/File-3.pdf', 
                        progress=0,
                        userId=userId, 
                        filename='File-3.pdf', 
                        id=103
                        )]

    # Check if the expected response is correct:
    assert json.loads(response.data) == expected_response

def testRetrieveFilesOfUserCourseDesc(testClient, initDatabase):
    '''
        This test checks the retrieval of of files in a specified order, namely
        course name descending, of a certain user, here with user id 200, in a json file.
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
    sortingAttribute = 'course.desc'

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
                        progress=0,
                        userId=userId, 
                        filename='File-1.pdf', 
                        id=101
                        ),
                        dict(courseCode='2IPE0', 
                        date='12/02/99',
                        fileType='.pdf',
                        path='C:/normal/path/File-3.pdf', 
                        progress=0,
                        userId=userId, 
                        filename='File-3.pdf', 
                        id=103
                        ), 
                        dict(courseCode='2INC0', 
                        date='06/05/20',
                        fileType='.pdf',
                        path='C:/normal/path/File-4.pdf', 
                        progress=0,
                        userId=userId, 
                        filename='File-4.pdf', 
                        id=104
                        ),
                        dict(courseCode='1ZV50', 
                        date='12/02/80',
                        fileType='.pdf',
                        path='C:/normal/path/File-5.pdf', 
                        progress=0,
                        userId=userId, 
                        filename='File-5.pdf', 
                        id=105
                        )]

    # Check if the expected response is correct:
    assert json.loads(response.data) == expected_response

def testRetrieveFilesOfUserWithoutFiles(testClient, initDatabase):
    '''
        This test checks the retrieval of files in a specified order, namely date ascending, 
        of a certain user that has not uploaded any files, here with user id 202, in a json file.
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
    '''
    del initDatabase
    # We define the user and sorting order
    userId = User.query.filter_by(username='Pietje').first().id
    sortingAttr = 'date.asc'

    # get access token for the regular user
    access_token = loginHelper(testClient, 'Pietje', 'Bell')

    data = {
        'userId': userId,
        'sortingAttribute': sortingAttr,
    }

    # We add five files to the database session
    file = Files(path='C:/normal/path/File-1.pdf', filename='File-1.pdf', fileType='.pdf', date=datetime(2019, 2, 12), userId = 202, courseCode = '2IPE0', id=101)
    db.session.add(file)
    file2 = Files(path='C:/normal/path/File-2.pdf', filename='File-2.pdf', fileType='.pdf', date=datetime(2019, 3, 4), userId = 201, courseCode = '2IPE0', id=102)
    db.session.add(file2)
    file1 = Files(path='C:/normal/path/File-3.pdf', filename='File-3.pdf', fileType='.pdf', date=datetime(1999, 2, 12), userId = 202, courseCode = '2IPE0', id=103)
    db.session.add(file1)
    file3 = Files(path='C:/normal/path/File-4.pdf', filename='File-4.pdf', fileType='.pdf', date=datetime(2020, 5, 6), userId = 202, courseCode = '2INC0', id=104)
    db.session.add(file3)
    file4 = Files(path='C:/normal/path/File-5.pdf', filename='File-5.pdf', fileType='.pdf', date=datetime(1980, 2, 12), userId = 202, courseCode = '1ZV50', id=105)
    db.session.add(file4)
    db.session.commit()
    
    # Retrieve the files from the specified user
    response = testClient.get('/fileapi/fileretrieve', query_string=data, headers={"Authorization": "Bearer " + access_token})

    # Check if we get the correct status code:
    assert response.status_code == 200
    # Check if we indeed get no data back:
    assert json.loads(response.data) == []

def testRetrieveFilesProgress(testClient, initDatabase):
    '''
        Test if we also correctly generate the progress if we have a file with scores.
        Arguments:
            testClient:  The test client we test this for.
            initDatabase: the database instance we test this for. 
        Attributes: 
            file: File to be added to the database.
            score: Score corresponding to this file.
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
    sortingAttribute = 'course.desc'

    # get access token for the regular user
    access_token = loginHelper(testClient, 'Pietje', 'Bell')

    data = {
        'userId': userId,
        'sortingAttribute': sortingAttribute,
    }

    # We add five one to the database session:
    file = Files(path='C:/normal/path/File-1.pdf', filename='File-1.pdf', fileType='.pdf', date=datetime(2019, 2, 12), userId = userId, courseCode = '2IPE0', id=101)
    # Add the score to the database:
    score = Scores(fileId=101, scoreStyle=1, scoreCohesion=1, scoreStructure=0, scoreIntegration=10, feedbackVersion=1)
    db.session.add(file)
    db.session.add(score)
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
                        progress=100,
                        scoreCohesion='1.00', 
                        scoreIntegration='10.00',
                        scoreStructure='0.00',
                        scoreStyle='1.00',
                        feedbackVersion='1.00',
                        userId=userId, 
                        filename='File-1.pdf', 
                        id=101
                        )]

    # Check if the expected response is correct:
    assert json.loads(response.data) == expected_response