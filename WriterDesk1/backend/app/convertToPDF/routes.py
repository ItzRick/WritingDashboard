from app.convertToPDF import bp
from flask import request, send_file
from docx2pdf import convert
import os
from fpdf import FPDF


@bp.route('/convert', methods= ['GET'])
def convertToPDF():
    '''
        Function to convert a document of type docx or txt to a document of
        type pdf. 
        Attributes:
            filepath: the path to the document to be converted.
            filetype: the type of the document to be converted.
            pdf: used in making a pdf from a txt file.
        Return:
            Take the converted document from the disk and send it. 
    '''
    filepath = request.args.get('filepath')
    filetype = request.args.get('filetype')
    # if the document is a docx file, use the convert method from the docx2pdf module and return the converted document.
    if filetype == 'docx':
        if not os.path.isfile(filepath.replace("docx", "pdf")):
            convert(filepath)
        return send_file(filepath.replace("docx", "pdf"))
    # if the document is a txt file, convert it to a pdf by making a new pdf using the contents of the txt file, 
    # then return the converted document.
    if filetype == 'txt':
        if not os.path.isfile(filepath.replace("txt", "pdf")):
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=15)
            f = open(filepath, "r")
            for x in f:
                pdf.multi_cell(w=0, h=10, txt = x, align = 'L')
            pdf.output(filepath.replace("txt", "pdf"))
        return send_file(filepath.replace("txt", "pdf"))
    return send_file(filepath)

