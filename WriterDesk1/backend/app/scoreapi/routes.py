from app.scoreapi import bp

import os
from werkzeug.utils import secure_filename
from flask import current_app, request, session, jsonify
from app.models import Files, Scores, Explanations
from app.database import uploadToDatabase, getFilesByUser, removeFromDatabase, initialSetup
from magic import from_buffer 
from datetime import date
from mimetypes import guess_extension

@bp.route('/setScore', methods = ['POST'])
def setScore():
    '''
        This functions handles setting the score
        If score is -1, the score is not updated
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
    
    ''''''
    # Get current scores for fileId, note that since fileId is primaryKey, this should be at most 1
    
    return setScoreDB(fid, scoreStyle, scoreCohesion, scoreStructure, scoreIntegration)

@bp.route('/getScores', methods = ['GET'])
def getScores(): 
    # get fileId from request
    fileId = request.args.get('fileId')
    
    # Check if the fileId exists in Scores
    if (Scores.query.filter_by(fileId=fileId).first() is None):
        return 'No score found with fileId', 400
    
    # Get scores
    scores = Scores.query.filter_by(fileId=fileId).first()
    # return scores
    return {'scoreStyle':scores.scoreStyle, 'scoreCohesion':scores.scoreCohesion, 'scoreStructure':scores.scoreStructure, 'scoreIntegration':scores.scoreIntegration}, 200
    #

def setScoreDB(fileId, scoreStyle, scoreCohesion, scoreStructure, scoreIntegration):
    '''
        This functions handles setting the score and explanations for a file.
        If score is not in [0..1], the score is not updated
        Attributes:
            fileId: Id of the file for which the score and explanation has to be set
            scoreStyle: Score for Language and Style
            scoreCohesion: Score for Cohesion
            scoreStructure: Score for Structure
            scoreIntegration: Score for Source Integration and Content
    '''
    # Check if the fileId exists in Files
    if (Files.query.filter_by(id=fileId).first() is None):
        return 'No file found with fileId', 400
    # Check fileId exists in scores
    elif Scores.query.filter_by(fileId=fileId).first() is not None:
        # already in score
        # retreive current Scores
        currentScores = Scores.query.filter_by(fileId=fileId).first()

        # local function returns new score if new score is valid
        def compareScores(current, new):
            current = float(current)
            new = float(new)
            if (new < 0.0) or (new > 1.0):
                # invalid new score, return current
                return current
            else:
                return new
        # choose the new score if it is valid
        scoreStyle = compareScores(currentScores.scoreStyle, scoreStyle)
        scoreCohesion = compareScores(currentScores.scoreCohesion, scoreCohesion)
        scoreStructure = compareScores(currentScores.scoreStructure, scoreStructure)
        scoreIntegration = compareScores(currentScores.scoreIntegration, scoreIntegration)

        # remove from database, current scores
        removeFromDatabase(currentScores)
        
    # create Scores object
    scoreIndb = Scores(fileId=fileId, scoreStyle=scoreStyle, scoreStructure=scoreStructure, scoreCohesion=scoreCohesion, scoreIntegration=scoreIntegration)
    # upload
    uploadToDatabase(scoreIndb)

    return 'successfully uploaded Scores'

