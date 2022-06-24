from app.scoreapi import bp
from app.scoreapi.scores import setScoreDB, setExplanationDB
from flask import request, jsonify
from app.models import Files, Scores, Explanations
from app.database import uploadToDatabase, removeFromDatabase
from flask_jwt_extended import jwt_required, current_user
from sqlalchemy import func

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
@jwt_required()
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
@jwt_required()
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

@bp.route('/getAvgScores', methods = ['GET'])
@jwt_required()
def getAverageScores():
    '''
        This function handles returning the average scores of the latest (date) files
        from a given user, the number of files is dependend on the variable avgBasedOn
        Attributes:
            userId: user id as given by the frontend
            AVGBASEDON: integer, which is the number of recent files that the function uses for the average
        Arguments:
            avgscoreStyle: Average score for Language and Style
            avgscoreCohesion: Average score for Cohesion
            avgscoreStructure: Average score for Structure
            avgscoreIntegration: Average score for Source Integration and Content
        Returns:
            Average scores and status code, 
                status code 200: succes
                status code 400: no files found for given userId
    '''
    # get UserID from request
    userId = request.args.get('userId')

    # Average scores is based on num:AVGBASEDON files 
    AVGBASEDON = 5 

    # Check if user has files
    if (Files.query.filter_by(userId=userId).first() is None) :
        return 'No files for user', 400

    # Subquery selects num:avgBasedOn files from user orded by most recent date
    subq =  Files.query.\
            filter_by(userId = userId).\
            order_by(Files.date.desc()).\
            subquery()

    # All recents scores from user
    recentScores = Scores.query.join(subq, Scores.fileId == subq.c.id).limit(AVGBASEDON).all()

    if (len(recentScores) == 0) :
        return 'No files with scores for user', 400

    # Average value each explanation type for recentScores 
    avgscoreStyle = sum(x.scoreStyle for x in recentScores) / len(recentScores)
    avgscoreCohesion = sum(x.scoreCohesion for x in recentScores) / len(recentScores)
    avgscoreStructure = sum(x.scoreStructure for x in recentScores) / len(recentScores)
    avgscoreIntegration = sum(x.scoreIntegration for x in recentScores) / len(recentScores)

    return {
        'scoreStyle'       :round(avgscoreStyle,2),
        'scoreCohesion'    :round(avgscoreCohesion,2),
        'scoreStructure'   :round(avgscoreStructure,2),
        'scoreIntegration' :round(avgscoreIntegration,2)
    }, 200


@bp.route('/getFilesAndScoresByUser', methods=['GET'])
@jwt_required()
def getFilesAndScoresByUser():
    '''
        This function handles returning the files and corresponding scores of the current user.
        Attributes:
            fileList: List of rows containing file and score attributes for the current user.
            file: Row in fileList.
        returns:
            fileDict: Dictionary containing file and score attributes for the current user.
    '''

    # Query all files and scores of current user
    fileList = Files.query.filter_by(userId=current_user.id).join(Scores, Files.id == Scores.fileId)\
        .with_entities(Files.id, Files.filename, Files.date, Scores.scoreStyle, Scores.scoreCohesion,
                       Scores.scoreStructure, Scores.scoreIntegration).order_by(Files.date.asc())

    # Create empty dictionary
    fileDict = {'id': [], 'filename': [], 'date': [], 'scoreStyle': [], 'scoreCohesion': [], 'scoreStructure': [], 'scoreIntegration': []}

    # Copy fileList to fileDict
    for file in fileList:
        fileDict['id'].append(file.id)
        fileDict['filename'].append(file.filename)
        fileDict['date'].append(file.date.strftime('%m/%d/%y'))
        fileDict['scoreStyle'].append(str(file.scoreStyle))
        fileDict['scoreCohesion'].append(str(file.scoreCohesion))
        fileDict['scoreStructure'].append(str(file.scoreStructure))
        fileDict['scoreIntegration'].append(str(file.scoreIntegration))

    return fileDict, 200



@bp.route('/getExplanationForFile', methods = ['GET'])
@jwt_required()
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

    # Make the call to the backend function and retrieve if this is successful or not and the message:
    isSuccessful, message = setExplanationDB(fileId, explId, type, explanation, mistakeText, X1, X2, Y1, Y2, replacement1, replacement2, replacement3)

    # Return message and the correct status code:
    if isSuccessful:
        return message, 200
    else: 
        return message, 400