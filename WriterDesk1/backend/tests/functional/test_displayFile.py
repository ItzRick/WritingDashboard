import os
from io import BytesIO

def test_docx(testClient):
    '''
        Tests if a file that is of type docx gets converted to a pdf file.
        Attributes:
            BASEDIR: the location of the files.
            fileName: the name of the docx file.
            fileDir: a pointer to the docx file.
            data: the data needed by the display function.
            response: the result fo retrieving the file.
            pdfFile: the converted docx file.
        Arguments:
            testClient: The test client we test this for.
    '''
    BASEDIR = os.path.abspath(os.path.dirname(__file__))
    fileName = 'test_docx.docx'
    fileDir = os.path.join(BASEDIR, fileName)
    # check if the converted file already exists, if so remove it
    if os.path.isfile(fileDir.replace('.docx', '.pdf')):
        os.remove(fileDir.replace('.docx', '.pdf'))
    # put the data needed for the display function in a dictionary
    data = {
        'filepath': fileDir,
        'filetype': 'docx'
    }    
    # run the display function with the provided data
    response = testClient.get('/fileapi/display', query_string=data)   
    assert response.status_code == 200
    assert response.headers['Content-Disposition'] == 'inline; filename=test_docx.pdf'
    # read the newly converted file as a pdf
    with open(fileDir.replace(".docx", ".pdf"), 'rb') as file:
        pdfFile = BytesIO(file.read())
    assert response.data == pdfFile.read() 

def test_txt(testClient):
    '''
        Tests if a file that is of type txt gets converted to a pdf file.
        Attributes:
            BASEDIR: the location of the files.
            fileName: the name of the txt file.
            fileDir: a pointer to the txt file.
            data: the data needed by the display function.
            response: the result fo retrieving the file.
            pdfFile: the converted txt file.
        Arguments:
            testClient: The test client we test this for.
    '''
    BASEDIR = os.path.abspath(os.path.dirname(__file__))
    fileName = 'test_txt.txt'
    fileDir = os.path.join(BASEDIR, fileName)
    # check if the converted file already exists, if so remove it
    if os.path.isfile(fileDir.replace('.txt', '.pdf')):
        os.remove(fileDir.replace('.txt', '.pdf'))
    # put the data needed for the display function in a dictionary
    data = {
        'filepath': fileDir,
        'filetype': 'txt'
    }    
    # run the display function with the provided data
    response = testClient.get('/fileapi/display', query_string=data)   
    assert response.status_code == 200
    assert response.headers['Content-Disposition'] == 'inline; filename=test_txt.pdf'
    # read the newly converted file as a pdf
    with open(fileDir.replace(".txt", ".pdf"), 'rb') as file:
        pdfFile = BytesIO(file.read())
    assert response.data == pdfFile.read()

def test_pdf(testClient):
    '''
        Tests if a file that is of type pdf does not get converted.
        Attributes:
            BASEDIR: the location of the files.
            fileName: the name of the pdf file.
            fileDir: a pointer to the pdf file.
            data: the data needed by the display function.
            response: the result fo retrieving the file.
            pdfFile: the converted pdf file.
        Arguments:
            testClient: The test client we test this for.
    '''
    BASEDIR = os.path.abspath(os.path.dirname(__file__))
    fileName = 'test_pdf.pdf'
    fileDir = os.path.join(BASEDIR, fileName)
    # put the data needed for the display function in a dictionary
    data = {
        'filepath': fileDir,
        'filetype': 'pdf'
    }    
    # run the display function with the provided data
    response = testClient.get('/fileapi/display', query_string=data)   
    assert response.status_code == 200
    assert response.headers['Content-Disposition'] == 'inline; filename=test_pdf.pdf'
    # read the newly converted file as a pdf
    with open(fileDir.replace(".pdf", ".pdf"), 'rb') as file:
        pdfFile = BytesIO(file.read())
    assert response.data == pdfFile.read()