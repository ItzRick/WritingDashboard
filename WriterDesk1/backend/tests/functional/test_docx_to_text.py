from app.feedback.retrieveText.convertDocxTxtToText import getDOCXText
import os


def testGetDocxHeading(testClient):
    """
        Test if the getDOCXText function retrieves the text from the docx file without headings.
        Attributes:
            dir_path: Path of the location where the file is stored.
            text: String that contains the output of the getDOCXText function.
            references: String that contains the references extracted from the docx file.
        Arguments:
            testClient:  The test client we test this for.
    """
    del testClient
    BASEDIR = os.path.abspath(os.path.dirname(__file__))
    fileDir = os.path.join(BASEDIR, 'headingTest.docx')

    text, references = getDOCXText(fileDir)
    assert text == 'This is some text.\n\nMore text.'
    assert references == ''


def testGetDocxReferences(testClient):
    """
        Test if the getDOCXText function retrieves the text from the docx file without references.
        Attributes:
            dir_path: Path of the location where the file is stored.
            text: String that contains the output of the getDOCXText function.
            references: String that contains the references extracted from the docx file.
        Arguments:
            testClient:  The test client we test this for.
    """
    del testClient
    BASEDIR = os.path.abspath(os.path.dirname(__file__))
    fileDir = os.path.join(BASEDIR, 'referencesTest.docx')

    text, references = getDOCXText(fileDir)
    assert text == 'Text.\n\nMore text.\n\nNew text.'
    assert references == 'Reference 1\n\nReference 2\n\nReference 1\n\nReference 2'


def testGetDocxImages(testClient):
    """
        Test if the getDOCXText function retrieves the text from the docx file without images and corresponding captions.
        Attributes:
            dir_path: Path of the location where the file is stored.
            text: String that contains the output of the getDOCXText function.
            references: String that contains the references extracted from the docx file.
        Arguments:
            testClient:  The test client we test this for.
    """
    del testClient
    BASEDIR = os.path.abspath(os.path.dirname(__file__))
    fileDir = os.path.join(BASEDIR, 'imagesTest.docx')

    text, references = getDOCXText(fileDir)
    assert text == 'Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Maecenas porttitor congue massa.'
    assert references == ''


def testGetDocxTextboxes(testClient):
    """
        Test if the getDOCXText function retrieves the text from the docx file without text from textboxes.
        Attributes:
            dir_path: Path of the location where the file is stored.
            text: String that contains the output of the getDOCXText function.
            references: String that contains the references extracted from the docx file.
        Arguments:
            testClient:  The test client we test this for.
    """
    del testClient
    BASEDIR = os.path.abspath(os.path.dirname(__file__))
    fileDir = os.path.join(BASEDIR, 'textboxTest.docx')

    text, references = getDOCXText(fileDir)
    assert text == 'This is text outside a textbox.'
    assert references == ''


def testGetDocxEmptyFile(testClient):
    """
        Test if the getDOCXText function outputs an empty string when using an empty file.
        Attributes:
            dir_path: Path of the location where the file is stored.
            text: String that contains the output of the getDOCXText function.
            references: String that contains the references extracted from the docx file.
        Arguments:
            testClient:  The test client we test this for.
    """
    del testClient
    BASEDIR = os.path.abspath(os.path.dirname(__file__))
    fileDir = os.path.join(BASEDIR, 'emptyFile.docx')

    text, references = getDOCXText(fileDir)
    assert text == ''
    assert references == ''


def testGetDocxCorruptedFile(testClient):
    """
        Test if the getDOCXText function outputs an empty string when using a corrupted file.
        Attributes:
            dir_path: Path of the location where the file is stored.
            text: String that contains the output of the getDOCXText function.
            references: String that contains the references extracted from the docx file.
        Arguments:
            testClient:  The test client we test this for.
    """
    del testClient
    BASEDIR = os.path.abspath(os.path.dirname(__file__))
    fileDir = os.path.join(BASEDIR, 'corruptedFile.docx')

    text, references = getDOCXText(fileDir)
    assert text == ''
    assert references == ''


def testGetDocxInvalidFile(testClient):
    """
        Test if the getDOCXText function outputs an empty string when using a file path that does not exist.
        Attributes:
            dir_path: Path of the location where the file is stored.
            text: String that contains the output of the getDOCXText function.
            references: String that contains the references extracted from the docx file.
        Arguments:
            testClient:  The test client we test this for.
    """
    del testClient
    BASEDIR = os.path.abspath(os.path.dirname(__file__))
    fileDir = os.path.join(BASEDIR, 'invalidFileName.docx')

    text, references = getDOCXText(fileDir)
    assert text == ''
    assert references == ''


def testGetDocxInvalidExtension(testClient):
    """
        Test if the getDOCXText function outputs an empty string when using a file that is not a docx file.
        Attributes:
            dir_path: Path of the location where the file is stored.
            text: String that contains the output of the getDOCXText function.
            references: String that contains the references extracted from the docx file.
        Arguments:
            testClient:  The test client we test this for.
    """
    del testClient
    BASEDIR = os.path.abspath(os.path.dirname(__file__))
    fileDir = os.path.join(BASEDIR, 'invalidFileExtension.pdf')

    text, references = getDOCXText(fileDir)
    assert text == ''
    assert references == ''
