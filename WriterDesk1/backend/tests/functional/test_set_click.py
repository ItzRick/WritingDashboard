from app.models import User, Clicks
from test_set_role import loginHelper

def test_set_click(testClient, initDatabase):
    '''
    Test if we can properly set a click instance
    Assumed that currentUser=='Pietje' with current plainTextPassword=='Bell'
    Arguments:
        testClient:   The test client we test this for.
        initDatabase: The database instance we test this for.
    '''
    del initDatabase
    user = User.query.filter_by(username='Pietje').first()

    #check username and password
    assert user.username == 'Pietje'
    assert user.check_password('Bell')
    # get access token for Pietje Bell
    access_token = loginHelper(testClient, 'Pietje', 'Bell')

    url = 'test'
    # set new password in data
    data = {
        'url':url,
    }

    # test response data
    response = testClient.post('/clickapi/setClick', data=data, headers = {"Authorization": "Bearer " + access_token})
    assert response.status_code == 200
    # test if other data gets set
    click = Clicks.query.filter_by(userId = user.id).all()
    assert len(click) == 1
    assert click[0].url == url
    assert click[0].timestamp is not None