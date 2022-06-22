from app.feedback import bp
from flask import request
from app.models import Files
from app.feedback.feedback import genFeedback

@bp.route('/generate', methods = ['POST'])
def generateFeedback():
    '''
        Retrieve the fileId which has been passed as argument and run the genFeedback method on the file 
        associated to this fileId. Then indicate if feedback has been generated or a message with error code if no feedback
        could be generated. 
        Attributes:
            fileId: File id of the file we need to generate feedback for. 
            file: File associated with this fileId. 
            isSuccessful: True if the feedback generation was successful. False otherwise.
            message: Possible error message if feedback could not be generated.
        Returns: 
            Message, that indicated successful or an error if unsuccessful. And a status code, 200 if successful, 400 otherwise.
    '''
    # Get the fileId and file:
    fileIds = request.args.getlist('fileId')
    for fileId in fileIds:
        file = Files.query.filter_by(id=fileId).first()
        # Return error message if necessary:
        if file == None: 
            return f'The file with id {fileId} can not be found in the database.', 400
        # Call the genFeedback method:
        isSuccessful, message = genFeedback(file)
        # Return error message if necessary:
        if not isSuccessful:
            return str(message), 400
    return str(message), 200