from app.models import User
from app import create_app, db
import json

def test_valid_login(testClient, initDatabase):
    '''
    TODO ADD COMMENTS
    '''

    del initDatabase
    data = {
        'username':'Pietje',
        'password':'Bell',
    }

    response = testClient.post('/loginapi/login', json=data, headers={"Content-Type": "application/json"})
    assert response.status_code == 200

def test_invalid_login(testClient,initDatabase):
    '''
    TODO ADD COMMENTS
    '''
    del initDatabase
    data = {
        'username':'Pietje',
        'password':'Duck',
    }

    response = testClient.post('/loginapi/login', json=data, headers={"Content-Type": "application/json"})
    assert response.status_code == 401