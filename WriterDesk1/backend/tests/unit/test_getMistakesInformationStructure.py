from app.getMistakesInformation import getMistakesInformationStructure
import fitz
import os

def testOnePageZeroMistakes():
    '''
        Tests if a document that contains no mistakes returns no information
        regarding the mistakes.
    '''
    mistakes = {

    }
    BASEPATH = os.path.abspath(os.path.dirname(__file__))
    fileLoc = os.path.join(BASEPATH, 'testFilesStructure', 'testStructureOnePageZeroMistakes.pdf')
    output = getMistakesInformationStructure(mistakes, fileLoc)
    assert output == []

def testOnePageOneMistakeOneLine():
    '''
        Tests if a document containing one mistake covering one line in the
        document returns a list containing one element that provides information
        about that mistake.
    '''
    mistakes = {
        'Short 1' : 'This paragraph is too short, try to make paragraphs with more words.'
    }
    BASEPATH = os.path.abspath(os.path.dirname(__file__))
    fileLoc = os.path.join(BASEPATH, 'testFilesStructure', 'testStructureOnePageOneMistakeOneLine.pdf')
    output = getMistakesInformationStructure(mistakes, fileLoc)
    assert len(output) == 1
    doc = fitz.open(fileLoc)
    page = doc.load_page(0)
    assert page.get_textbox(fitz.Rect(output[0][0], output[0][1], output[0][2], output[0][3])) == 'Short 1'
    assert output[0][4] == 2
    assert output[0][5] == 'This paragraph is too short, try to make paragraphs with more words.'
    assert output[0][6] == 'Short 1'

def testOnePageOneMistakeTwoLines():
    '''
        Tests if a document containing one mistake covering two lines in the
        document returns a list containing two elements. These two elements 
        provide, among other information, the coordinates of each of the lines.
    '''
    mistakes = {
        'Short on 2 lines, short on 2 lines, short on 2 lines, short on 2 lines, short on 2 lines, short on 2 lines, short on 2 lines, short on 2 lines, short on 2 lines.' : 'This paragraph is too short, try to make paragraphs with more words.'
    }
    BASEPATH = os.path.abspath(os.path.dirname(__file__))
    fileLoc = os.path.join(BASEPATH, 'testFilesStructure', 'testStructureOnePageOneMistakeTwoLines.pdf')
    output = getMistakesInformationStructure(mistakes, fileLoc)
    assert len(output) == 2
    doc = fitz.open(fileLoc)
    page = doc.load_page(0)
    assert page.get_textbox(fitz.Rect(output[0][0], output[0][1], output[0][2], output[0][3])) == 'Short on 2 lines, short on 2 lines, short on 2 lines, short on 2 lines, short on 2 lines, short on 2 lines, short on 2 lines, short '
    assert page.get_textbox(fitz.Rect(output[1][0], output[1][1], output[1][2], output[1][3])) == 'on 2 lines, short on 2 lines.'
    assert output[0][4] == 2
    assert output[0][5] == 'This paragraph is too short, try to make paragraphs with more words.'
    assert output[0][6] == 'Short on 2 lines, short on 2 lines, short on 2 lines, short on 2 lines, short on 2 lines, short on 2 lines, short on 2 lines, short on 2 lines, short on 2 lines.'
    assert output[1][4] == 2
    assert output[1][5] == 'This paragraph is too short, try to make paragraphs with more words.'
    assert output[1][6] == 'Short on 2 lines, short on 2 lines, short on 2 lines, short on 2 lines, short on 2 lines, short on 2 lines, short on 2 lines, short on 2 lines, short on 2 lines.'

def testOnePageTwoMistakesOneLine():
    '''
        Tests if a document containing two mistakes that cover the same line
        returns a list containing two elements. Those elements contain, among
        other information, the coordinates of the text on that single line.
    '''
    mistakes = {
        'Short 1' : 'This paragraph is too short, try to make paragraphs with more words.',
        'Short 2' : 'This paragraph is too short, try to make paragraphs with more words.'
    }
    BASEPATH = os.path.abspath(os.path.dirname(__file__))
    fileLoc = os.path.join(BASEPATH, 'testFilesStructure', 'testStructureOnePageTwoMistakesOneLine.pdf')
    output = getMistakesInformationStructure(mistakes, fileLoc)
    assert len(output) == 2
    doc = fitz.open(fileLoc)
    page = doc.load_page(0)
    assert page.get_textbox(fitz.Rect(output[0][0], output[0][1], output[0][2], output[0][3])) == 'Short 1'
    assert page.get_textbox(fitz.Rect(output[1][0], output[1][1], output[1][2], output[1][3])) == 'Short 2'
    assert output[0][4] == 2
    assert output[0][5] == 'This paragraph is too short, try to make paragraphs with more words.'
    assert output[0][6] == 'Short 1'
    assert output[1][4] == 2
    assert output[1][5] == 'This paragraph is too short, try to make paragraphs with more words.'
    assert output[1][6] == 'Short 2'

def testOnePageTwoMistakesTwoLines():
    '''
        Tests if a document containing two mistakes that cover two lines
        returns a list containing two elements. Those elements contain, among
        other information, the coordinates of the text on each of those lines.
    '''
    mistakes = {
        'Short 1' : 'This paragraph is too short, try to make paragraphs with more words.',
        'Short 2' : 'This paragraph is too short, try to make paragraphs with more words.'
    }
    BASEPATH = os.path.abspath(os.path.dirname(__file__))
    fileLoc = os.path.join(BASEPATH, 'testFilesStructure', 'testStructureOnePageTwoMistakesTwoLines.pdf')
    output = getMistakesInformationStructure(mistakes, fileLoc)
    assert len(output) == 2
    doc = fitz.open(fileLoc)
    page = doc.load_page(0)
    assert page.get_textbox(fitz.Rect(output[0][0], output[0][1], output[0][2], output[0][3])) == 'Short 1'
    assert page.get_textbox(fitz.Rect(output[1][0], output[1][1], output[1][2], output[1][3])) == 'Short 2'
    assert output[0][4] == 2
    assert output[0][5] == 'This paragraph is too short, try to make paragraphs with more words.'
    assert output[0][6] == 'Short 1'
    assert output[1][4] == 2
    assert output[1][5] == 'This paragraph is too short, try to make paragraphs with more words.'
    assert output[1][6] == 'Short 2'

def testTwoPagesOneMistakeOneLine():
    '''
        Tests if a document with one mistake that covers one line on the second
        page of the document returns a list with one element. That element is a
        list that contains, among other information, the coordinates of the text
        calculated from the height from the first page in the document.
    '''
    mistakes = {
        'Short 1' : 'This paragraph is too short, try to make paragraphs with more words.'
    }
    BASEPATH = os.path.abspath(os.path.dirname(__file__))
    fileLoc = os.path.join(BASEPATH, 'testFilesStructure', 'testStructureTwoPageOneMistakeOneLine.pdf')
    output = getMistakesInformationStructure(mistakes, fileLoc)
    assert len(output) == 1
    doc = fitz.open(fileLoc)
    page = doc.load_page(1)
    assert page.get_textbox(fitz.Rect(output[0][0], output[0][1] - page.rect.y1, output[0][2], output[0][3] - page.rect.y1)) == 'Short 1'
    assert output[0][4] == 2
    assert output[0][5] == 'This paragraph is too short, try to make paragraphs with more words.'
    assert output[0][6] == 'Short 1'

def testTwoPagesOneMistakeTwoLines():
    '''
        Tests if a document with one mistake that covers two lines on the second
        page of the document returns a list with two elements. Those elements
        are lists that contain, among other information, the coordinates of the 
        mistake text calculated from the height from the first page in the 
        document.
    '''
    mistakes = {
        'Short on 2 lines, short on 2 lines, short on 2 lines, short on 2 lines, short on 2 lines, short on 2 lines, short on 2 lines, short on 2 lines, short on 2 lines.' : 'This paragraph is too short, try to make paragraphs with more words.'
    }
    BASEPATH = os.path.abspath(os.path.dirname(__file__))
    fileLoc = os.path.join(BASEPATH, 'testFilesStructure', 'testStructureTwoPagesOneMistakeTwoLines.pdf')
    output = getMistakesInformationStructure(mistakes, fileLoc)
    assert len(output) == 2
    doc = fitz.open(fileLoc)
    page = doc.load_page(1)
    assert page.get_textbox(fitz.Rect(output[0][0], output[0][1] - page.rect.y1, output[0][2], output[0][3] - page.rect.y1)) == 'Short on 2 lines, short on 2 lines, short on 2 lines, short on 2 lines, short on 2 lines, short on 2 lines, short on 2 lines, short '
    assert page.get_textbox(fitz.Rect(output[1][0], output[1][1] - page.rect.y1, output[1][2], output[1][3] - page.rect.y1)) == 'on 2 lines, short on 2 lines.'
    assert output[0][4] == 2
    assert output[0][5] == 'This paragraph is too short, try to make paragraphs with more words.'
    assert output[0][6] == 'Short on 2 lines, short on 2 lines, short on 2 lines, short on 2 lines, short on 2 lines, short on 2 lines, short on 2 lines, short on 2 lines, short on 2 lines.'
    assert output[1][4] == 2
    assert output[1][5] == 'This paragraph is too short, try to make paragraphs with more words.'
    assert output[1][6] == 'Short on 2 lines, short on 2 lines, short on 2 lines, short on 2 lines, short on 2 lines, short on 2 lines, short on 2 lines, short on 2 lines, short on 2 lines.'

def testTwoPagesTwoMistakesOneLine():
    '''
        Tests if a document containing two mistakes that cover the same line on 
        the second page of the document returns a list containing two elements. 
        Those elements contain, among other information, the coordinates of the 
        text on that single line calculated from the height from the first page 
        in the document.
    '''
    mistakes = {
        'Short 1' : 'This paragraph is too short, try to make paragraphs with more words.',
        'Short 2' : 'This paragraph is too short, try to make paragraphs with more words.'
    }
    BASEPATH = os.path.abspath(os.path.dirname(__file__))
    fileLoc = os.path.join(BASEPATH, 'testFilesStructure', 'testStructureTwoPagesTwoMistakesOneLine.pdf')
    output = getMistakesInformationStructure(mistakes, fileLoc)
    assert len(output) == 2
    doc = fitz.open(fileLoc)
    page = doc.load_page(1)
    assert page.get_textbox(fitz.Rect(output[0][0], output[0][1] - page.rect.y1, output[0][2], output[0][3] - page.rect.y1)) == 'Short 1'
    assert page.get_textbox(fitz.Rect(output[1][0], output[1][1] - page.rect.y1, output[1][2], output[1][3] - page.rect.y1)) == 'Short 2'
    assert output[0][4] == 2
    assert output[0][5] == 'This paragraph is too short, try to make paragraphs with more words.'
    assert output[0][6] == 'Short 1'
    assert output[1][4] == 2
    assert output[1][5] == 'This paragraph is too short, try to make paragraphs with more words.'
    assert output[1][6] == 'Short 2'

def testTwoPagesTwoMistakesTwoLines():
    '''
        Tests if a document containing two mistakes that cover two lines on the
        second page of the document returns a list containing two elements. 
        Those elements contain, among other information, the coordinates of the
        text on each of those lines calculated from the height from the first 
        page in the document.
    '''
    mistakes = {
        'Short 1' : 'This paragraph is too short, try to make paragraphs with more words.',
        'Short 2' : 'This paragraph is too short, try to make paragraphs with more words.'
    }
    BASEPATH = os.path.abspath(os.path.dirname(__file__))
    fileLoc = os.path.join(BASEPATH, 'testFilesStructure', 'testStructureTwoPagesTwoMistakesTwoLines.pdf')
    output = getMistakesInformationStructure(mistakes, fileLoc)
    assert len(output) == 2
    doc = fitz.open(fileLoc)
    page = doc.load_page(1)
    assert page.get_textbox(fitz.Rect(output[0][0], output[0][1] - page.rect.y1, output[0][2], output[0][3] - page.rect.y1)) == 'Short 1'
    assert page.get_textbox(fitz.Rect(output[1][0], output[1][1] - page.rect.y1, output[1][2], output[1][3] - page.rect.y1)) == 'Short 2'
    assert output[0][4] == 2
    assert output[0][5] == 'This paragraph is too short, try to make paragraphs with more words.'
    assert output[0][6] == 'Short 1'
    assert output[1][4] == 2
    assert output[1][5] == 'This paragraph is too short, try to make paragraphs with more words.'
    assert output[1][6] == 'Short 2'