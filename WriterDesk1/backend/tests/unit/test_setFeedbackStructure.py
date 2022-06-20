from app.feedback.feedback import setFeedbackStructure
from app.models import Files, Explanations
import os
import fitz

def testSetFeedbackStructure(testClient, initDatabase):
    '''
        Test the setFeedbackStructure method from the feedback file in the feedback blueprint. 
        Attributes:
            file: A file which has been added to the database previously, retrieved for the fileId.
            fileId: fileId of this file that has been previously added to the database.
            explanationText: The explanationText we set using the method and check we can retrieve later.
            mistakes: mistakes in the correct format as given to the setFeedbackStructure method. 
            BASEPATH: Path of the current test_setFeedbackStructure.py file.
            fileLoc: Location of the file we test this for.
            explanations: Database for the current file, containing explanations, as retrieved from the database.
            doc: The file opened by fitz.
            page: page of the document as opened by fitz.
        Arguments:
            testClient:  The test client we test this for.
            initDatabase: the database instance we test this for. 
    
    '''
    del testClient, initDatabase
    # Retrieve a fileId that has been currently added to the database:
    file = Files.query.first()
    fileId = file.id
    # Add an explanationText, we look if we can retrieve later:
    explanationText = 'This paragraph is too short, try to make paragraphs with approximately 200 words.'
    # Create a mistakes dictionary, such as it will also be generated by the application later, to add these mistakes to the database:
    mistakes = {
        'Short 1' : explanationText,
        'Short 2' : explanationText
    }
    # The file location on the disk:
    BASEPATH = os.path.abspath(os.path.dirname(__file__))
    fileLoc = os.path.join(BASEPATH, 'testFilesStructure', 'testStructureOnePageTwoMistakesTwoLines.pdf')
    # Make the call to the setFeedbackStructure method:
    setFeedbackStructure(mistakes, fileLoc, fileId)
    # Retrieve this explanation from the database:
    explanations = Explanations.query.filter_by(fileId = fileId).all()
    # Check if all information about this mistake has been added to this database correctly:
    assert explanations[0].mistakeText == 'Short 1'
    assert explanations[0].explanation == explanationText
    assert explanations[0].type == 2
    assert explanations[1].mistakeText == 'Short 2'
    assert explanations[1].explanation == explanationText
    assert explanations[1].type == 2
    # Check if the coordinates of the mistakes have also been found correctly:
    doc = fitz.open(fileLoc)
    page = doc.load_page(0)
    assert page.get_textbox(fitz.Rect(explanations[0].X1, explanations[0].Y1, explanations[0].X2, explanations[0].Y2)) == 'Short 1'
    assert page.get_textbox(fitz.Rect(explanations[1].X1, explanations[1].Y1, explanations[1].X2, explanations[1].Y2)) == 'Short 2'