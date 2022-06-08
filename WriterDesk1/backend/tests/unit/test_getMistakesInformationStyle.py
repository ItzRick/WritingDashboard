from app.getMistakesInformation import getMistakesInformationStyle
import fitz
import os

def testOnePageZeroMistakes():
    '''
        Tests if a document that contains no mistakes returns no information
        regarding the mistakes.
    '''
    mistakes = ([], 10.0)
    BASEPATH = os.path.abspath(os.path.dirname(__file__))
    fileLoc = os.path.join(BASEPATH, 'testFilesStyle', 'testStyleOnePageZeroMistakes.pdf')
    output = getMistakesInformationStyle(mistakes, fileLoc)
    assert output == []

def testOnePageOneMistake():
    '''
        Tests if a document containing one mistake returns a list containing one
        element that provides information about that mistake.
    '''
    mistakes = ([
        ['a', 'tor into thinking it is conversing with a another human, like with the Google Dup',
         0, 'Use "an" instead of "a" if the following word starts with a vowel sound, e.g. "an article", "an hour".',
         ['an']
        ]
    ], 9.6)
    BASEPATH = os.path.abspath(os.path.dirname(__file__))
    fileLoc = os.path.join(BASEPATH, 'testFilesStyle', 'testStyleOnePageOneMistake.pdf')
    output = getMistakesInformationStyle(mistakes, fileLoc)
    assert len(output) == 1
    doc = fitz.open(fileLoc)
    page = doc.load_page(0)
    assert page.get_textbox(fitz.Rect(output[0][0], output[0][1], output[0][2], output[0][3])) == 'a'
    assert output[0][4] == 0
    assert output[0][5] == 'Use "an" instead of "a" if the following word starts with a vowel sound, e.g. "an article", "an hour".'
    assert output[0][6] == 'a'
    assert output[0][7] == ['an']

def testOnePageTwoMistakes():
    '''
        Tests if a document containing two mistakes returns a list containing 
        two elements. Those elements contain, among other information, the 
        coordinates of the mistakes text.
    '''
    mistakes = ([
        ['a', 'tor into thinking it is conversing with a another human, like with the Google Dup',
         0, 'Use "an" instead of "a" if the following word starts with a vowel sound, e.g. "an article", "an hour".',
         ['an']
        ],
        ['must try', 'e hand of asking (written) questions. A must try to cause C to make the wrong identifica',
         0, 'It appears that a hyphen is missing in this expression.', ['must-try']
        ]
    ], 9.6)
    BASEPATH = os.path.abspath(os.path.dirname(__file__))
    fileLoc = os.path.join(BASEPATH, 'testFilesStyle', 'testStyleOnePageTwoMistakes.pdf')
    output = getMistakesInformationStyle(mistakes, fileLoc)
    assert len(output) == 2
    doc = fitz.open(fileLoc)
    page = doc.load_page(0)
    assert page.get_textbox(fitz.Rect(output[0][0], output[0][1], output[0][2], output[0][3])) == 'a'
    assert page.get_textbox(fitz.Rect(output[1][0], output[1][1], output[1][2], output[1][3])) == 'must try'
    assert output[0][4] == 0
    assert output[0][5] == 'Use "an" instead of "a" if the following word starts with a vowel sound, e.g. "an article", "an hour".'
    assert output[0][6] == 'a'
    assert output[0][7] == ['an']
    assert output[1][4] == 0
    assert output[1][5] == 'It appears that a hyphen is missing in this expression.'
    assert output[1][6] == 'must try'
    assert output[1][7] == ['must-try']

def testTwoPagesOneMistake():
    '''
        Tests if a document containing one mistake on the second page of the
        document returns a list containing one element that provides information
        about that mistake.
    '''
    mistakes = ([
        ['a', 'tor into thinking it is conversing with a another human, like with the Google Dup',
         0, 'Use "an" instead of "a" if the following word starts with a vowel sound, e.g. "an article", "an hour".',
         ['an']
        ]
    ], 9.6)
    BASEPATH = os.path.abspath(os.path.dirname(__file__))
    fileLoc = os.path.join(BASEPATH, 'testFilesStyle', 'testStyleTwoPagesOneMistake.pdf')
    output = getMistakesInformationStyle(mistakes, fileLoc)
    assert len(output) == 1
    doc = fitz.open(fileLoc)
    page = doc.load_page(1)
    assert page.get_textbox(fitz.Rect(output[0][0], output[0][1] - page.rect.y1, output[0][2], output[0][3] - page.rect.y1)) == 'a'
    assert output[0][4] == 0
    assert output[0][5] == 'Use "an" instead of "a" if the following word starts with a vowel sound, e.g. "an article", "an hour".'
    assert output[0][6] == 'a'
    assert output[0][7] == ['an']

def testTwoPagesTwoMistakes():
    '''
        Tests if a document containing two mistakes on the second page of the 
        document returns a list containing two elements. Those elements contain,
        among other information, the coordinates of the mistakes text which are
        calculated from the height from the first page in the document.
    '''
    mistakes = ([
        ['a', 'tor into thinking it is conversing with a another human, like with the Google Dup',
         0, 'Use "an" instead of "a" if the following word starts with a vowel sound, e.g. "an article", "an hour".',
         ['an']
        ],
        ['must try', 'e hand of asking (written) questions. A must try to cause C to make the wrong identifica',
         0, 'It appears that a hyphen is missing in this expression.', ['must-try']
        ]
    ], 9.6)
    BASEPATH = os.path.abspath(os.path.dirname(__file__))
    fileLoc = os.path.join(BASEPATH, 'testFilesStyle', 'testStyleTwoPagesTwoMistakes.pdf')
    output = getMistakesInformationStyle(mistakes, fileLoc)
    assert len(output) == 2
    doc = fitz.open(fileLoc)
    page = doc.load_page(1)
    assert page.get_textbox(fitz.Rect(output[0][0], output[0][1] - page.rect.y1, output[0][2], output[0][3] - page.rect.y1)) == 'a'
    assert page.get_textbox(fitz.Rect(output[1][0], output[1][1] - page.rect.y1, output[1][2], output[1][3] - page.rect.y1)) == 'must try'
    assert output[0][4] == 0
    assert output[0][5] == 'Use "an" instead of "a" if the following word starts with a vowel sound, e.g. "an article", "an hour".'
    assert output[0][6] == 'a'
    assert output[0][7] == ['an']
    assert output[1][4] == 0
    assert output[1][5] == 'It appears that a hyphen is missing in this expression.'
    assert output[1][6] == 'must try'
    assert output[1][7] == ['must-try']