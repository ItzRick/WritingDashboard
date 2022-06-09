from app.convertToPDF import bp
from flask import request, send_file
from docx2pdf import convert
import os
from fpdf import FPDF


@bp.route('/convert', methods= ['GET'])
def convertToPDF():
    '''
        Returns the document converted to a pdf file. It will be converted to a pdf file if it is a docx or txt file, 
        otherwise it will just return the current document.
        Attributes:
            filepath: the path to the document to be converted.
            filetype: the type of the document to be converted which is used in determining the convertion method.
            pdf: an instance of the FPDF class used to make a pdf from a txt file.
            f: the txt file that is opened which is used for reading the contents of the txt file.
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

