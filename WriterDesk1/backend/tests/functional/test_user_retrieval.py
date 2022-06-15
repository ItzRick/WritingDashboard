from distutils.command.upload import upload
from app.models import User
from app.database import uploadToDatabase, getFilesByUser, removeFromDatabase
from app import db
from datetime import datetime, date
import os
from werkzeug.utils import secure_filename
import json


def testRetrieveUsers(testClient, initDatabaseEmpty):
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
            expected_response: the response we expect when we run the function.
    '''
    del initDatabaseEmpty

    # We add five users to the database session
    try:
        db.session.commit()
    except:
        db.session.rollback()
    try:
        user = User(username='John', password_plaintext='blegh')
        db.session.add(user)
        user2 = User(username='Kevin', password_plaintext='bleh')
        db.session.add(user2)
        user3 = User(username='Samantha', password_plaintext='bleurgh')
        user3.role = 'participant'
        db.session.add(user3)
        user4 = User(username='Timothy', password_plaintext='bleeeeeh')
        db.session.add(user4)
        user5 = User(username='Bobby', password_plaintext='blaargh')

        db.session.add(user5)
        db.session.commit()
    except:
        db.session.rollback()

    # Retrieve the users except for those with the participant role
    response = testClient.get('/usersapi/users')

    # Check if we get the correct status_code:
    assert response.status_code == 200
    # Create the expected response:
    expected_response = [dict(type='user',
                              id='123',
                              username='John'
                              ),
                         dict(type='user',
                              id='124',
                              username='Kevin'
                              ),
                         dict(type='user',
                              id='126',
                              username='Timothy'
                              ),
                         dict(type='user',
                              id='127',
                              username='Bobby'
                              ),
                         ]

    # Check if the expected response is correct:
    assert json.loads(response.data) == expected_response