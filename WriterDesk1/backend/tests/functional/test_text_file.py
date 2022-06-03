from app.convertDocxTxtToText import getTXTText
import os

### Note: Test cases regarding finding references, images, or text boxes are not necessary in a txt file

def testGetTxtFile():
    """
        Test if the getTXTText function retrieves the text from the txt file as a string.
        Attributes:
            dir_path: Path of the location where the file is stored.
            actualOutput: String that contains the output of the getTXTText function.
            expectedOutput: String that is to be compared to the actual output
    """
    dir_path = os.path.dirname(os.path.realpath(__file__))
    os.chdir(dir_path)

    actualOutput = getTXTText('normalFile.txt')
    expectedOutput = "This is the first sentence. The second sentence are as follows. I don't understand this document.\nThis is another paragraph. Why is this the case?\nHelp. Help. Help."
    assert actualOutput == expectedOutput

def testGetDocxEmptyFile():
    """
        Test if the getTXTText function retrieves the text from the empty txt file as an empty string.
        Attributes:
            dir_path: Path of the location where the file is stored.
            text: String that contains the output of the getTXTText function.
    """
    dir_path = os.path.dirname(os.path.realpath(__file__))
    os.chdir(dir_path)

    text = getTXTText('emptyFile.txt')
    assert text == ''


def testGetDocxCorruptedFile():
    """
        Test if the getTXTText function retrieves the text from the corrupted txt file as an empty string.
        Attributes:
            dir_path: Path of the location where the file is stored.
            text: String that contains the output of the getTXTText function.
    """
    dir_path = os.path.dirname(os.path.realpath(__file__))
    os.chdir(dir_path)

    text = getTXTText('corruptedFile.txt')
    assert text == ''


def testGetDocxInvalidFile():
    """
        Test if the getTXTText function retrieves the text from the nonexistent file as an empty string.
        Attributes:
            dir_path: Path of the location where the file is stored.
            text: String that contains the output of the getTXTText function.
    """
    dir_path = os.path.dirname(os.path.realpath(__file__))
    os.chdir(dir_path)

    text = getTXTText('invalidFileName.txt')
    assert text == ''


def testGetDocxInvalidExtension():
    """
        Test if the getTXTText function retrieves the text from the doc file as an empty string.
        Attributes:
            dir_path: Path of the location where the file is stored.
            text: String that contains the output of the getTXTText function.
    """
    dir_path = os.path.dirname(os.path.realpath(__file__))
    os.chdir(dir_path)

    text = getTXTText('invalidFileExtension.doc')
    assert text == ''
