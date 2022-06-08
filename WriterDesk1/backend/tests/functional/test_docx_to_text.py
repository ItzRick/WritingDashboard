from app.convertDocxTxtToText import getDOCXText
import os


def testGetDocxHeading(testClient):
    """
        Test if the getDOCXText function retrieves the text from the docx file without headings.
        Attributes:
            dir_path: Path of the location where the file is stored.
            text: String that contains the output of the getDOCXText function.
        Arguments:
            testClient:  The test client we test this for.
    """
    del testClient
    dir_path = os.path.dirname(os.path.realpath(__file__))  # Get directory path
    os.chdir(dir_path)  # Set directory path

    text = getDOCXText('headingTest.docx')
    assert text == 'This is some text.\n\nMore text.'


def testGetDocxReferences(testClient):
    """
        Test if the getDOCXText function retrieves the text from the docx file without references.
        Attributes:
            dir_path: Path of the location where the file is stored.
            text: String that contains the output of the getDOCXText function.
        Arguments:
            testClient:  The test client we test this for.
    """
    del testClient
    dir_path = os.path.dirname(os.path.realpath(__file__))  # Get directory path
    os.chdir(dir_path)  # Set directory path

    text = getDOCXText('referencesTest.docx')
    assert text == 'Text.\n\nMore text.\n\nNew text.'


def testGetDocxImages(testClient):
    """
        Test if the getDOCXText function retrieves the text from the docx file without images and corresponding captions.
        Attributes:
            dir_path: Path of the location where the file is stored.
            text: String that contains the output of the getDOCXText function.
        Arguments:
            testClient:  The test client we test this for.
    """
    del testClient
    dir_path = os.path.dirname(os.path.realpath(__file__))  # Get directory path
    os.chdir(dir_path)  # Set directory path

    text = getDOCXText('imagesTest.docx')
    assert text == 'Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Maecenas porttitor congue massa.'


def testGetDocxTextboxes(testClient):
    """
        Test if the getDOCXText function retrieves the text from the docx file without text from textboxes.
        Attributes:
            dir_path: Path of the location where the file is stored.
            text: String that contains the output of the getDOCXText function.
        Arguments:
            testClient:  The test client we test this for.
    """
    del testClient
    dir_path = os.path.dirname(os.path.realpath(__file__))  # Get directory path
    os.chdir(dir_path)  # Set directory path

    text = getDOCXText('textboxTest.docx')
    assert text == 'This is text outside a textbox.'


def testGetDocxEmptyFile(testClient):
    """
        Test if the getDOCXText function outputs an empty string when using an empty file.
        Attributes:
            dir_path: Path of the location where the file is stored.
            text: String that contains the output of the getDOCXText function.
        Arguments:
            testClient:  The test client we test this for.
    """
    del testClient
    dir_path = os.path.dirname(os.path.realpath(__file__))  # Get directory path
    os.chdir(dir_path)  # Set directory path

    text = getDOCXText('emptyFile.docx')
    assert text == ''


def testGetDocxCorruptedFile(testClient):
    """
        Test if the getDOCXText function outputs an empty string when using a corrupted file.
        Attributes:
            dir_path: Path of the location where the file is stored.
            text: String that contains the output of the getDOCXText function.
        Arguments:
            testClient:  The test client we test this for.
    """
    del testClient
    dir_path = os.path.dirname(os.path.realpath(__file__))  # Get directory path
    os.chdir(dir_path)  # Set directory path

    text = getDOCXText('corruptedFile.docx')
    assert text == ''


def testGetDocxInvalidFile(testClient):
    """
        Test if the getDOCXText function outputs an empty string when using a file path that does not exist.
        Attributes:
            dir_path: Path of the location where the file is stored.
            text: String that contains the output of the getDOCXText function.
        Arguments:
            testClient:  The test client we test this for.
    """
    del testClient
    dir_path = os.path.dirname(os.path.realpath(__file__))  # Get directory path
    os.chdir(dir_path)  # Set directory path

    text = getDOCXText('invalidFileName.docx')
    assert text == ''


def testGetDocxInvalidExtension(testClient):
    """
        Test if the getDOCXText function outputs an empty string when using a file that is not a docx file.
        Attributes:
            dir_path: Path of the location where the file is stored.
            text: String that contains the output of the getDOCXText function.
        Arguments:
            testClient:  The test client we test this for.
    """
    del testClient
    dir_path = os.path.dirname(os.path.realpath(__file__))  # Get directory path
    os.chdir(dir_path)  # Set directory path

    text = getDOCXText('invalidFileExtension.pdf')
    assert text == ''
