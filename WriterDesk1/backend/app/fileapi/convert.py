import os
from fpdf import FPDF
from docx2pdf import convert

def convertDocx(filePath):
    newPath = filePath.replace("docx", "pdf")
    if not os.path.isfile(newPath):
        convert(newPath)
    return newPath

def convertTxt(filePath):
    newPath = filePath.replace("txt", "pdf")
    if not os.path.isfile(newPath):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=15)
        f = open(filePath, "r")
        for x in f:
            pdf.multi_cell(w=0, h=10, txt = x, align = 'L')
        pdf.output(newPath)
    return newPath