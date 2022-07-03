from app.fileapi.convert import convertDocx, convertTxt, removeConvertedFiles
import os

def test_convertDocx(testClient):
    '''
        Tests if a docx file gets converted to a pdf file and the location of
        the converted file is returned
        Requires libreoficce to run, and requires libreoffice to be added to PATH
        Attributes:
            BASEPATH: path to the files.
            fileLoc: pointer to the docx file.
            convertedFileLoc: pointer to the pdf file.
            output: the location of the converted file.
            head: The head of the filePath of the file that is converted.
            tail: The tail of the filepath of the file that is converted.
    '''
    del testClient
    BASEPATH = os.path.abspath(os.path.dirname(__file__))
    fileLoc = os.path.join(BASEPATH, 'testFiles', 'test_convertDocx.docx')
    # the pdf file is in the same location but the extension is different
    head, tail = os.path.split(fileLoc)
    convertedFileLoc = os.path.join(head, 'converted', tail.replace(".docx", ".pdf"))
    # check is there is no converted file yet
    assert not os.path.exists(convertedFileLoc)
    # convert the docx file to a pdf file and return the location of the pdf
    output = convertDocx(fileLoc)
    # check if there now is a converted file
    assert os.path.exists(convertedFileLoc)
    # check if the output is the location of the converted file
    assert output == convertedFileLoc
    # remove the converted file for repeated testing
    removeConvertedFiles(fileLoc, '.docx')
    assert not os.path.exists(convertedFileLoc)
    assert not os.path.exists(os.path.split(convertedFileLoc)[0])

def test_convertTxt(testClient):
    '''
        Tests if a txt file gets converted to a pdf file and the location of
        the converted file is returned
        Attributes:
            BASEPATH: path to the files.
            fileLoc: pointer to the txt file.
            convertedFileLoc: pointer to the pdf file.
            output: the location of the converted file.
            head: The head of the filePath of the file that is converted.
            tail: The tail of the filepath of the file that is converted.
    '''
    del testClient
    BASEPATH = os.path.abspath(os.path.dirname(__file__))
    fileLoc = os.path.join(BASEPATH, 'testFiles', 'test_convertTxt.txt')
    # the pdf file is in the same location but the extension is different
    head, tail = os.path.split(fileLoc)
    convertedFileLoc = os.path.join(head, 'converted', tail.replace(".txt", ".pdf"))
    # check is there is no converted file yet
    assert not os.path.exists(convertedFileLoc)
    # convert the txt file to a pdf file and return the location of the pdf
    output = convertTxt(fileLoc)
    # check if there now is a converted file
    assert os.path.exists(convertedFileLoc)
    # check if the output is the location of the converted file
    assert output == convertedFileLoc
    # remove the converted file for repeated testing
    removeConvertedFiles(fileLoc, '.txt')
    assert not os.path.exists(convertedFileLoc)
    assert not os.path.exists(os.path.split(convertedFileLoc)[0])
