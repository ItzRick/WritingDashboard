from app.convertToPDF import bp
from flask import request, jsonify
from docx2pdf import convert


@bp.route('/convert', methods= ['GET'])
def convertDocx():
    file = request.args.get('filePath')
    convert(file, 'filePath'.replace("docx", "pdf"))
    return 'filePath'.replace("docx", "pdf")

