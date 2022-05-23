from app.convertToPDF import bp
from flask import request, send_file
from docx2pdf import convert
import os
from fpdf import FPDF


@bp.route('/convert', methods= ['GET'])
def convertToPDF():
    filepath = request.args.get('filepath')
    filetype = request.args.get('filetype')
    print(filepath)
    if filetype == 'docx':
        if not os.path.isfile(filepath.replace("docx", "pdf")):
            convert(filepath)
        return send_file(filepath.replace("docx", "pdf"))
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

