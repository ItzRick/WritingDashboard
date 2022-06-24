from flask import current_app

def testGetCurrentFeedbackVersion(testClient):
    '''
        Test the getCurrentFeedbackVersion method to see if we can retrieve the correct feedbackmodel version.
        Attributes:
            response: Response we get from the get request.
        Arguments:
            testClient:  The test client we test this for. 
    '''
    # Set the FEEDBACKVERSION to a known value:
    current_app.config['FEEDBACKVERSION'] = '0.01'
    response = testClient.get('/feedback/getCurrentVersion')   
    # Test if we also correctly retrieve this feedback version:
    assert response.status_code == 200
    assert response.data == b'0.01'