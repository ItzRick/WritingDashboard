from app.feedback.generateFeedback.StructureFeedback import StructureFeedback
import fitz
import os

def testOnePageZeroMistakes(testClient):
    '''
        Tests if a document that contains no mistakes returns no information
        regarding the mistakes.
        Attributes:
            mistakes: the mistakes on the text.
            BASEPATH: path to the file.
            fileLoc: pointer to the file.
            output: list of information about mistakes generated by the function.
            feedbackObject: Object of the class that generates the feedback for this structure category.
        Arguments:
            testClient:  The test client we test this for.
    '''
    del testClient
    mistakes = {

    }
    BASEPATH = os.path.abspath(os.path.dirname(__file__))
    fileLoc = os.path.join(BASEPATH, 'testFilesStructure', 'testStructureOnePageZeroMistakes.pdf')
    # generate the output on an empty text with no mistakes:
    feedbackObject = StructureFeedback('', '', 1, 1, fileLoc)
    feedbackObject.getMistakesInformationStructure(mistakes)
    output = feedbackObject.explanations
    assert output == []

def testOnePageOneMistakeOneLine(testClient):
    '''
        Tests if a document containing one mistake covering one line in the
        document returns a list containing one element that provides information
        about that mistake.
        Attributes:
            mistakes: the mistakes on the text.
            BASEPATH: path to the file.
            fileLoc: pointer to the file.
            output: list of information about mistakes generated by the function.
            doc: the document opened through the fitz module for reading text.
            page: the first page in the document.
            feedbackObject: Object of the class that generates the feedback for this structure category.
        Arguments:
            testClient:  The test client we test this for.
    '''
    del testClient
    mistakes = {
        'Short 1' : 'This paragraph is too short, try to make paragraphs with approximately 200 words.'
    }
    BASEPATH = os.path.abspath(os.path.dirname(__file__))
    fileLoc = os.path.join(BASEPATH, 'testFilesStructure', 'testStructureOnePageOneMistakeOneLine.pdf')
    # generate the output on a document with one page and one line of text and 
    # one mistake
    feedbackObject = StructureFeedback('', '', 1, 1, fileLoc)
    feedbackObject.getMistakesInformationStructure(mistakes)
    output = feedbackObject.explanations
    # del feedbackObject
    # check if the output contains one list of information
    assert len(output) == 1
    doc = fitz.open(fileLoc)
    page = doc.load_page(0)
    # check if the coordinates enclose the mistake text, the writing skill has
    # number 2, the explanation and corresponding text is correct
    assert page.get_textbox(fitz.Rect(output[0][0], output[0][1], output[0][2], output[0][3])) == 'Short 1'
    assert output[0][4] == 2
    assert output[0][5] == 'This paragraph is too short, try to make paragraphs with approximately 200 words.'
    assert output[0][6] == 'Short 1'

def testOnePageOneMistakeTwoLines(testClient):
    '''
        Tests if a document containing one mistake covering two lines in the
        document returns a list containing two elements. These two elements 
        provide, among other information, the coordinates of each of the lines.
        Attributes:
            mistakes: the mistakes on the text.
            BASEPATH: path to the file.
            fileLoc: pointer to the file.
            output: list of information about mistakes generated by the function.
            doc: the document opened through the fitz module for reading text.
            page: the first page in the document.
            feedbackObject: Object of the class that generates the feedback for this structure category.
        Arguments:
            testClient:  The test client we test this for.
    '''
    del testClient
    mistakes = {
        'Short on 2 lines, short on 2 lines, short on 2 lines, short on 2 lines, short on 2 lines, short on 2 lines, short on 2 lines, short on 2 lines, short on 2 lines.' : 'This paragraph is too short, try to make paragraphs with approximately 200 words.'
    }
    BASEPATH = os.path.abspath(os.path.dirname(__file__))
    fileLoc = os.path.join(BASEPATH, 'testFilesStructure', 'testStructureOnePageOneMistakeTwoLines.pdf')
    # generate the output on a document with one page and two lines of text and 
    # one mistake
    feedbackObject = StructureFeedback('', '', 1, 1, fileLoc)
    feedbackObject.getMistakesInformationStructure(mistakes)
    output = feedbackObject.explanations
    # check if the output contains two lists of information
    assert len(output) == 2
    doc = fitz.open(fileLoc)
    page = doc.load_page(0)
    # check if the coordinates enclose the mistake text, the writing skill has
    # number 2, the explanation and corresponding text is correct
    assert page.get_textbox(fitz.Rect(output[0][0], output[0][1], output[0][2], output[0][3])) == 'Short on 2 lines, short on 2 lines, short on 2 lines, short on 2 lines, short on 2 lines, short on 2 lines, short on 2 lines, short '
    assert page.get_textbox(fitz.Rect(output[1][0], output[1][1], output[1][2], output[1][3])) == 'on 2 lines, short on 2 lines.'
    assert output[0][4] == 2
    assert output[0][5] == 'This paragraph is too short, try to make paragraphs with approximately 200 words.'
    assert output[0][6] == 'Short on 2 lines, short on 2 lines, short on 2 lines, short on 2 lines, short on 2 lines, short on 2 lines, short on 2 lines, short on 2 lines, short on 2 lines.'
    assert output[1][4] == 2
    assert output[1][5] == 'This paragraph is too short, try to make paragraphs with approximately 200 words.'
    assert output[1][6] == 'Short on 2 lines, short on 2 lines, short on 2 lines, short on 2 lines, short on 2 lines, short on 2 lines, short on 2 lines, short on 2 lines, short on 2 lines.'

def testOnePageTwoMistakesOneLine(testClient):
    '''
        Tests if a document containing two mistakes that cover the same line
        returns a list containing two elements. Those elements contain, among
        other information, the coordinates of the text on that single line.
        Attributes:
            mistakes: the mistakes on the text.
            BASEPATH: path to the file.
            fileLoc: pointer to the file.
            output: list of information about mistakes generated by the function.
            doc: the document opened through the fitz module for reading text.
            page: the first page in the document.
            feedbackObject: Object of the class that generates the feedback for this structure category.
        Arguments:
            testClient:  The test client we test this for.
    '''
    del testClient
    mistakes = {
        'Short 1' : 'This paragraph is too short, try to make paragraphs with approximately 200 words.',
        'Short 2' : 'This paragraph is too short, try to make paragraphs with approximately 200 words.'
    }
    BASEPATH = os.path.abspath(os.path.dirname(__file__))
    fileLoc = os.path.join(BASEPATH, 'testFilesStructure', 'testStructureOnePageTwoMistakesOneLine.pdf')
    # generate the output on a document with one page and one line of text and 
    # two mistakes
    feedbackObject = StructureFeedback('', '', 1, 1, fileLoc)
    feedbackObject.getMistakesInformationStructure(mistakes)
    output = feedbackObject.explanations
    # check if the output contains two lists of information
    assert len(output) == 2
    doc = fitz.open(fileLoc)
    page = doc.load_page(0)
    # check if the coordinates enclose the mistake text, the writing skill has
    # number 2, the explanation and corresponding text is correct
    assert page.get_textbox(fitz.Rect(output[0][0], output[0][1], output[0][2], output[0][3])) == 'Short 1'
    assert page.get_textbox(fitz.Rect(output[1][0], output[1][1], output[1][2], output[1][3])) == 'Short 2'
    assert output[0][4] == 2
    assert output[0][5] == 'This paragraph is too short, try to make paragraphs with approximately 200 words.'
    assert output[0][6] == 'Short 1'
    assert output[1][4] == 2
    assert output[1][5] == 'This paragraph is too short, try to make paragraphs with approximately 200 words.'
    assert output[1][6] == 'Short 2'

def testOnePageTwoMistakesTwoLines(testClient):
    '''
        Tests if a document containing two mistakes that cover two lines
        returns a list containing two elements. Those elements contain, among
        other information, the coordinates of the text on each of those lines.
        Attributes:
            mistakes: the mistakes on the text.
            BASEPATH: path to the file.
            fileLoc: pointer to the file.
            output: list of information about mistakes generated by the function.
            doc: the document opened through the fitz module for reading text.
            page: the first page in the document.
            feedbackObject: Object of the class that generates the feedback for this structure category.
        Arguments:
            testClient:  The test client we test this for.
    '''
    del testClient
    mistakes = {
        'Short 1' : 'This paragraph is too short, try to make paragraphs with approximately 200 words.',
        'Short 2' : 'This paragraph is too short, try to make paragraphs with approximately 200 words.'
    }
    BASEPATH = os.path.abspath(os.path.dirname(__file__))
    fileLoc = os.path.join(BASEPATH, 'testFilesStructure', 'testStructureOnePageTwoMistakesTwoLines.pdf')
    # generate the output on a document with one page and two lines of text and 
    # two mistakes
    feedbackObject = StructureFeedback('', '', 1, 1, fileLoc)
    feedbackObject.getMistakesInformationStructure(mistakes)
    output = feedbackObject.explanations
    # check if the output contains two lists of information
    assert len(output) == 2
    doc = fitz.open(fileLoc)
    page = doc.load_page(0)
    # check if the coordinates enclose the mistake text, the writing skill has
    # number 2, the explanation and corresponding text is correct
    assert page.get_textbox(fitz.Rect(output[0][0], output[0][1], output[0][2], output[0][3])) == 'Short 1'
    assert page.get_textbox(fitz.Rect(output[1][0], output[1][1], output[1][2], output[1][3])) == 'Short 2'
    assert output[0][4] == 2
    assert output[0][5] == 'This paragraph is too short, try to make paragraphs with approximately 200 words.'
    assert output[0][6] == 'Short 1'
    assert output[1][4] == 2
    assert output[1][5] == 'This paragraph is too short, try to make paragraphs with approximately 200 words.'
    assert output[1][6] == 'Short 2'

def testTwoPagesOneMistakeOneLine(testClient):
    '''
        Tests if a document with one mistake that covers one line on the second
        page of the document returns a list with one element. That element is a
        list that contains, among other information, the coordinates of the text
        calculated from the height from the first page in the document.
        Attributes:
            mistakes: the mistakes on the text.
            BASEPATH: path to the file.
            fileLoc: pointer to the file.
            output: list of information about mistakes generated by the function.
            doc: the document opened through the fitz module for reading text.
            page: the second page in the document.
            feedbackObject: Object of the class that generates the feedback for this structure category.
        Arguments:
            testClient:  The test client we test this for.
    '''
    del testClient
    mistakes = {
        'Short 1' : 'This paragraph is too short, try to make paragraphs with approximately 200 words.'
    }
    BASEPATH = os.path.abspath(os.path.dirname(__file__))
    fileLoc = os.path.join(BASEPATH, 'testFilesStructure', 'testStructureTwoPageOneMistakeOneLine.pdf')
    # generate the output on a document with two pages and one line of text and 
    # one mistake
    feedbackObject = StructureFeedback('', '', 1, 1, fileLoc)
    feedbackObject.getMistakesInformationStructure(mistakes)
    output = feedbackObject.explanations
    # check if the output contains one list of information
    assert len(output) == 1
    doc = fitz.open(fileLoc)
    page = doc.load_page(1)
    # check if the coordinates enclose the mistake text, the writing skill has
    # number 2, the explanation and corresponding text is correct
    assert page.get_textbox(fitz.Rect(output[0][0], output[0][1] - page.rect.y1, output[0][2], output[0][3] - page.rect.y1)) == 'Short 1'
    assert output[0][4] == 2
    assert output[0][5] == 'This paragraph is too short, try to make paragraphs with approximately 200 words.'
    assert output[0][6] == 'Short 1'

def testTwoPagesOneMistakeTwoLines(testClient):
    '''
        Tests if a document with one mistake that covers two lines on the second
        page of the document returns a list with two elements. Those elements
        are lists that contain, among other information, the coordinates of the 
        mistake text calculated from the height from the first page in the 
        document.
        Attributes:
            mistakes: the mistakes on the text.
            BASEPATH: path to the file.
            fileLoc: pointer to the file.
            output: list of information about mistakes generated by the function.
            doc: the document opened through the fitz module for reading text.
            page: the second page in the document.
            feedbackObject: Object of the class that generates the feedback for this structure category.
        Arguments:
            testClient:  The test client we test this for.
    '''
    del testClient
    mistakes = {
        'Short on 2 lines, short on 2 lines, short on 2 lines, short on 2 lines, short on 2 lines, short on 2 lines, short on 2 lines, short on 2 lines, short on 2 lines.' : 'This paragraph is too short, try to make paragraphs with approximately 200 words.'
    }
    BASEPATH = os.path.abspath(os.path.dirname(__file__))
    fileLoc = os.path.join(BASEPATH, 'testFilesStructure', 'testStructureTwoPagesOneMistakeTwoLines.pdf')
    # generate the output on a document with two pages and two lines of text and 
    # one mistake
    feedbackObject = StructureFeedback('', '', 1, 1, fileLoc)
    feedbackObject.getMistakesInformationStructure(mistakes)
    output = feedbackObject.explanations
    # check if the output contains two lists of information
    assert len(output) == 2
    doc = fitz.open(fileLoc)
    page = doc.load_page(1)
    # check if the coordinates enclose the mistake text, the writing skill has
    # number 2, the explanation and corresponding text is correct
    assert page.get_textbox(fitz.Rect(output[0][0], output[0][1] - page.rect.y1, output[0][2], output[0][3] - page.rect.y1)) == 'Short on 2 lines, short on 2 lines, short on 2 lines, short on 2 lines, short on 2 lines, short on 2 lines, short on 2 lines, short '
    assert page.get_textbox(fitz.Rect(output[1][0], output[1][1] - page.rect.y1, output[1][2], output[1][3] - page.rect.y1)) == 'on 2 lines, short on 2 lines.'
    assert output[0][4] == 2
    assert output[0][5] == 'This paragraph is too short, try to make paragraphs with approximately 200 words.'
    assert output[0][6] == 'Short on 2 lines, short on 2 lines, short on 2 lines, short on 2 lines, short on 2 lines, short on 2 lines, short on 2 lines, short on 2 lines, short on 2 lines.'
    assert output[1][4] == 2
    assert output[1][5] == 'This paragraph is too short, try to make paragraphs with approximately 200 words.'
    assert output[1][6] == 'Short on 2 lines, short on 2 lines, short on 2 lines, short on 2 lines, short on 2 lines, short on 2 lines, short on 2 lines, short on 2 lines, short on 2 lines.'

def testTwoPagesTwoMistakesOneLine(testClient):
    '''
        Tests if a document containing two mistakes that cover the same line on 
        the second page of the document returns a list containing two elements. 
        Those elements contain, among other information, the coordinates of the 
        text on that single line calculated from the height from the first page 
        in the document.
        Attributes:
            mistakes: the mistakes on the text.
            BASEPATH: path to the file.
            fileLoc: pointer to the file.
            output: list of information about mistakes generated by the function.
            doc: the document opened through the fitz module for reading text.
            page: the second page in the document.
            feedbackObject: Object of the class that generates the feedback for this structure category.
        Arguments:
            testClient:  The test client we test this for.
    '''
    del testClient
    mistakes = {
        'Short 1' : 'This paragraph is too short, try to make paragraphs with approximately 200 words.',
        'Short 2' : 'This paragraph is too short, try to make paragraphs with approximately 200 words.'
    }
    BASEPATH = os.path.abspath(os.path.dirname(__file__))
    fileLoc = os.path.join(BASEPATH, 'testFilesStructure', 'testStructureTwoPagesTwoMistakesOneLine.pdf')
    # generate the output on a document with two pages and one line of text and 
    # two mistakes
    feedbackObject = StructureFeedback('', '', 1, 1, fileLoc)
    feedbackObject.getMistakesInformationStructure(mistakes)
    output = feedbackObject.explanations
    # check if the output contains two lists of information
    assert len(output) == 2
    doc = fitz.open(fileLoc)
    page = doc.load_page(1)
    # check if the coordinates enclose the mistake text, the writing skill has
    # number 2, the explanation and corresponding text is correct
    assert page.get_textbox(fitz.Rect(output[0][0], output[0][1] - page.rect.y1, output[0][2], output[0][3] - page.rect.y1)) == 'Short 1'
    assert page.get_textbox(fitz.Rect(output[1][0], output[1][1] - page.rect.y1, output[1][2], output[1][3] - page.rect.y1)) == 'Short 2'
    assert output[0][4] == 2
    assert output[0][5] == 'This paragraph is too short, try to make paragraphs with approximately 200 words.'
    assert output[0][6] == 'Short 1'
    assert output[1][4] == 2
    assert output[1][5] == 'This paragraph is too short, try to make paragraphs with approximately 200 words.'
    assert output[1][6] == 'Short 2'

def testTwoPagesTwoMistakesTwoLines(testClient):
    '''
        Tests if a document containing two mistakes that cover two lines on the
        second page of the document returns a list containing two elements. 
        Those elements contain, among other information, the coordinates of the
        text on each of those lines calculated from the height from the first 
        page in the document.
        Attributes:
            mistakes: the mistakes on the text.
            BASEPATH: path to the file.
            fileLoc: pointer to the file.
            output: list of information about mistakes generated by the function.
            doc: the document opened through the fitz module for reading text.
            page: the second page in the document.
            feedbackObject: Object of the class that generates the feedback for this structure category.
        Arguments:
            testClient:  The test client we test this for.
    '''
    del testClient
    mistakes = {
        'Short 1' : 'This paragraph is too short, try to make paragraphs with approximately 200 words.',
        'Short 2' : 'This paragraph is too short, try to make paragraphs with approximately 200 words.'
    }
    BASEPATH = os.path.abspath(os.path.dirname(__file__))
    fileLoc = os.path.join(BASEPATH, 'testFilesStructure', 'testStructureTwoPagesTwoMistakesTwoLines.pdf')
    # generate the output on a document with two pages and two lines of text and 
    # two mistakes
    feedbackObject = StructureFeedback('', '', 1, 1, fileLoc)
    feedbackObject.getMistakesInformationStructure(mistakes)
    output = feedbackObject.explanations
    # check if the output contains two lists of information
    assert len(output) == 2
    doc = fitz.open(fileLoc)
    page = doc.load_page(1)
    # check if the coordinates enclose the mistake text, the writing skill has
    # number 2, the explanation and corresponding text is correct
    assert page.get_textbox(fitz.Rect(output[0][0], output[0][1] - page.rect.y1, output[0][2], output[0][3] - page.rect.y1)) == 'Short 1'
    assert page.get_textbox(fitz.Rect(output[1][0], output[1][1] - page.rect.y1, output[1][2], output[1][3] - page.rect.y1)) == 'Short 2'
    assert output[0][4] == 2
    assert output[0][5] == 'This paragraph is too short, try to make paragraphs with approximately 200 words.'
    assert output[0][6] == 'Short 1'
    assert output[1][4] == 2
    assert output[1][5] == 'This paragraph is too short, try to make paragraphs with approximately 200 words.'
    assert output[1][6] == 'Short 2'

def testTeXFile(testClient):
    '''
        Tests if a TeX document with one mistake that covers one line on the 
        second page of the document returns a list with one element. That 
        element is a list that contains, among other information, the 
        coordinates of the text calculated from the height from the first page 
        in the document.
        Attributes:
            mistakes: the mistakes on the text.
            BASEPATH: path to the file.
            fileLoc: pointer to the file.
            output: list of information about mistakes generated by the function.
            doc: the document opened through the fitz module for reading text.
            page: the second page in the document.
            feedbackObject: Object of the class that generates the feedback for this structure category.
        Arguments:
            testClient:  The test client we test this for.
    '''
    del testClient
    mistakes = {
        'Short 1' : 'This paragraph is too short, try to make paragraphs with approximately 200 words.'
    }
    BASEPATH = os.path.abspath(os.path.dirname(__file__))
    fileLoc = os.path.join(BASEPATH, 'testFilesStructure', 'testTeXFile.pdf')
    # generate the output on a document with two pages and one line of text and 
    # one mistake
    feedbackObject = StructureFeedback('', '', 1, 1, fileLoc)
    feedbackObject.getMistakesInformationStructure(mistakes)
    output = feedbackObject.explanations
    # check if the output contains one list of information
    assert len(output) == 1
    doc = fitz.open(fileLoc)
    page = doc.load_page(1)
    # check if the coordinates enclose the mistake text, the writing skill has
    # number 2, the explanation and corresponding text is correct
    assert page.get_textbox(fitz.Rect(output[0][0], output[0][1] - page.rect.y1 * 0.999, output[0][2], output[0][3] - page.rect.y1 * 0.999)) == 'Short 1'
    assert output[0][4] == 2
    assert output[0][5] == 'This paragraph is too short, try to make paragraphs with approximately 200 words.'
    assert output[0][6] == 'Short 1'