from app.feedback.retrieveText.convertPdfToText import getPDFText, splitBlocks, getFrequencyX, postProcessText, getLineText, filterLineList, filterLineNoLetters, getBlockText, isBlockTable, isTextCaption
import os
import fitz

def testGetPDFContinuedSentence(testClient):
    '''
        Test if text of pages is concatenated correctly when getPDFText() is called 
        on a file with sentences spread over multiple pages.
        Attributes: 
            BASEDIR: path of the directory that holds this file
            fileDir: path of the directory that holds the test pdf
            text: string of text returned by getPDFText
            isSuccesful: Boolean value to indicate if the text has been successfully retrieved
        Arguments:
            testClient: the test client we test this for
    '''

    del testClient
    BASEDIR = os.path.abspath(os.path.dirname(__file__))
    fileDir = os.path.join(BASEDIR, 'continuedSentenceFile.pdf')

    isSuccesful, text = getPDFText(fileDir)
    assert isSuccesful == True
    assert text == ('This is the last sentence of the first page, but it is so long that the sentence is continued'
    ' further on the next page.')

def testGetPDFReferences(testClient):
    '''
        Test if references are split and returned when getPDFText() is called with returnReferences=True
        Attributes: 
            BASEDIR: path of the directory that holds this file
            fileDir: path of the directory that holds the test pdf
            text: string of text returned by getPDFText
            references: string containing references returned by getPDFText
            isSuccesful: Boolean value to indicate if the text has been successfully retrieved
        Arguments:
            testClient: the test client we test this for
    '''

    del testClient
    BASEDIR = os.path.abspath(os.path.dirname(__file__))
    fileDir = os.path.join(BASEDIR, 'referenceFile.pdf')

    isSuccesful, text, references = getPDFText(fileDir, returnReferences=True)
    assert isSuccesful == True
    assert text == '''Donec fringilla risus nec lacus sollicitudin aliquam. Suspendisse non scelerisque leo. Sed malesuada arcu vel erat ultricies rutrum. Quisque condimentum cursus pharetra. Phasellus rutrum molestie dictum. Orci varius natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Nunc faucibus lobortis tortor non hendrerit.'''
    assert references == '''A Framework for Personal Science - Quantified Self. (n.d.). Retrieved June 17, 2021, from https://quantifiedself.com/blog/personal-science/ \n\nBaumer, E. P. S. (2015). Reflective Informatics. 585–594. https://doi.org/10.1145/2702123.2702234 \n\nBaumer, E. P. S., Khovanskaya, V., Matthews, M., Reynolds, L., Sosik, V. S., & Gay, G. (2014). Reviewing reflection: On the use of reflection in interactive system design. Proceedings of the Conference on Designing Interactive Systems: Processes, Practices, Methods, and Techniques, DIS, 93–102. https://doi.org/10.1145/2598510.2598598'''

def testGetPDFImages(testClient):
    '''
        Test if images are ignored when getPDFText() is called.
        Attributes: 
            BASEDIR: path of the directory that holds this file
            fileDir: path of the directory that holds the test pdf
            text: string of text returned by getPDFText
            isSuccesful: Boolean value to indicate if the text has been successfully retrieved
        Arguments:
            testClient: the test client we test this for
    '''

    del testClient
    BASEDIR = os.path.abspath(os.path.dirname(__file__))
    fileDir = os.path.join(BASEDIR, 'imageFile.pdf')

    isSuccesful, text = getPDFText(fileDir)
    assert isSuccesful == True
    assert text == ('Lorem ipsum dolor sit amet, consectetur adipiscing elit. Phasellus feugiat laoreet lacus id elementum.'
    ' Nunc sagittis commodo ipsum, a scelerisque odio viverra ac. Nullam id congue leo, condimentum hendrerit nibh. '
    'Ut pulvinar diam ut dignissim malesuada. \n\nDonec fringilla risus nec lacus sollicitudin aliquam. Suspendisse non'
    ' scelerisque leo. Sed malesuada arcu vel erat ultricies rutrum. Quisque condimentum cursus pharetra.')

def testGetPDFList(testClient):
    '''
        Test if list symbols are removed when getPDFText() is called.
        Attributes: 
            BASEDIR: path of the directory that holds this file
            fileDir: path of the directory that holds the test pdf
            text: string of text returned by getPDFText
            isSuccesful: Boolean value to indicate if the text has been successfully retrieved
        Arguments:
            testClient: the test client we test this for
    '''

    del testClient
    BASEDIR = os.path.abspath(os.path.dirname(__file__))
    fileDir = os.path.join(BASEDIR, 'listFile.pdf')

    isSuccesful, text = getPDFText(fileDir)
    assert isSuccesful == True
    assert text == ('Lorem ipsum dolor sit amet, consectetur adipiscing elit. Phasellus feugiat laoreet lacus id elementum.'
    ' Nunc sagittis commodo ipsum, a scelerisque odio viverra ac. Nullam id congue leo, condimentum hendrerit nibh. Ut pulvinar diam ut dignissim malesuada.'
    ' \n\nLorum \n\nIpsum \n\nDonec fringilla risus nec lacus sollicitudin aliquam. Suspendisse non scelerisque leo. Sed malesuada arcu vel erat ultricies rutrum.'
    ' Quisque condimentum cursus pharetra.')

def testGetPDFListNotIncluded(testClient):
    '''
        Test if list lines are removed completely when getPDFText() is called with includeLists=False.
        Attributes: 
            BASEDIR: path of the directory that holds this file
            fileDir: path of the directory that holds the test pdf
            text: string of text returned by getPDFText
            isSuccesful: Boolean value to indicate if the text has been successfully retrieved
        Arguments:
            testClient: the test client we test this for
    '''

    del testClient
    BASEDIR = os.path.abspath(os.path.dirname(__file__))
    fileDir = os.path.join(BASEDIR, 'notIncludeListFile.pdf')

    isSuccesful, text = getPDFText(fileDir, includeLists=False)
    assert isSuccesful == True
    assert text == ('This should be the only text.')

def testGetPDFTable(testClient):
    '''
        Test if text from tables is removed when getPDFText() is called.
        Attributes: 
            BASEDIR: path of the directory that holds this file
            fileDir: path of the directory that holds the test pdf
            text: string of text returned by getPDFText
            isSuccesful: Boolean value to indicate if the text has been successfully retrieved
        Arguments:
            testClient: the test client we test this for
    '''

    del testClient
    BASEDIR = os.path.abspath(os.path.dirname(__file__))
    fileDir = os.path.join(BASEDIR, 'tableFile.pdf')

    isSuccesful, text = getPDFText(fileDir)
    assert isSuccesful == True
    assert text == ('Lorem ipsum dolor sit amet, consectetur adipiscing elit. Phasellus feugiat laoreet lacus id elementum. '
    'Nunc sagittis commodo ipsum, a scelerisque odio viverra ac. Nullam id congue leo, condimentum hendrerit nibh. Ut pulvinar diam ut dignissim malesuada.'
    ' \n\nDonec fringilla risus nec lacus sollicitudin aliquam. Suspendisse non scelerisque leo. Sed malesuada arcu vel erat ultricies rutrum.'
    ' Quisque condimentum cursus pharetra.')

def testGetPDFEmptyFile(testClient):
    '''
        Test if empty string is returned when getPDFText() is called on an empty file.
        Attributes: 
            BASEDIR: path of the directory that holds this file
            fileDir: path of the directory that holds the test pdf
            text: string of text returned by getPDFText
            isSuccesful: Boolean value to indicate if the text has been successfully retrieved
        Arguments:
            testClient: the test client we test this for
    '''

    del testClient
    BASEDIR = os.path.abspath(os.path.dirname(__file__))
    fileDir = os.path.join(BASEDIR, 'emptyFile.pdf')

    isSuccesful, text = getPDFText(fileDir)
    assert isSuccesful == True
    assert text == ''


def testGetPDFCorruptedFile(testClient):
    '''
        Test if an error message string is returned when getPDFText() is called on a corrupted file.
        Attributes: 
            BASEDIR: path of the directory that holds this file
            fileDir: path of the directory that holds the test pdf
            message: string of text returned by getPDFText
            isSuccesful: Boolean value to indicate if the text has been successfully retrieved
        Arguments:
            testClient: the test client we test this for
    '''

    del testClient
    BASEDIR = os.path.abspath(os.path.dirname(__file__))
    fileDir = os.path.join(BASEDIR, 'corruptedFile.pdf')

    isSuccesful, message = getPDFText(fileDir)
    assert isSuccesful == False
    assert message == "Caught FileDataError('cannot open broken document') when calling getPDFText."


def testGetPDFInvalidFile(testClient):
    '''
        Test if an error message string is returned when getPDFText() is called on a file with an invalid file name.
        Attributes: 
            BASEDIR: path of the directory that holds this file
            fileDir: path of the directory that holds the test pdf
            message: string of text returned by getPDFText
            isSuccesful: Boolean value to indicate if the text has been successfully retrieved
        Arguments:
            testClient: the test client we test this for
    '''

    del testClient
    BASEDIR = os.path.abspath(os.path.dirname(__file__))
    fileDir = os.path.join(BASEDIR, 'invalidFileName.pdf')

    isSuccesful, message = getPDFText(fileDir)
    assert isSuccesful == False
    assert 'Caught FileNotFoundError("no such file: ' in message


def testGetPDFInvalidExtension(testClient):
    '''
        Test if an error message string is returned when getPDFText() is called on a file that is not a pdf.
        Attributes: 
            BASEDIR: path of the directory that holds this file
            fileDir: path of the directory that holds the test pdf
            message: string of text returned by getPDFText
            isSuccesful: Boolean value to indicate if the text has been successfully retrieved
        Arguments:
            testClient: the test client we test this for
    '''

    del testClient
    BASEDIR = os.path.abspath(os.path.dirname(__file__))
    fileDir = os.path.join(BASEDIR, 'invalidFileExtension.docx')

    isSuccesful, message = getPDFText(fileDir)
    assert isSuccesful == False
    assert 'Caught FileNotFoundError("no such file: ' in message

def testSplitBlocks(testClient):
    '''
        Test if splitBlocks() splits blocks correctly when they contain empty lines.
        Attributes: 
            BASEDIR: path of the directory that holds this file
            fileDir: path of the directory that holds the test pdf
            doc: document opened with Pymupdf
            blocks: blocks on the first page of the opened document
        Arguments:
            testClient: the test client we test this for
    '''
    
    del testClient
    BASEDIR = os.path.abspath(os.path.dirname(__file__))
    fileDir = os.path.join(BASEDIR, 'multitasking.pdf')

    doc = fitz.open(fileDir)
    blocks = doc[0].get_text("dict", flags = fitz.TEXTFLAGS_DICT & ~fitz.TEXT_PRESERVE_IMAGES & fitz.TEXT_INHIBIT_SPACES & fitz.TEXT_DEHYPHENATE)["blocks"]
    assert len(blocks) == 1
    blocks = splitBlocks(blocks)
    assert len(blocks) == 7

def testGetFrequencyX(testClient):
    '''
        Test if getFrequencyX() counts frequencies of x-coordinates correctly.
        Attributes: 
            BASEDIR: path of the directory that holds this file
            fileDir: path of the directory that holds the test pdf
            doc: document opened with Pymupdf
            counter: Counter object returned by getFrequencyX()
        Arguments:
            testClient: the test client we test this for
    '''

    del testClient
    BASEDIR = os.path.abspath(os.path.dirname(__file__))
    fileDir = os.path.join(BASEDIR, 'multitasking.pdf')

    doc = fitz.open(fileDir)
    counter = getFrequencyX(doc)
    assert len(counter) == 1

def testPostProcessText(testClient):
    '''
        Test if postProcessText() removes references, hyphenations and empty lines correctly.
        Attributes: 
            inputText: text that will be processed
            output: text returned by postProcessText()
        Arguments:
            testClient: the test client we test this for
    '''

    del testClient
    inputText = "First [1] sen- \ntences are hard (Source, 2022) \n  \nSo now you know "
    output = postProcessText(inputText, False)
    assert output == "First sentences are hard \n\nSo now you know"

def testGetLineText(testClient):
    '''
        Test if getLineText() retrieves text from lines correctly.
        Attributes: 
            BASEDIR: path of the directory that holds this file
            fileDir: path of the directory that holds the test pdf
            doc: document opened with Pymupdf
            line: first line from first block of opened document
        Arguments:
            testClient: the test client we test this for
    '''

    del testClient
    BASEDIR = os.path.abspath(os.path.dirname(__file__))
    fileDir = os.path.join(BASEDIR, 'multitasking.pdf')

    doc = fitz.open(fileDir)
    line = doc[0].get_text("dict", flags = fitz.TEXTFLAGS_DICT & ~fitz.TEXT_PRESERVE_IMAGES & fitz.TEXT_INHIBIT_SPACES & fitz.TEXT_DEHYPHENATE)["blocks"][0]["lines"][0]
    assert getLineText(line) == "Summary debate 1 Multitasking "

def testFilterLineList(testClient):
    '''
        Test if filterLineList() removes list symbols correctly.
        Attributes: 
            inputText: text that will be processed
            output: text returned by filterLineList()
        Arguments:
            testClient: the test client we test this for
    '''

    del testClient
    inputText = "b. This is a list "
    output = filterLineList(inputText)
    assert output == "This is a list "

def testFilterLineNoLetters(testClient):
    '''
        Test if filterLineNoLetters() removes empty lines without letters correctly.
        Attributes: 
            inputText: text that will be processed
            output: text returned by filterLineNoLetters()
        Arguments:
            testClient: the test client we test this for
    '''

    del testClient
    inputText = "4 "
    output = filterLineNoLetters(inputText)
    assert output == ""

def testGetBlockText(testClient):
    '''
        Test if getBlockText() retrieves text from blocks correctly.
        Attributes: 
            BASEDIR: path of the directory that holds this file
            fileDir: path of the directory that holds the test pdf
            doc: document opened with Pymupdf
            block: first block of opened document
        Arguments:
            testClient: the test client we test this for
    '''

    del testClient
    BASEDIR = os.path.abspath(os.path.dirname(__file__))
    fileDir = os.path.join(BASEDIR, 'multitasking.pdf')

    doc = fitz.open(fileDir)
    block = splitBlocks(doc[0].get_text("dict", flags = fitz.TEXTFLAGS_DICT & ~fitz.TEXT_PRESERVE_IMAGES & fitz.TEXT_INHIBIT_SPACES & fitz.TEXT_DEHYPHENATE)["blocks"])[0]
    assert getBlockText(block, True) == "Summary debate 1 Multitasking "

def testIsBlockTable(testClient):
    '''
        Test if isBlockTable() identifies potential table blocks correctly.
        Attributes: 
            BASEDIR: path of the directory that holds this file
            fileDir: path of the directory that holds the test pdf
            doc: document opened with Pymupdf
            xNormal: x-coordinate of normal text in the document
            blocks: blocks of opened document
        Arguments:
            testClient: the test client we test this for
    '''

    del testClient
    BASEDIR = os.path.abspath(os.path.dirname(__file__))
    fileDir = os.path.join(BASEDIR, 'tableFile.pdf')

    doc = fitz.open(fileDir)
    xNormal = getFrequencyX(doc).most_common(1)[0][0]
    blocks = splitBlocks(doc[0].get_text("dict", flags = fitz.TEXTFLAGS_DICT & ~fitz.TEXT_PRESERVE_IMAGES & fitz.TEXT_INHIBIT_SPACES & fitz.TEXT_DEHYPHENATE)["blocks"])
    assert isBlockTable(blocks[0], xNormal) == False
    assert isBlockTable(blocks[1], xNormal) == True
    assert isBlockTable(blocks[2], xNormal) == True
    assert isBlockTable(blocks[3], xNormal) == True
    assert isBlockTable(blocks[4], xNormal) == True
    assert isBlockTable(blocks[5], xNormal) == False

def testIsTextCaption(testClient):
    '''
        Test if isTextCaption() identifies captions correctly.
        Attributes: 
            inputText: text without caption that will be checked
            inputCaption: text with caption that will be checked
        Arguments:
            testClient: the test client we test this for
    '''

    del testClient
    inputText = "Figure 1 is not a caption"
    inputCaption = "Figure 2. A caption"
    assert not isTextCaption(inputText)
    assert isTextCaption(inputCaption)
