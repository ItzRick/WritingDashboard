from docx2pdf import convert 
from fpdf import FPDF

def convertDocx(file):
    convert(file, file.replace('docx', 'pdf'))

convertDocx('../writerdesk1/src/example3.docx')

def convertTXT(file):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=15)
    f = open(file, "r")
    for x in f:
        pdf.multi_cell(w=0, h=10, txt = x, align = 'L')

    pdf.output("src/example4.pdf")

convertTXT('../writerdesk1/src/example4.txt')
