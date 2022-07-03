from app.feedback.retrieveText.convertDocxTxtToText import getTXTText
import os

### Note: Test cases regarding finding references, images, or text boxes are not necessary in a txt file

def testGetTxtFile(testClient):
    """
        Test if the getTXTText function retrieves the text from the txt file as a string.
        Attributes:
            dir_path: Path of the location where the file is stored.
            actualOutput: String that contains the output of the getTXTText function.
            expectedOutput: String that is to be compared to the actual output.
            isSuccesful: Boolean to indicate if the text has been successfully retrieved.
        Arguments:
            testClient:  The test client we test this for.
    """
    del testClient
    BASEDIR = os.path.abspath(os.path.dirname(__file__))
    fileDir = os.path.join(BASEDIR, 'testFiles', 'normalFile.txt')

    isSuccesful, actualOutput = getTXTText(fileDir)
    assert isSuccesful == True
    expectedOutput = ("This is the first sentence. The second sentence are as follows. I don't understand this document.\n\n" 
        "This is another paragraph. Why is this the case?\n\nHelp. Help. Help.")
    assert actualOutput == expectedOutput

def testGetDocxEmptyFile(testClient):
    """
        Test if the getTXTText function retrieves the catched error from an empty txt file.
        Attributes:
            dir_path: Path of the location where the file is stored.
            message: String that contains the output of the getTXTText function.
            isSuccesful: Boolean to indicate if the text has been successfully retrieved.
        Arguments:
            testClient:  The test client we test this for.
    """
    del testClient
    BASEDIR = os.path.abspath(os.path.dirname(__file__))
    fileDir = os.path.join(BASEDIR, 'testFiles', 'emptyFile.txt')

    isSuccesful, message = getTXTText(fileDir)
    assert isSuccesful == False
    assert message == "Caught IndexError('list index out of range') when calling getTXTText."


def testGetDocxCorruptedFile(testClient):
    """
        Test if the getTXTText function retrieves the catched error from a corrupted txt file.
        Attributes:
            dir_path: Path of the location where the file is stored.
            message: String that contains the output of the getTXTText function.
            isSuccesful: Boolean to indicate if the text has been successfully retrieved.
        Arguments:
            testClient:  The test client we test this for.
    """
    del testClient
    BASEDIR = os.path.abspath(os.path.dirname(__file__))
    fileDir = os.path.join(BASEDIR, 'testFiles', 'corruptedFile.txt')

    isSuccesful, message =  getTXTText(fileDir)
    assert isSuccesful == False
    assert "Caught UnicodeDecodeError" in message


def testGetDocxInvalidFile(testClient):
    """
        Test if the getTXTText function retrieves the catched error from an nonextistent txt file.
        Attributes:
            dir_path: Path of the location where the file is stored.
            message: String that contains the output of the getTXTText function.
            isSuccesful: Boolean to indicate if the text has been successfully retrieved.
        Arguments:
            testClient:  The test client we test this for.
    """
    del testClient
    BASEDIR = os.path.abspath(os.path.dirname(__file__))
    fileDir = os.path.join(BASEDIR, 'testFiles', 'invalidFileName.txt')

    isSuccesful, message = getTXTText(fileDir)
    assert isSuccesful == False
    assert message == "Caught FileNotFoundError(2, 'No such file or directory') when calling getTXTText."


def testGetDocxInvalidExtension(testClient):
    """
        Test if the getTXTText function retrieves the catched error from an file with an invalid extension.
        Attributes:
            dir_path: Path of the location where the file is stored.
            message: String that contains the output of the getTXTText function.
            isSuccesful: Boolean to indicate if the text has been successfully retrieved.
        Arguments:
            testClient:  The test client we test this for.
    """
    del testClient
    BASEDIR = os.path.abspath(os.path.dirname(__file__))
    fileDir = os.path.join(BASEDIR, 'testFiles', 'invalidFileExtension.doc')

    isSuccesful, message = getTXTText(fileDir)
    assert isSuccesful == False
    assert message == "Caught FileNotFoundError(2, 'No such file or directory') when calling getTXTText."
