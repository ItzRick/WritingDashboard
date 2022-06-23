import os
from fpdf import FPDF
from subprocess import  Popen

def convertDocx(filePath):
    '''
        This function converts a docx file to a pdf file using libreoffice and calling it using the subprocess
        module. It then placed the newly made pdf file in the same location as 
        the docx file.
        Requires libreoficce to run, and requires libreoffice to be added to PATH
        Attributes:
            newPath: The path to the new pdf file.
            head: The head of the filePath of the file that is converted.
            tail: The tail of the filepath of the file that is converted.
        Arguments:
            filePath: The path to the docx file to be converted.
        Return:
            newPath: The location of the newly made pdf file.
    '''
    head, tail = os.path.split(filePath)
    newPath = os.path.join(head, 'converted', tail.replace(".docx", ".pdf"))
    # If the file is not yet converted:
    if not os.path.isfile(newPath):
        # Convert the file by using a libreoffice subprocess, that is making an libreoffice call to convert this docx file to a pdf:
        p = Popen(['soffice', '--headless', '--convert-to', 'pdf', '--outdir', os.path.split(newPath)[0], filePath])
        p.communicate()
    return newPath

def convertTxt(filePath):
    '''
        This function converts a txt file to a pdf file by making an empty pdf
        and copying the contents of the txt file to the newly made pdf file.
        Attributes:
            newPath: the path to the new pdf file.
            pdf: the newly made pdf file.
            f: the txt file opened to retrieve all text in it.
            head: The head of the filePath of the file that is converted.
            tail: The tail of the filepath of the file that is converted.
        Arguments:
            filePath: the path to the txt file to be converted.
        Return:
            newPath: the location of the newly made pdf file.
    '''
    head, tail = os.path.split(filePath)
    newPath = os.path.join(head, 'converted', tail.replace(".txt", ".pdf"))
    # If the converted folder of the newPath does not yet exist, create it:
    if not os.path.isdir(os.path.split(newPath)[0]):
        os.makedirs(os.path.split(newPath)[0])
    if not os.path.isfile(newPath):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=15)
        f = open(filePath, "r")
        # go over all lines in the txt file and add the text to the pdf file
        for x in f:
            pdf.multi_cell(w=0, h=10, txt = x, align = 'L')
        pdf.output(newPath)
    return newPath

def removeConvertedFiles(filePath, fileType):
    '''
        Removes files that have been converted to pdf from the folder the files have been converted to.
        Arguments:
            filePath: The path of the file that needs to be removed.
            fileType: The fileType of the file that needs to be removed.
        Attributes: 
            head: The head of the filePath of the file that needs to be removed.
            tail: The tail of the filepath of the file that needs to be removed.
            newPath: The path of the converted file that needs to be removed.
    '''
    # For a txt file:
    if fileType == '.txt':
        # Get the path of the converted file:
        head, tail = os.path.split(filePath)
        newPath = os.path.join(head, 'converted', tail.replace(".txt", ".pdf"))
        # If this exists, remove it:
        if os.path.isfile(newPath):
            os.remove(newPath)
            # If the folder this file is located in is empty, remove this folder:
            if not os.listdir(os.path.split(newPath)[0]):
                os.rmdir(os.path.split(newPath)[0])
    # For a docx file:
    elif fileType == '.docx':
        # Get the path of the converted file:
        head, tail = os.path.split(filePath)
        newPath = os.path.join(head, 'converted', tail.replace(".docx", ".pdf"))
        # If this exists, remove it:
        if os.path.isfile(newPath):
            os.remove(newPath)
            # If the folder this file is located in is empty, remove this folder:
            if not os.listdir(os.path.split(newPath)[0]):
                os.rmdir(os.path.split(newPath)[0])