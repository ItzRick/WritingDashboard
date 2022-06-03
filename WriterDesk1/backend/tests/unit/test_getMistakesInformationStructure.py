from app.getMistakesInformation import getMistakesInformationStructure
import fitz
import os

def testOnePageZeroMistakes():
    mistakes = {

    }
    BASEPATH = os.path.abspath(os.path.dirname(__file__))
    fileLoc = os.path.join(BASEPATH, 'testFilesStructure', 'testStructureOnePageZeroMistakes.pdf')
    output = getMistakesInformationStructure(mistakes, fileLoc)
    assert output == []

def testOnePageOneMistakeOneLine():
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