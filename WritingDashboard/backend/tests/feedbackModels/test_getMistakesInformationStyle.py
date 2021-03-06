from app.feedback.generateFeedback.LanguageStyleFeedback import LanguageStyleFeedback
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
            feedbackObject: Object of the class that generates the feedback for this language and style category.
        Arguments:
            testClient:  The test client we test this for.
    '''
    del testClient
    mistakes = []
    BASEPATH = os.path.abspath(os.path.dirname(__file__))
    fileLoc = os.path.join(BASEPATH, 'testFilesStyle', 'testStyleOnePageZeroMistakes.pdf')
    # generate the output on an empty text with no mistakes
    feedbackObject = LanguageStyleFeedback('', '', 1, 1, fileLoc)
    feedbackObject.getMistakesInformationStyle(mistakes)
    output = feedbackObject.explanations
    assert output == []

def testOnePageOneMistake(testClient):
    '''
        Tests if a document containing one mistake returns a list containing one
        element that provides information about that mistake.
        Attributes:
            mistakes: the mistakes on the text.
            BASEPATH: path to the file.
            fileLoc: pointer to the file.
            output: list of information about mistakes generated by the function.
            doc: the document opened through the fitz module for reading text.
            page: the first page in the document.
            feedbackObject: Object of the class that generates the feedback for this language and style category.
        Arguments:
            testClient:  The test client we test this for.
    '''
    del testClient
    mistakes = [
        ['a', 'tor into thinking it is conversing with a another human, like with the Google Dup',
         0, 'Use "an" instead of "a" if the following word starts with a vowel sound, e.g. "an article", "an hour".',
         ['an']
        ]
    ]
    BASEPATH = os.path.abspath(os.path.dirname(__file__))
    fileLoc = os.path.join(BASEPATH, 'testFilesStyle', 'testStyleOnePageOneMistake.pdf')
    # generate the output on a document with one page and one mistake
    feedbackObject = LanguageStyleFeedback('', '', 1, 1, fileLoc)
    feedbackObject.getMistakesInformationStyle(mistakes)
    output = feedbackObject.explanations
    # check if the output contains one list of information
    assert len(output) == 1
    doc = fitz.open(fileLoc)
    page = doc.load_page(0)
    # check if the coordinates enclose the mistake text, the writing skill has
    # number 0, the explanation, corresponding text and replacements is correct
    assert page.get_textbox(fitz.Rect(output[0][0], output[0][1], output[0][2], output[0][3])) == 'a'
    assert output[0][4] == 0
    assert output[0][5] == 'Use "an" instead of "a" if the following word starts with a vowel sound, e.g. "an article", "an hour".'
    assert output[0][6] == 'a'
    assert output[0][7] == ['an']

def testOnePageTwoMistakes(testClient):
    '''
        Tests if a document containing two mistakes returns a list containing 
        two elements. Those elements contain, among other information, the 
        coordinates of the mistakes text.
        Attributes:
            mistakes: the mistakes on the text.
            BASEPATH: path to the file.
            fileLoc: pointer to the file.
            output: list of information about mistakes generated by the function.
            doc: the document opened through the fitz module for reading text.
            page: the first page in the document.
            feedbackObject: Object of the class that generates the feedback for this language and style category.
        Arguments:
            testClient:  The test client we test this for.
    '''
    del testClient
    mistakes = [
        ['a', 'tor into thinking it is conversing with a another human, like with the Google Dup',
         0, 'Use "an" instead of "a" if the following word starts with a vowel sound, e.g. "an article", "an hour".',
         ['an']
        ],
        ['must try', 'e hand of asking (written) questions. A must try to cause C to make the wrong identifica',
         0, 'It appears that a hyphen is missing in this expression.', ['must-try']
        ]
    ]
    BASEPATH = os.path.abspath(os.path.dirname(__file__))
    fileLoc = os.path.join(BASEPATH, 'testFilesStyle', 'testStyleOnePageTwoMistakes.pdf')
    # generate the output on a document with one page and two mistakes
    feedbackObject = LanguageStyleFeedback('', '', 1, 1, fileLoc)
    feedbackObject.getMistakesInformationStyle(mistakes)
    output = feedbackObject.explanations
    # check if the output contains two lists of information
    assert len(output) == 2
    doc = fitz.open(fileLoc)
    page = doc.load_page(0)
    # check if the coordinates enclose the mistake text, the writing skill has
    # number 0, the explanation, corresponding text and replacements is correct
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

def testTwoPagesOneMistake(testClient):
    '''
        Tests if a document containing one mistake on the second page of the
        document returns a list containing one element that provides information
        about that mistake.
        Attributes:
            mistakes: the mistakes on the text.
            BASEPATH: path to the file.
            fileLoc: pointer to the file.
            output: list of information about mistakes generated by the function.
            doc: the document opened through the fitz module for reading text.
            page: the first page in the document.
            feedbackObject: Object of the class that generates the feedback for this language and style category.
        Arguments:
            testClient:  The test client we test this for.
    '''
    del testClient
    mistakes = [
        ['a', 'tor into thinking it is conversing with a another human, like with the Google Dup',
         0, 'Use "an" instead of "a" if the following word starts with a vowel sound, e.g. "an article", "an hour".',
         ['an']
        ]
    ]
    BASEPATH = os.path.abspath(os.path.dirname(__file__))
    fileLoc = os.path.join(BASEPATH, 'testFilesStyle', 'testStyleTwoPagesOneMistake.pdf')
    # generate the output on a document with two pages and one mistake
    feedbackObject = LanguageStyleFeedback('', '', 1, 1, fileLoc)
    feedbackObject.getMistakesInformationStyle(mistakes)
    output = feedbackObject.explanations
    # check if the output contains one list of information
    assert len(output) == 1
    doc = fitz.open(fileLoc)
    page = doc.load_page(1)
    # check if the coordinates enclose the mistake text, the writing skill has
    # number 0, the explanation, corresponding text and replacements is correct
    assert page.get_textbox(fitz.Rect(output[0][0], output[0][1] - page.rect.y1, output[0][2], output[0][3] - page.rect.y1)) == 'a'
    assert output[0][4] == 0
    assert output[0][5] == 'Use "an" instead of "a" if the following word starts with a vowel sound, e.g. "an article", "an hour".'
    assert output[0][6] == 'a'
    assert output[0][7] == ['an']

def testTwoPagesTwoMistakes(testClient):
    '''
        Tests if a document containing two mistakes on the second page of the 
        document returns a list containing two elements. Those elements contain,
        among other information, the coordinates of the mistakes text which are
        calculated from the height from the first page in the document.
        Attributes:
            mistakes: the mistakes on the text.
            BASEPATH: path to the file.
            fileLoc: pointer to the file.
            output: list of information about mistakes generated by the function.
            doc: the document opened through the fitz module for reading text.
            page: the first page in the document.
            feedbackObject: Object of the class that generates the feedback for this language and style category.
        Arguments:
            testClient:  The test client we test this for.
    '''
    del testClient
    mistakes = [
        ['a', 'tor into thinking it is conversing with a another human, like with the Google Dup',
         0, 'Use "an" instead of "a" if the following word starts with a vowel sound, e.g. "an article", "an hour".',
         ['an']
        ],
        ['must try', 'e hand of asking (written) questions. A must try to cause C to make the wrong identifica',
         0, 'It appears that a hyphen is missing in this expression.', ['must-try']
        ]
    ]
    BASEPATH = os.path.abspath(os.path.dirname(__file__))
    fileLoc = os.path.join(BASEPATH, 'testFilesStyle', 'testStyleTwoPagesTwoMistakes.pdf')
    # generate the output on a document with two pages and two mistakes
    feedbackObject = LanguageStyleFeedback('', '', 1, 1, fileLoc)
    feedbackObject.getMistakesInformationStyle(mistakes)
    output = feedbackObject.explanations
    # check if the output contains two lists of information
    assert len(output) == 2
    doc = fitz.open(fileLoc)
    page = doc.load_page(1)
    # check if the coordinates enclose the mistake text, the writing skill has
    # number 0, the explanation, corresponding text and replacements is correct
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

def testTeXFile(testClient):
    '''
        Tests if a TeX document containing one mistake on the second page of the
        document returns a list containing one element that provides information
        about that mistake.
        Attributes:
            mistakes: the mistakes on the text.
            BASEPATH: path to the file.
            fileLoc: pointer to the file.
            output: list of information about mistakes generated by the function.
            doc: the document opened through the fitz module for reading text.
            page: the first page in the document.
            feedbackObject: Object of the class that generates the feedback for this language and style category.
        Arguments:
            testClient:  The test client we test this for.
    '''
    del testClient
    mistakes = [
        ['a', 'tor into thinking it is conversing with a another human, like with the Google Dup',
         0, 'Use "an" instead of "a" if the following word starts with a vowel sound, e.g. "an article", "an hour".',
         ['an']
        ]
    ]
    BASEPATH = os.path.abspath(os.path.dirname(__file__))
    fileLoc = os.path.join(BASEPATH, 'testFilesStyle', 'testTeXFile.pdf')
    # generate the output on a document with two pages and one mistake
    feedbackObject = LanguageStyleFeedback('', '', 1, 1, fileLoc)
    feedbackObject.getMistakesInformationStyle(mistakes)
    output = feedbackObject.explanations
    # check if the output contains one list of information
    assert len(output) == 1
    doc = fitz.open(fileLoc)
    page = doc.load_page(1)
    # check if the coordinates enclose the mistake text, the writing skill has
    # number 0, the explanation, corresponding text and replacements is correct
    assert page.get_textbox(fitz.Rect(output[0][0], output[0][1] - page.rect.y1 * 0.999, output[0][2], output[0][3] - page.rect.y1 * 0.999)) == 'a'
    assert output[0][4] == 0
    assert output[0][5] == 'Use "an" instead of "a" if the following word starts with a vowel sound, e.g. "an article", "an hour".'
    assert output[0][6] == 'a'
    assert output[0][7] == ['an']