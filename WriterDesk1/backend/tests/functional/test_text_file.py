from app.convertToText import getTXTText
import os

### Note: Test cases regarding finding references, images, or text boxes are not necessary in a txt file

def testGetTxtHeading():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    os.chdir(dir_path)

    actualOutput = getTXTText('normalFile.txt')
    expectedOutput = "This is the first sentence. The second sentence are as follows. I don't understand this document.\nThis is another paragraph. Why is this the case?\nHelp. Help. Help."
    assert actualOutput == expectedOutput

def testGetDocxEmptyFile():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    os.chdir(dir_path)

    text = getTXTText('emptyFile.txt')
    assert text == ''


def testGetDocxCorruptedFile():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    os.chdir(dir_path)

    text = getTXTText('corruptedFile.txt')
    assert text == ''


def testGetDocxInvalidFile():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    os.chdir(dir_path)

    text = getTXTText('invalidFileName.txt')
    assert text == ''


def testGetDocxInvalidExtension():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    os.chdir(dir_path)

    text = getTXTText('invalidFileExtension.doc')
    assert text == ''
