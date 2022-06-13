from app.feedback.retrieveText.convertDocxTxtToText import getTXTText
import os

### Note: Test cases regarding finding references, images, or text boxes are not necessary in a txt file

def testGetTxtFile(testClient):
    """
        Test if the getTXTText function retrieves the text from the txt file as a string.
        Attributes:
            dir_path: Path of the location where the file is stored.
            actualOutput: String that contains the output of the getTXTText function.
            expectedOutput: String that is to be compared to the actual output
        Arguments:
            testClient:  The test client we test this for.
    """
    del testClient
    BASEDIR = os.path.abspath(os.path.dirname(__file__))
    fileDir = os.path.join(BASEDIR, 'normalFile.txt')

    actualOutput = getTXTText(fileDir)
    expectedOutput = "This is the first sentence. The second sentence are as follows. I don't understand this document.\n\nThis is another paragraph. Why is this the case?\n\nHelp. Help. Help."
    assert actualOutput == expectedOutput

def testGetDocxEmptyFile(testClient):
    """
        Test if the getTXTText function retrieves the text from the empty txt file as an empty string.
        Attributes:
            dir_path: Path of the location where the file is stored.
            text: String that contains the output of the getTXTText function.
        Arguments:
            testClient:  The test client we test this for.
    """
    del testClient
    BASEDIR = os.path.abspath(os.path.dirname(__file__))
    fileDir = os.path.join(BASEDIR, 'emptyFile.txt')

    text = getTXTText(fileDir)
    assert text == ''


def testGetDocxCorruptedFile(testClient):
    """
        Test if the getTXTText function retrieves the text from the corrupted txt file as an empty string.
        Attributes:
            dir_path: Path of the location where the file is stored.
            text: String that contains the output of the getTXTText function.
        Arguments:
            testClient:  The test client we test this for.
    """
    del testClient
    BASEDIR = os.path.abspath(os.path.dirname(__file__))
    fileDir = os.path.join(BASEDIR, 'corruptedFile.txt')

    text = getTXTText(fileDir)
    assert text == ''


def testGetDocxInvalidFile(testClient):
    """
        Test if the getTXTText function retrieves the text from the nonexistent file as an empty string.
        Attributes:
            dir_path: Path of the location where the file is stored.
            text: String that contains the output of the getTXTText function.
        Arguments:
            testClient:  The test client we test this for.
    """
    del testClient
    BASEDIR = os.path.abspath(os.path.dirname(__file__))
    fileDir = os.path.join(BASEDIR, 'invalidFileName.txt')

    text = getTXTText(fileDir)
    assert text == ''


def testGetDocxInvalidExtension(testClient):
    """
        Test if the getTXTText function retrieves the text from the doc file as an empty string.
        Attributes:
            dir_path: Path of the location where the file is stored.
            text: String that contains the output of the getTXTText function.
        Arguments:
            testClient:  The test client we test this for.
    """
    del testClient
    BASEDIR = os.path.abspath(os.path.dirname(__file__))
    fileDir = os.path.join(BASEDIR, 'invalidFileExtension.doc')

    text = getTXTText(fileDir)
    assert text == ''
