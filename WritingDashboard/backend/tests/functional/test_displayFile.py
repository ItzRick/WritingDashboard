import os
from io import BytesIO

from test_set_role import loginHelper

def test_docx(testClient, initDatabase):
    '''
        Tests if a file that is of type docx gets converted to a pdf file.
        Attributes:
            BASEDIR: the location of the files.
            fileName: the name of the docx file.
            fileDir: a pointer to the docx file.
            data: the data needed by the display function.
            response: the result fo retrieving the file.
            pdfFile: the converted docx file.
            convertedFileLoc: pointer to the pdf file that has been created by having converted the docx file.
            head: The head of the filePath of the file that is converted.
            tail: The tail of the filepath of the file that is converted.
        Arguments:
            testClient: The test client we test this for.
    '''

    del initDatabase

    BASEDIR = os.path.abspath(os.path.dirname(__file__))
    fileName = 'test_docx.docx'
    fileDir = os.path.join(BASEDIR, 'testFiles', fileName)
    # Get the path of the converted file:
    head, tail = os.path.split(fileDir)
    convertedFileLoc = os.path.join(head, 'converted', tail.replace(".docx", ".pdf"))
    # check if the converted file already exists, if so remove it
    if os.path.isfile(convertedFileLoc):
        os.remove(convertedFileLoc)
    # put the data needed for the display function in a dictionary
    data = {
        'filepath': fileDir,
        'filetype': 'docx'
    }    
    # run the display function with the provided data
    access_token = loginHelper(testClient, 'ad', 'min')

    response = testClient.get('/fileapi/display', query_string=data,
                            headers={"Authorization": "Bearer " + access_token})   
    assert response.status_code == 200
    assert response.headers['Content-Disposition'] == 'inline; filename=test_docx.pdf'
    # read the newly converted file as a pdf
    with open(convertedFileLoc, 'rb') as file:
        pdfFile = BytesIO(file.read())
    assert response.data == pdfFile.read() 

def test_txt(testClient, initDatabase):
    '''
        Tests if a file that is of type txt gets converted to a pdf file.
        Attributes:
            BASEDIR: the location of the files.
            fileName: the name of the txt file.
            fileDir: a pointer to the txt file.
            data: the data needed by the display function.
            response: the result fo retrieving the file.
            pdfFile: the converted txt file.
            convertedFileLoc: pointer to the pdf file that has been created by having converted the txt file.
            head: The head of the filePath of the file that is converted.
            tail: The tail of the filepath of the file that is converted.
            access_token: the access token
        Arguments:
            testClient: The test client we test this for.
    '''
    del initDatabase
    
    BASEDIR = os.path.abspath(os.path.dirname(__file__))
    fileName = 'test_txt.txt'
    fileDir = os.path.join(BASEDIR, 'testFiles', fileName)
    # Get the path of the converted file:
    head, tail = os.path.split(fileDir)
    convertedFileLoc = os.path.join(head, 'converted', tail.replace(".txt", ".pdf"))
    # check if the converted file already exists, if so remove it
    if os.path.isfile(convertedFileLoc):
        os.remove(convertedFileLoc)
    # put the data needed for the display function in a dictionary
    data = {
        'filepath': fileDir,
        'filetype': 'txt'
    }    
    # run the display function with the provided data
    access_token = loginHelper(testClient, 'ad', 'min')
    response = testClient.get('/fileapi/display', query_string=data,
                                headers={"Authorization": "Bearer " + access_token})   
    assert response.status_code == 200
    assert response.headers['Content-Disposition'] == 'inline; filename=test_txt.pdf'
    # read the newly converted file as a pdf
    with open(convertedFileLoc, 'rb') as file:
        pdfFile = BytesIO(file.read())
    assert response.data == pdfFile.read()

def test_pdf(testClient, initDatabase):
    '''
        Tests if a file that is of type pdf does not get converted.
        Attributes:
            BASEDIR: the location of the files.
            fileName: the name of the pdf file.
            fileDir: a pointer to the pdf file.
            data: the data needed by the display function.
            response: the result fo retrieving the file.
            pdfFile: the converted pdf file.
            access_token: the access token
        Arguments:
            testClient: The test client we test this for.
    '''
    del initDatabase

    BASEDIR = os.path.abspath(os.path.dirname(__file__))
    fileName = 'test_pdf.pdf'
    fileDir = os.path.join(BASEDIR, 'testFiles', fileName)
    # put the data needed for the display function in a dictionary
    data = {
        'filepath': fileDir,
        'filetype': 'pdf'
    }    
    # run the display function with the provided data
    access_token = loginHelper(testClient, 'ad', 'min')
    response = testClient.get('/fileapi/display', query_string=data,
                            headers={"Authorization": "Bearer " + access_token})   
    assert response.status_code == 200
    assert response.headers['Content-Disposition'] == 'inline; filename=test_pdf.pdf'
    # read the newly converted file as a pdf
    with open(fileDir.replace(".pdf", ".pdf"), 'rb') as file:
        pdfFile = BytesIO(file.read())
    assert response.data == pdfFile.read()