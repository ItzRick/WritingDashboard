from app.models import Files, Scores
from app.database import uploadToDatabase, removeFromDatabase

def isValid(score):
    '''
        This function returns whether or not a score is valid: bool
        The score should be in [0..10]. Scores are acurate to 2 decimal points
        Arguments:
            score: score to best test for validness
    '''
    return (score >= 0.0) and (score <= 10.0)
    
def compareScores(current, new, NULL_VALUE):
    '''
        If the new is in [0..10], it returns new
        If the new is -1, it returns current
        If the new is something else, we set -2 to indicate a null value
        arguments:
            current: score that is currently in the database
            new: score that is destined for the database
        returns:
            If the new is in [0..10], it returns new
            If the new is -1, it returns current
            If the new is something else, we set -2 to indicate a null value
    '''
    #first check if is none, or if 'something else'
    if new is None or (not isValid(float(new)) and float(new) != -1):
        return NULL_VALUE
    elif float(new) == -1:
        return float(current)
    else:
        return float(new)

def setScoreDB(fileId, scoreStyle, scoreCohesion, scoreStructure, scoreIntegration):
    '''
        This functions handles setting the score and explanations for a file.
        If score is -1, the previous score is used
        If score is not in [0..10], and not -1. The score is set to -2 to indicate a null value
        Scores are acurate to 2 decimal points
        Arguments:
            fileId: Id of the file for which the score and explanation has to be set
            scoreStyle: Score for Language and Style
            scoreCohesion: Score for Cohesion
            scoreStructure: Score for Structure
            scoreIntegration: Score for Source Integration and Content
        returns:
            return code
    '''
    # value for when a variable is not defined
    NULL_VALUE = -2

    # Check if the fileId exists in Files
    if (Files.query.filter_by(id=fileId).first() is None):
        return 'No file found with fileId', 400
    
    # Check fileId exists in scores
    if Scores.query.filter_by(fileId=fileId).first() is not None:
        # already in score
        # retreive current Scores
        currentScores = Scores.query.filter_by(fileId=fileId).first()
        # remove from database, current scores
        removeFromDatabase(currentScores)
        # choose the new score if it is valid
        scoreStyle = compareScores(currentScores.scoreStyle, scoreStyle, NULL_VALUE)
        scoreCohesion = compareScores(currentScores.scoreCohesion, scoreCohesion, NULL_VALUE)
        scoreStructure = compareScores(currentScores.scoreStructure, scoreStructure, NULL_VALUE)
        scoreIntegration = compareScores(currentScores.scoreIntegration, scoreIntegration, NULL_VALUE)
    else:
        # check if score is valid or -1, when nothing was set before
        scoreStyle = compareScores(NULL_VALUE, scoreStyle, NULL_VALUE)
        scoreCohesion = compareScores(NULL_VALUE, scoreCohesion, NULL_VALUE)
        scoreStructure = compareScores(NULL_VALUE, scoreStructure, NULL_VALUE)
        scoreIntegration = compareScores(NULL_VALUE, scoreIntegration, NULL_VALUE)
    
    # create Scores object
    scoreIndb = Scores(fileId=fileId, scoreStyle=scoreStyle, scoreStructure=scoreStructure, scoreCohesion=scoreCohesion, scoreIntegration=scoreIntegration)
    # upload
    uploadToDatabase(scoreIndb)
    return 'successfully uploaded Scores'