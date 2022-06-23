from app.feedback import bp
from flask import request, current_app
from app.models import Files
from app.feedback.feedback import genFeedback
from app.scoreapi.scores import getCurrentExplanationVersion

@bp.route('/generate', methods = ['POST'])
def generateFeedback():
    '''
        Retrieve the fileId which has been passed as argument and run the genFeedback method on the file 
        associated to this fileId. Then indicate if feedback has been generated or a message with error code if no feedback
        could be generated. 
        Attributes:
            fileIds: List with file ids we need to generate feedback for as retrieved from the frontend:
            fileId: File id of each file we need to generate feedback for. 
            file: File associated with this fileId. 
            isSuccessful: True if the feedback generation was successful. False otherwise.
            message: Possible error message if feedback could not be generated.
        Returns: 
            Message, that indicated successful or an error if unsuccessful. And a status code, 200 if successful, 400 otherwise.
    '''
    # Get the fileIds 
    fileIds = request.args.getlist('fileId')
    for fileId in fileIds:
        # For each fileId, retrieve this file from the database and generate feedback:
        file = Files.query.filter_by(id=fileId).first()
        # Return error message if necessary:
        if file == None: 
            return f'The file with id {fileId} can not be found in the database.', 400
        # Check if the feedback has already been generated:
        currentVersion = getCurrentExplanationVersion(fileId)
        if currentVersion >= current_app.config['feedbackVersion']:
            return 'Feedback has already been generated!', 200
        # Call the genFeedback method:
        isSuccessful, message = genFeedback(file)
        # Return error message if necessary:
        if not isSuccessful:
            return str(message), 400
    return str(message), 200