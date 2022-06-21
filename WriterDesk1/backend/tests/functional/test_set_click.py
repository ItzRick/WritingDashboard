from app.models import User, Clicks
from test_set_role import loginHelper
from app.database import uploadToDatabase

def test_set_click(testClient, initDatabase):
    '''
    Test if we can properly set a click instance
    Assumed that currentUser=='Pietje' with current plainTextPassword=='Bell'
    Arguments:
        testClient:   The test client we test this for.
        initDatabase: The database instance we test this for.
    Atributes:
        user: user for whom to set the click
        access_token: the access token
        url: url of the current page as given by the frontend
        eventType: type of event, can be one of [click.button, click.link, view.document, click.highlight]
        actionId: String giving additional information to the event
        data: data for setClick
        response: response from the api call
        click: clicks related to the user
    '''
    del initDatabase
    user = User.query.filter_by(username='Pietje').first()

    #check username and password
    assert user.username == 'Pietje'
    assert user.check_password('Bell')
    # get access token for Pietje Bell
    access_token = loginHelper(testClient, 'Pietje', 'Bell')

    url = 'Progress'
    eventType = 'click.button'
    actionId = 'actionId'
    # set new password in data
    data = {
        'url':url,
        'eventType':eventType,
        'actionId':actionId, 
    }

    # test response data
    response = testClient.post('/clickapi/addClick', data=data, headers = {"Authorization": "Bearer " + access_token})
    assert response.status_code == 200
    # test if data gets set
    click = Clicks.query.filter_by(userId = user.id).all()
    assert len(click) == 1
    assert click[0].url == url
    assert click[0].timestamp is not None
    assert click[0].eventType == eventType
    assert click[0].actionId == actionId

def testClickNoTrackingPlz(testClient, initDatabase):
    '''
    Test if we get rejected when we try to call the api for a user that does not want to be tracked
    Arguments:
        testClient:   The test client we test this for.
        initDatabase: The database instance we test this for.
    Atributes:
        uname: username for user
        upass: user password for the user
        user: user for whom to set the click
        access_token: the access token
        data: data for setClick
        response: response from the api call
    '''
    del initDatabase
    uname = 'untracktor'
    upass = 'pass'
    # create a user that does not want to be tracked
    user = User(username=uname, password_plaintext=upass, trackable=False)
    # test if user.trackable is false
    uploadToDatabase(user)
    user = User.query.filter_by(username=uname).first()
    assert user is not None
    assert not user.trackable

    # get access token for the user
    access_token = loginHelper(testClient, uname, upass)

    # set new password in data
    data = {
        'url':'',
        'eventType':'click.button', # valid eventType
        'actionId':'', 
    }

    # test response data
    response = testClient.post('/clickapi/addClick', data=data, headers = {"Authorization": "Bearer " + access_token})
    assert response.status_code == 451
    assert response.data == b'User clicks not trackable'

def testClickInvalidEventType(testClient, initDatabase):
    '''
    Test if we get an error when we provide an invalid eventType
    Arguments:
        testClient:   The test client we test this for.
        initDatabase: The database instance we test this for.
    Atributes:
        user: user for whom to set the click
        access_token: the access token
        data: data for setClick
        response: response from the api call
    '''
    del initDatabase
    user = User.query.filter_by(username='Pietje').first()

    #check username and password
    assert user.username == 'Pietje'
    assert user.check_password('Bell')
    # get access token for Pietje Bell
    access_token = loginHelper(testClient, 'Pietje', 'Bell')
    # set new password in data
    data = {
        'url':'',
        'eventType':'invalid', # invalid event type
        'actionId':'', 
    }

    # test response data
    response = testClient.post('/clickapi/addClick', data=data, headers = {"Authorization": "Bearer " + access_token})
    assert response.status_code == 400
    assert response.data == b'Invalid eventType'