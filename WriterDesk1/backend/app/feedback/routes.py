from app.feedback import bp
from flask import request
from app.models import Files
from app.feedback.feedback import genFeedback

@bp.route('/generate', methods = ['GET', 'POST'])
def generateFeedback():
    fileId = request.args.get('fileId')
    file = Files.query.filter_by(id=fileId).first()
    if file == None: 
        return f'The file with id {fileId} can not be found in the database.', 400
    genFeedback(file)
    return 'Feedback has been generated.', 200