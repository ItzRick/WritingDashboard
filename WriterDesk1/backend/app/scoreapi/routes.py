from app.scoreapi import bp
from app.scoreapi.scores import setScoreDB
from flask import request, jsonify
from app.models import Files, Scores, Explanations
from app.database import uploadToDatabase, removeFromDatabase

@bp.route('/setScore', methods = ['POST'])
def setScore():
    '''
        This functions handles setting the score as requested by the frontend.
        If the score is in [0..10], it sets the score. Scores are acurate to 2 decimal points
        If the score is -1, it does not override the old score
        If the score is something else, we set -2 to indicate a null value
        Attributes:
            fileId: Id of the file for which the score and explanation has to be set
            scoreStyle: Score for Language and Style
            scoreCohesion: Score for Cohesion
            scoreStructure: Score for Structure
            scoreIntegration: Score for Source Integration and Content
    '''
    # Get the data as sent by the react frontend:
    fid = request.form.get('fileId')
    scoreStyle = request.form.get('scoreStyle')
    scoreCohesion = request.form.get('scoreCohesion')
    scoreStructure = request.form.get('scoreStructure')
    scoreIntegration = request.form.get('scoreIntegration')
    
    return setScoreDB(fid, scoreStyle, scoreCohesion, scoreStructure, scoreIntegration)




@bp.route('/getScores', methods = ['GET'])
def getScores(): 
    '''
        This function handles returning the score of some file
        Attributes: 
            fileId: file id as given by the frontend
        Arguments:
            scoreStyle: Score for Language and Style
            scoreCohesion: Score for Cohesion
            scoreStructure: Score for Structure
            scoreIntegration: Score for Source Integration and Content
        returns:
            scores and code
    '''

    # get fileId from request
    fileId = request.args.get('fileId')
    
    # Check if the fileId exists in Scores
    if (Scores.query.filter_by(fileId=fileId).first() is None):
        return 'No score found with matching fileId', 400
    
    # Get scores
    scores = Scores.query.filter_by(fileId=fileId).first()
    # return scores
    return {
        'scoreStyle'       :scores.scoreStyle, 
        'scoreCohesion'    :scores.scoreCohesion, 
        'scoreStructure'   :scores.scoreStructure, 
        'scoreIntegration' :scores.scoreIntegration
    }, 200


@bp.route('/getExplanation', methods = ['GET'])
def getExplanation(): 
    '''
        This function handles returning a specific explanation of some file
        Attributes: 
            fileId: file id as given by the frontend
            explId: explanation id as given by the frontend
        Arguments:
            fileId: file id
            explId: explanation id
            type: Explanation type, what type of mistake is explained,
                    0=style, 1=cohesion, 2=structure, 3=integration
            explanation: String containing a comment on a part of the text in the file
            mistakeText: String, What text in the document is wrong
            X1: X of the top right corner of the boxing rectangle
            X2: X of the bottom left corner of the boxing rectangle
            Y1: Y of the top right corner of the boxing rectangle
            Y2: Y of the bottom left corner of the boxing rectangle
            replacement1..3: Three possible replacements for the mistakeText
        returns:
            explanation and code
    '''
    # get fileId from request
    fileId = request.args.get('fileId')
    explId = request.args.get('explId')
    
    # get explanation
    explanation = Explanations.query.filter_by(fileId=fileId, explId=explId).first()

    # Check if the fileId and explId exists in Explanation
    if explanation is None:
        return 'No explanation found with matching fileId and explId', 400
    
    # return explanation
    return explanation.serialize, 200

@bp.route('/getExplanationForFile', methods = ['GET'])
def getExplanationForFile(): 
    '''
        This function handles returning all explanations of some file
        Attributes: 
            fileId: file id as given by the frontend
        Arguments:
            Array containing:
                fileId: file id
                explId: explanation id
                type: Explanation type, what type of mistake is explained,
                        0=style, 1=cohesion, 2=structure, 3=integration
                explanation: String containing a comment on a part of the text in the file
                mistakeText: String, What text in the document is wrong
                X1: X of the top right corner of the boxing rectangle
                X2: X of the bottom left corner of the boxing rectangle
                Y1: Y of the top right corner of the boxing rectangle
                Y2: Y of the bottom left corner of the boxing rectangle
                replacement1..3: Three possible replacements for the mistakeText
        returns:
            list of explanations and code: code is return code, so 200 if it succeeded
    '''
    # get fileId from request
    fileId = request.args.get('fileId')
    
    # Check if the fileId exists in Explanation
    if (Explanations.query.filter_by(fileId=fileId).first() is None):
        return 'No explanations found with matching fileId', 400
    
    # Get explanations
    explanations = Explanations.query.filter_by(fileId=fileId).all()
    # return scores
    return jsonify([i.serialize for i in explanations]), 200


@bp.route('/setExplanation', methods = ['POST'])
def setExplanation():
    '''
        This functions handles setting the explanation to the database

        Attributes:
            fileId: Id for the file
            explId: Id for the explanation, if -1, create new explanation
            type: Explanation type, what type of mistake is explained,
                    0=style, 1=cohesion, 2=structure, 3=integration
            explanation: String containing a comment on a part of the text in the file
            mistakeText: String, What text in the document is wrong
            X1: X of the top right corner of the boxing rectangle
            X2: X of the bottom left corner of the boxing rectangle
            Y1: Y of the top right corner of the boxing rectangle
            Y2: Y of the bottom left corner of the boxing rectangle
            replacement1..3: Three possible replacements for the mistakeText
        returns:
            return code
    '''
    # Get the data as sent by the react frontend:
    fileId = request.form.get('fileId')
    explId = request.form.get('explId')
    type = request.form.get('type')
    explanation = request.form.get('explanation')
    mistakeText = request.form.get('mistakeText')
    X1          = request.form.get('X1')
    X2          = request.form.get('X2')
    Y1          = request.form.get('Y1')
    Y2          = request.form.get('Y2')
    replacement1= request.form.get('replacement1')
    replacement2= request.form.get('replacement2')
    replacement3= request.form.get('replacement3')

    # check if file exists
    if (Files.query.filter_by(id=fileId).first() is None):
        return 'No file found with fileId', 400

    # if explId = -1, create new record, else override one
    if explId == -1:
        # create new record
        # create Explanations object
        explanationIndb = Explanations(
            fileId = fileId,
            type        = type,
            explanation = explanation,
            mistakeText = mistakeText,
            X1          = X1,
            X2          = X2,
            Y1          = Y1,
            Y2          = Y2,
            replacement1= replacement1,
            replacement2= replacement2,
            replacement3= replacement3,
        )
    else:
        # already in Explanations
        # retreive current Explanation
        current = Explanations.query.filter_by(
            fileId=fileId, explId=explId).first()
        if current is not None:
            # remove from database, current scores
            removeFromDatabase(current)

        # create Explanations object
        explanationIndb = Explanations(
            fileId = fileId,
            explId = explId,
            type = type,
            explanation = explanation,
            mistakeText = mistakeText,
            X1          = X1,
            X2          = X2,
            Y1          = Y1,
            Y2          = Y2,
            replacement1= replacement1,
            replacement2= replacement2,
            replacement3= replacement3,
        )
    
    # upload
    uploadToDatabase(explanationIndb)

    return 'successfully uploaded Explanations'