from test_genFeedback import uploadFile
from app.models import Files, Scores, Explanations
import fitz
import json

def testGenerateFeedbackNoFile(testClient, initDatabase):
    '''
        Test the feedback/generate API on a file that is not in the database.
        Attributes:
            data: Data we send with the post request.
            response: Response we get from the post request.
            access_token: the access token
        Arguments:
            testClient:  The test client we test this for.
            initDatabase: the database instance we test this for. 
    '''
    del initDatabase
    data = {
        'fileId': 3
    }
    access_token = loginHelper(testClient, 'ad', 'min')    
    response = testClient.post('/feedback/generate', query_string=data,
                                headers={"Authorization": "Bearer " + access_token})   
    assert response.status_code == 400
    assert response.data == b'The file with id 3 can not be found in the database.'

def testGenerateFeedbackNoFileOnDisk(testClient, initDatabase):
    '''
        Test the feedback/generate API on a file that is not on the disk, but in the database.
        Attributes:
            data: Data we send with the post request.
            response: Response we get from the post request.
            access_token: the access token
        Arguments:
            testClient:  The test client we test this for.
            initDatabase: the database instance we test this for. 
    '''
    del initDatabase
    file = Files.query.first()
    data = {
        'fileId': file.id
    }    
    access_token = loginHelper(testClient, 'ad', 'min')    
    response = testClient.post('/feedback/generate', query_string=data,
                                headers={"Authorization": "Bearer " + access_token})    
    assert response.status_code == 400
    # Test if the response message contains 'no such file':
    assert 'no such file' in response.data.decode("utf-8")

def testGenerateFeedbackPdf(testClient, initDatabase):
    '''
        Test the feedback/generate API on a pdf file.
        Attributes:
            data: Data we send with the post request.
            response: Response we get from the post request.
            file: A file which has been added to uploaded to the application using the uploadFile method.
            isSuccessful: Boolean retrieved from the uploadFile method to indicate if we have correctly calculated the score.
            score: scores as retrieved from the database after running the genFeedback method.
            fileId: fileId of this file that has been previously added to the database.
            mistakes: mistakes in the correct format as given to the setFeedbackStyle method. 
            BASEPATH: Path of the current test_setFeedbackStyle.py file.
            fileLoc: Location of the file we test this for.
            explanations: Database for the current file, containing explanations, as retrieved from the database 
                and created using the genFeedback method.
            access_token: the access token
        Arguments:
            testClient:  The test client we test this for.
            initDatabase: the database instance we test this for. 
    '''
    del initDatabase
    file = uploadFile('testfeedback_1.pdf', testClient)
    data = {
        'fileId': file.id
    }    
    access_token = loginHelper(testClient, 'ad', 'min')    
    response = testClient.post('/feedback/generate', query_string=data,
                                headers={"Authorization": "Bearer " + access_token})   
    assert response.status_code == 200
    assert response.data == b'Feedback has been generated!'
    # Check if we have added the correct score to the database:
    score = Scores.query.filter_by(fileId=file.id).first()
    assert float(score.scoreStyle) == 8.40
    assert float(score.scoreCohesion) == 7.81
    assert float(score.scoreStructure) == 6.5
    assert float(score.scoreIntegration) == 0.0
    # Get all explanations for this file from the database.
    explanations = Explanations.query.filter_by(fileId = file.id).all()
    # Check if all explanations have been added to the database:
    assert len(explanations) == 9
    # Check if all information about the style mistakes mistake has been added to this database correctly:
    assert explanations[0].mistakeText == 'a'
    assert explanations[0].explanation == 'Use “an” instead of ‘a’ if the following word starts with a vowel sound, e.g. ‘an article’, ‘an hour’.'
    assert explanations[0].type == 0
    assert explanations[0].replacement1 == 'an'
    assert explanations[1].mistakeText == 'must try'
    assert explanations[1].explanation == 'It appears that a hyphen is missing in this expression.'
    assert explanations[1].type == 0
    assert explanations[1].replacement1 == 'must-try'
    # Check if the coordinates of the style mistakes have also been found correctly:
    doc = fitz.open(file.path)
    page = doc.load_page(0)
    assert page.get_textbox(fitz.Rect(explanations[0].X1, explanations[0].Y1, explanations[0].X2, explanations[0].Y2)) == 'a'
    assert page.get_textbox(fitz.Rect(explanations[1].X1, explanations[1].Y1, explanations[1].X2, explanations[1].Y2)) == 'must try'
    # Check if the Cohesion mistakes have been added to the database correctly:
    assert explanations[2].mistakeText == ''
    assert explanations[2].explanation == ('Your score for cohesion is 7.81.\nYou used enough variation of words. You have in between 70'+ 
    ' and 90 percent variation in your text. These are your most used words: "the", "to" and "a".\nYou could use less connectives in your text.' +
    ' You have a percentage of 12 in your text, ideally this would be 9 percent.\nConnectives are words or phrases that link ' +
        'other linguistic units.')
    assert explanations[2].type == 1
    explanationTextStructure = 'This paragraph is too short, try to make paragraphs with approximately 200 words.'
    assert explanations[3].mistakeText == ('So the Turing test might not good test to determine if machines can think, but determine'+
    ' if a machine is programmed well enough to imitate a human being so that it can trick an interrogator into thinking it is conversing'+
    ' with a another human, like with the Google Duplex. ')
    # Check if all information about the style Structure mistake has been added to this database correctly:
    assert explanations[3].explanation == explanationTextStructure
    assert explanations[3].type == 2
    assert explanations[4].mistakeText == ('So the Turing test might not good test to determine if machines can think, but determine'+
    ' if a machine is programmed well enough to imitate a human being so that it can trick an interrogator into thinking it is conversing'+
    ' with a another human, like with the Google Duplex. ')
    assert explanations[4].explanation == explanationTextStructure
    assert explanations[4].type == 2
    assert explanations[5].mistakeText == ('So the Turing test might not good test to determine if machines can think, but determine'+
    ' if a machine is programmed well enough to imitate a human being so that it can trick an interrogator into thinking it is conversing'+
    ' with a another human, like with the Google Duplex. ')
    assert explanations[5].explanation == explanationTextStructure
    assert explanations[5].type == 2
    assert explanations[6].mistakeText == ('C does this by the hand of asking (written) questions. A must try to cause C to make the wrong' + 
        ' identification, while B must try to help C make the right identification (Turing, 1950).')
    assert explanations[6].explanation == explanationTextStructure
    assert explanations[6].type == 2
    assert explanations[7].mistakeText == ('C does this by the hand of asking (written) questions. A must try to cause C to make the wrong' + 
        ' identification, while B must try to help C make the right identification (Turing, 1950).')
    assert explanations[7].explanation == explanationTextStructure
    assert explanations[7].type == 2
    # Check if the coordinates of the structure mistakes have also been found correctly:
    assert page.get_textbox(fitz.Rect(explanations[3].X1, explanations[3].Y1, explanations[3].X2, explanations[3].Y2)) == (
        'So the Turing test might not good test to determine if machines can think, but determine if a machine is programmed well ')
    assert page.get_textbox(fitz.Rect(explanations[4].X1, explanations[4].Y1, explanations[4].X2, explanations[4].Y2)) == (
        'enough to imitate a human being so that it can trick an interrogator into thinking it is conversing with a another human, like ')
    assert page.get_textbox(fitz.Rect(explanations[5].X1, explanations[5].Y1, explanations[5].X2, explanations[5].Y2)) == (
    'with the Google Duplex. ')
    assert page.get_textbox(fitz.Rect(explanations[6].X1, explanations[6].Y1, explanations[6].X2, explanations[6].Y2)) == (
        'C does this by the hand of asking (written) questions. A must try to cause C to make the wrong identification, while B must ')
    assert page.get_textbox(fitz.Rect(explanations[7].X1, explanations[7].Y1, explanations[7].X2, explanations[7].Y2)) == (
        'try to help C make the right identification (Turing, 1950).')
    # Check if the information for the source integration and content mistakes have been added correctly:
    assert explanations[8].mistakeText == ''
    assert explanations[8].explanation == ('Your score for source integration and content is 0. You only used 0 sources in 2 paragraphs of text.' +
    ' Try adding more sources. Writing Dashboard Could not check if text from the sources are actually used in the text.')
    assert explanations[8].type == 3

def loginHelper(testClient, username, password):
    '''
    Support function to log into the server as user with username and password
    and get the access_token
    Arguments:
        testClient:   The test client we test this for.
        username: username of the user we want the access_token from
        password: password of the user we want the access_token from
    Attributes:
        data: data for login
        responseLogin: response from logging in
        access_token: the access token
        responseAccess: response from checking if token is correct
    return:
        access_token: token needed to run locked jwt functions
    '''
    data = {
        'username':username,
        'password':password,
    }
    # Login request
    responseLogin = testClient.post('/loginapi/login', json=data, headers={"Content-Type": "application/json"})
    # Check if we got the correct status code -> login was successfull
    assert responseLogin.status_code == 200
    # Get access token, which we got from login request
    access_token = json.loads(responseLogin.data)['access_token']
    # Request with authorization header containing access token
    responseAccess = testClient.get('/loginapi/protected', headers = {"Authorization": "Bearer " + access_token})
    # Check if we got the correct status code
    assert responseAccess.status_code == 200
    
    return access_token