from app.feedback.feedback import genFeedback
from app.models import Files, Explanations, User, Scores
from app.scoreapi.scores import setScoreDB, getCurrentExplanationVersion
from datetime import date
import os
import fitz

def uploadFile(fileName, testClient):
    '''
        Upload a file to the server, for later use testing the genFeedback method.
        Arguments: 
            fileName: Filename in the location of this testfile we upload.
            testClient: The test client we test this for.
        Attributes: 
            user: A user which has been added to the database.
            BASEDIR: Directory the test_genFeedback.py file is located inside. 
            fileDir: The path to the actual file we upload. 
            data: Data to upload this file with. 
            response: Response after the ai call.
            file: Database instance of the file we have uploaded. 
    '''
    user = User.query.first()
    # Get the BASEDIR and set the fileDir with that:
    BASEDIR = os.path.abspath(os.path.dirname(__file__))
    fileDir = os.path.join(BASEDIR, fileName)
    # Create the data packet:
    data = {
        'files': (open(fileDir, 'rb'), fileName),
        'fileName': fileName,
        'userId': user.id,
        'courseCode': '',
        'date': date(2022, 5, 11)
    }
    # Create the response by means of the post request:
    response = testClient.post('/fileapi/upload', data=data)
    assert response.status_code == 200
    file = Files.query.filter_by(filename=fileName).first()
    return file

def testGenFeedbackNoFile(testClient, initDatabase):
    '''
        Test if we upload a file instance, without a file on the disk, we indeed get returned false 
        and indeed get returned an error message. 
        Arguments:
            testClient:  The test client we test this for.
            initDatabase: the database instance we test this for. 
        Attributes:     
            file: A file instance of the database, as previously uploaded to said database.
            isSuccesful: True if the feedback has been correctly generated, False otherwise.
            message: Message if we get an exception during execution of the method.
    '''
    del testClient, initDatabase
    # Get a file instance from the database:
    file = Files.query.first()
    # Call the genFeedback method and check if we get the correct info returned:
    isSuccessful, message = genFeedback(file)
    assert not isSuccessful
    assert 'no such file' in message

def testGenFeedbackAlreadyUploaded(testClient, initDatabase):
    '''
        Test the genFeedback method, for if we have already generated feedback for this file.
        That is, if we have generated feedback with a more recent version or the current version 
        of the feedback model.
        Arguments:
            testClient:  The test client we test this for.
            initDatabase: the database instance we test this for. 
        Attributes:     
            file: A file instance of the database, as previously uploaded to said database.
            isSuccesful: True if the feedback has been correctly generated, False otherwise.
            message: Message if we get an exception during execution of the method.
    '''
    del initDatabase
    # Get a file instance from the database:
    file = uploadFile('testfeedback.pdf', testClient)
    setScoreDB(file.id, 0, 0, 0, 0, 2)

    # Call the genFeedback method and check if we get the correct info returned:
    isSuccessful, message = genFeedback(file)
    assert not isSuccessful
    assert 'Feedback has already been generated!' in message

def testGenFeedbackDocxFile(testClient, initDatabase):
    ''' 
        Test the genFeedback method for a docx file.
        Attributes:
            file: A file which has been added to uploaded to the application using the uploadFile method.
            isSuccessful: Boolean retrieved from the uploadFile method to indicate if we have correctly calculated the score.
            score: scores as retrieved from the database after running the genFeedback method.
            fileId: fileId of this file that has been previously added to the database.
            mistakes: mistakes in the correct format as given to the setFeedbackStyle method. 
            BASEPATH: Path of the current test_setFeedbackStyle.py file.
            fileLoc: Location of the file we test this for.
            convertedFileLoc: pointer to the pdf file that is created by converting this docx file.
            head: The head of the filePath of the file for which the feedback will be generated.
            tail: The tail of the filepath of the file for which the feedback will be generated.
            explanations: Database for the current file, containing explanations, as retrieved from the database 
                and created using the genFeedback method.
        Arguments:
            testClient:  The test client we test this for.
            initDatabase: the database instance we test this for. 
    '''
    del initDatabase
    # Upload the file to the application:
    file = uploadFile('testfeedbackdocx.docx', testClient)
    # Generate the feedback:
    isSuccessful = genFeedback(file)
    assert isSuccessful[0]
    # Check if we have added the correct score to the database:
    score = Scores.query.filter_by(fileId=file.id).first()
    assert float(score.scoreStyle) == 8.40
    assert float(score.scoreCohesion) == 8.03
    assert float(score.scoreStructure) == 6.5
    assert float(score.scoreIntegration) == 0.0
    # Get all explanations for this file from the database.
    explanations = Explanations.query.filter_by(fileId = file.id).all()
    # Check if the correct number of explanations has been added to the database:
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
    head, tail = os.path.split(file.path)
    convertedFileLoc = os.path.join(head, 'converted', tail.replace(".docx", ".pdf"))
    doc = fitz.open(convertedFileLoc)
    page = doc.load_page(0)
    assert page.get_textbox(fitz.Rect(explanations[0].X1, explanations[0].Y1, explanations[0].X2, explanations[0].Y2)) == 'a'
    assert page.get_textbox(fitz.Rect(explanations[1].X1, explanations[1].Y1, explanations[1].X2, explanations[1].Y2)) == 'must try'
    # Check if all information for the Cohesion writing structures has been added to the database:
    assert explanations[2].mistakeText == ''
    assert explanations[2].explanation == ('Your score for cohesion is 8.03.\nYou used enough variation of words. You have in between 70'+ 
    ' and 90 percent variation in your text. These are your most used words: "the", "to" and "a".\nYou could use less connectives in your text.' +
    ' You have a percentage of 12 in your text, ideally this would be 9 percent.\nConnectives are words or phrases that link ' +
        'other linguistic units.')
    assert explanations[2].type == 1
    assert explanations[3].mistakeText == ('So the Turing test might not good test to determine if machines can think, but determine'+
    ' if a machine is programmed well enough to imitate a human being so that it can trick an interrogator into thinking it is conversing'+
    ' with a another human, like with the Google Duplex. ')
    # Check if all information about the style Structure mistake has been added to this database correctly:
    explanationTextStructure = 'This paragraph is too short, try to make paragraphs with approximately 200 words.'
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
        'So the Turing test might not good test to determine if machines can think, but determine if a ')
    assert page.get_textbox(fitz.Rect(explanations[4].X1, explanations[4].Y1, explanations[4].X2, explanations[4].Y2)) == (
        'machine is programmed well enough to imitate a human being so that it can trick an ')
    assert page.get_textbox(fitz.Rect(explanations[5].X1, explanations[5].Y1, explanations[5].X2, explanations[5].Y2)) == (
        'interrogator into thinking it is conversing with a another human, like with the Google Duplex. ')
    assert page.get_textbox(fitz.Rect(explanations[6].X1, explanations[6].Y1, explanations[6].X2, explanations[6].Y2)) == (
        'C does this by the hand of asking (written) questions. A must try to cause C to make the ')
    assert page.get_textbox(fitz.Rect(explanations[7].X1, explanations[7].Y1, explanations[7].X2, explanations[7].Y2)) == (
        'wrong identification, while B must try to help C make the right identification (Turing, 1950).')
    # Check if the information for the source integration and content mistakes have been added correctly:
    assert explanations[8].mistakeText == ''
    assert explanations[8].explanation == ('Your score for source integration and content is 0. You only used 0 sources in 2 paragraphs of text.' +
    ' Try adding more sources. Writing Dashboard Could not check if text from the sources are actually used in the text.')
    assert explanations[8].type == 3

def testGenFeedbackPdfFile(testClient, initDatabase):
    ''' 
        Test the genFeedback method for a pdf file.
        Attributes:
            file: A file which has been added to uploaded to the application using the uploadFile method.
            isSuccessful: Boolean retrieved from the uploadFile method to indicate if we have correctly calculated the score.
            score: scores as retrieved from the database after running the genFeedback method.
            fileId: fileId of this file that has been previously added to the database.
            mistakes: mistakes in the correct format as given to the setFeedbackStyle method. 
            BASEPATH: Path of the current test_setFeedbackStyle.py file.
            fileLoc: Location of the file we test this for.
            explanations: Database for the current file, containing explanations, as retrieved from the database 
                and created using the genFeedback method.
        Arguments:
            testClient:  The test client we test this for.
            initDatabase: the database instance we test this for. 
    '''
    del initDatabase
    # Upload the file to the application:
    file = uploadFile('testfeedback.pdf', testClient)
    # Generate the feedback:
    isSuccessful = genFeedback(file)
    assert isSuccessful[0]
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
    # Check if all information fro the cohesion writing skill has been added to the database correctly:
    assert explanations[2].mistakeText == ''
    assert explanations[2].explanation == ('Your score for cohesion is 7.81.\nYou used enough variation of words. You have in between 70'+ 
    ' and 90 percent variation in your text. These are your most used words: "the", "to" and "a".\nYou could use less connectives in your text.' +
    ' You have a percentage of 12 in your text, ideally this would be 9 percent.\nConnectives are words or phrases that link ' +
        'other linguistic units.')
    assert explanations[2].type == 1
    # Check if all information about the Structure mistake has been added to this database correctly:
    explanationTextStructure = 'This paragraph is too short, try to make paragraphs with approximately 200 words.'
    assert explanations[3].mistakeText == ('So the Turing test might not good test to determine if machines can think, but determine'+
    ' if a machine is programmed well enough to imitate a human being so that it can trick an interrogator into thinking it is conversing'+
    ' with a another human, like with the Google Duplex. ')
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

def testGenFeedbackTxtFile(testClient, initDatabase):
    ''' 
        Test the genFeedback method for a txt file.
        Attributes:
            file: A file which has been added to uploaded to the application using the uploadFile method.
            isSuccessful: Boolean retrieved from the uploadFile method to indicate if we have correctly calculated the score.
            score: scores as retrieved from the database after running the genFeedback method.
            fileId: fileId of this file that has been previously added to the database.
            mistakes: mistakes in the correct format as given to the setFeedbackStyle method. 
            BASEPATH: Path of the current test_setFeedbackStyle.py file.
            fileLoc: Location of the file we test this for.
            convertedFileLoc: pointer to the pdf file that is created by converting this docx file.
            head: The head of the filePath of the file for which the feedback will be generated.
            tail: The tail of the filepath of the file for which the feedback will be generated.
            explanations: Database for the current file, containing explanations, as retrieved from the database 
                and created using the genFeedback method.
        Arguments:
            testClient:  The test client we test this for.
            initDatabase: the database instance we test this for. 
    '''
    del initDatabase
    # Upload the file to the application:
    file = uploadFile('testfeedbacktxt.txt', testClient)
    # Generate the feedback:
    isSuccessful = genFeedback(file)
    assert isSuccessful[0]
    # Check if we have added the correct score to the database:
    score = Scores.query.filter_by(fileId=file.id).first()
    assert float(score.scoreStyle) == 8.40
    assert float(score.scoreCohesion) == 8.03
    assert float(score.scoreStructure) == 6.5
    assert float(score.scoreIntegration) == 0.0
    # Get all explanations for this file from the database.
    explanations = Explanations.query.filter_by(fileId = file.id).all()
    # Check if the correct number of explanations has been uploaded to the database:
    assert len(explanations) == 11
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
    head, tail = os.path.split(file.path)
    convertedFileLoc = os.path.join(head, 'converted', tail.replace(".txt", ".pdf"))
    doc = fitz.open(convertedFileLoc)
    page = doc.load_page(0)
    assert page.get_textbox(fitz.Rect(explanations[0].X1, explanations[0].Y1, explanations[0].X2, explanations[0].Y2)) == 'a'
    assert page.get_textbox(fitz.Rect(explanations[1].X1, explanations[1].Y1, explanations[1].X2, explanations[1].Y2)) == 'must try'
    # Check if the correct information for the Cohesion writing skill has been added to the database:
    assert explanations[2].mistakeText == ''
    assert explanations[2].explanation == ('Your score for cohesion is 8.03.\nYou used enough variation of words. You have in between 70'+ 
    ' and 90 percent variation in your text. These are your most used words: "the", "to" and "a".\nYou could use less connectives in your text.' +
    ' You have a percentage of 12 in your text, ideally this would be 9 percent.\nConnectives are words or phrases that link ' +
        'other linguistic units.')
    assert explanations[2].type == 1
    explanationTextStructure = 'This paragraph is too short, try to make paragraphs with approximately 200 words.'
    assert explanations[3].mistakeText == ('So the Turing test might not good test to determine if machines can think, but determine'+
    ' if a machine is programmed well enough to imitate a human being so that it can trick an interrogator into thinking it is conversing'+
    ' with a another human, like with the Google Duplex.')
    # Check if all information about the style Structure mistake has been added to this database correctly:
    assert explanations[3].explanation == explanationTextStructure
    assert explanations[3].type == 2
    assert explanations[4].mistakeText == ('So the Turing test might not good test to determine if machines can think, but determine'+
    ' if a machine is programmed well enough to imitate a human being so that it can trick an interrogator into thinking it is conversing'+
    ' with a another human, like with the Google Duplex.')
    assert explanations[4].explanation == explanationTextStructure
    assert explanations[4].type == 2
    assert explanations[5].mistakeText == ('So the Turing test might not good test to determine if machines can think, but determine'+
    ' if a machine is programmed well enough to imitate a human being so that it can trick an interrogator into thinking it is conversing'+
    ' with a another human, like with the Google Duplex.')
    assert explanations[5].explanation == explanationTextStructure
    assert explanations[5].type == 2
    assert explanations[6].mistakeText == ('So the Turing test might not good test to determine if machines can think, but determine'+
    ' if a machine is programmed well enough to imitate a human being so that it can trick an interrogator into thinking it is conversing'+
    ' with a another human, like with the Google Duplex.')
    assert explanations[6].explanation == explanationTextStructure
    assert explanations[6].type == 2
    assert explanations[7].mistakeText == ('C does this by the hand of asking (written) questions. A must try to cause C to make the wrong' + 
        ' identification, while B must try to help C make the right identification (Turing, 1950).')
    assert explanations[7].explanation == explanationTextStructure
    assert explanations[7].type == 2
    assert explanations[8].mistakeText == ('C does this by the hand of asking (written) questions. A must try to cause C to make the wrong' + 
        ' identification, while B must try to help C make the right identification (Turing, 1950).')
    assert explanations[8].explanation == explanationTextStructure
    assert explanations[8].type == 2
    assert explanations[9].mistakeText == ('C does this by the hand of asking (written) questions. A must try to cause C to make the wrong' + 
        ' identification, while B must try to help C make the right identification (Turing, 1950).')
    assert explanations[9].explanation == explanationTextStructure
    assert explanations[9].type == 2
    # Check if the coordinates of the structure mistakes have also been found correctly:
    assert page.get_textbox(fitz.Rect(explanations[3].X1, explanations[3].Y1, explanations[3].X2, explanations[3].Y2)) == (
        'So the Turing test might not good test to determine if machines can think, but')
    assert page.get_textbox(fitz.Rect(explanations[4].X1, explanations[4].Y1, explanations[4].X2, explanations[4].Y2)) == (
        'determine if a machine is programmed well enough to imitate a human being so')
    assert page.get_textbox(fitz.Rect(explanations[5].X1, explanations[5].Y1, explanations[5].X2, explanations[5].Y2)) == (
        'that it can trick an interrogator into thinking it is conversing with a another')
    assert page.get_textbox(fitz.Rect(explanations[6].X1, explanations[6].Y1, explanations[6].X2, explanations[6].Y2)) == (
        'human, like with the Google Duplex.')
    assert page.get_textbox(fitz.Rect(explanations[7].X1, explanations[7].Y1, explanations[7].X2, explanations[7].Y2)) == (
        'C does this by the hand of asking (written) questions. A must try to cause C to')
    assert page.get_textbox(fitz.Rect(explanations[8].X1, explanations[8].Y1, explanations[8].X2, explanations[8].Y2)) == (
        'make the wrong identification, while B must try to help C make the right')
    assert page.get_textbox(fitz.Rect(explanations[9].X1, explanations[9].Y1, explanations[9].X2, explanations[9].Y2)) == (
        'identification (Turing, 1950).')
    # Check if the information for the source integration and content mistakes have been added correctly:
    assert explanations[10].mistakeText == ''
    assert explanations[10].explanation == ('Your score for source integration and content is 0. You only used 0 sources in 2 paragraphs of text.' +
    ' Try adding more sources. Writing Dashboard Could not check if text from the sources are actually used in the text.')
    assert explanations[10].type == 3