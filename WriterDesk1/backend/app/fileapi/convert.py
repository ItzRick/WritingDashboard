import os
from fpdf import FPDF
from subprocess import  Popen

def convertDocx(filePath):
    '''
        This function converts a docx file to a pdf file using the aspose-words
        module. It then placed the newly made pdf file in the same location as 
        the docx file.
        Attributes:
            newPath: The path to the new pdf file.
        Arguments:
            filePath: The path to the docx file to be converted.
        Return:
            newPath: The location of the newly made pdf file.
    '''
    newPath = filePath.replace(".docx", ".pdf")
    if not os.path.isfile(newPath):
        LIBRE_OFFICE = r"C:\\Program Files\\LibreOffice\\program\\soffice.exe"
        p = Popen(['soffice', '--headless', '--convert-to', 'pdf', '--outdir', os.path.split(filePath)[0], filePath])
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
        Arguments:
            filePath: the path to the txt file to be converted.
        Return:
            newPath: the location of the newly made pdf file.
    '''
    newPath = filePath.replace(".txt", ".pdf")
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