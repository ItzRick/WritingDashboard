from app.scoreapi import bp
from flask import request, jsonify
from app.models import Files, Scores, Explanations
from flask_jwt_extended import jwt_required, current_user

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


@bp.route('/getExplanationForFileAndType', methods=['GET'])
def getExplanationForFileAndType():
    '''
        This function handles returning all explanations of a given file and type. These only include unique explanations.
        It returns a 400 error when there is no explanation in the database with the given fileId and type.
        Attributes:
            fileId: File id as given by the frontend
            type: Type in number given by the frontend
            explanationsFiltered: Query containing all explanations with given fileId and type
            explanations: Unique explanations with given fileId and type.
        returns:
            List of unique explanations with the given fileId and type.
            Function returns 400 error when there does not exist an explanation with these constraints in the database.
    '''
    # Get fileId from request
    fileId = request.args.get('fileId')
    type = request.args.get('type')

    # Filter on fileId and type
    explanationsFiltered = Explanations.query.filter_by(fileId=fileId, type=type)

    # Check if the fileId exists in Explanation
    if explanationsFiltered.first() is None:
        return 'No explanations found with matching fileId and type', 400

    # Get explanations
    explanations = explanationsFiltered\
        .distinct(Explanations.mistakeText, Explanations.explanation, Explanations.replacement1,
                  Explanations.replacement2, Explanations.replacement3).all()

    # Return Explanations
    return jsonify([i.serialize for i in explanations]), 200


@bp.route('/getExplanationForFileAndCoordinates', methods=['GET'])
def getExplanationForFileAndCoordinates():
    '''
        This function handles returning all explanations of a given file and coordinates. These only include unique explanations.
        It returns a 400 error when there is no explanation in the database with the given fileId and coordinates.
        Attributes:
            fileId: File id as given by the frontend
            x: X-coordinate of the click as given by the frontend
            y: Y-coordinate of the click as given by the frontend
            explanationsFiltered: Query containing all explanations with given fileId and coordinates
            explanations: Unique explanations with given fileId and coordinates.
        returns:
            List of unique explanations with the given fileId and coordinates.
            Function returns 400 error when there does not exist an explanation with these constraints in the database.
    '''
    # Get fileId from request
    fileId = request.args.get('fileId')

    # Get x and y coordinates of click from request
    x = request.args.get('x')
    y = request.args.get('y')

    # Filter on fileId and coordinates
    explanationsFiltered = Explanations.query.filter_by(fileId=fileId).filter(x >= Explanations.X1, x <= Explanations.X2,
                                                                              y >= Explanations.Y1, y <= Explanations.Y2)

    # Check if there exists explanations for this fileid and coordinates
    if explanationsFiltered.first() is None:
        return 'No explanations found with matching fileId and coordinates', 400

    # Get explanations
    explanations = explanationsFiltered\
        .distinct(Explanations.type, Explanations.mistakeText, Explanations.explanation, Explanations.replacement1,
                  Explanations.replacement2, Explanations.replacement3).all()

    # Return Explanations
    return jsonify([i.serialize for i in explanations]), 200
