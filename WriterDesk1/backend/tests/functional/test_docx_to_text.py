from app.convertToText import getDOCXText
import os


def testGetDocxHeading():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    os.chdir(dir_path)

    text = getDOCXText('headingTest.docx')
    assert text == 'This is some text.\n\nMore text.'


def testGetDocxReferences():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    os.chdir(dir_path)

    text = getDOCXText('referencesTest.docx')
    assert text == 'Text.\n\nMore text.\n\nNew text.'


def testGetDocxImages():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    os.chdir(dir_path)

    text = getDOCXText('imagesTest.docx')
    assert text == 'Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Maecenas porttitor congue massa.'


def testGetDocxTextboxes():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    os.chdir(dir_path)

    text = getDOCXText('textboxTest.docx')
    assert text == 'This is text outside a textbox.'


def testGetDocxEmptyFile():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    os.chdir(dir_path)

    text = getDOCXText('emptyFile.docx')
    assert text == ''


def testGetDocxCorruptedFile():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    os.chdir(dir_path)

    text = getDOCXText('corruptedFile.docx')
    assert text == ''


def testGetDocxInvalidFile():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    os.chdir(dir_path)

    text = getDOCXText('invalidFileName.docx')
    assert text == ''


def testGetDocxInvalidExtension():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    os.chdir(dir_path)

    text = getDOCXText('invalidFileExtension.pdf')
    assert text == ''
