from app.models import Files, Scores, Explanations
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

def setScoreDB(fileId, scoreStyle, scoreCohesion, scoreStructure, scoreIntegration, feedbackVersion):
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
    scoreIndb = Scores(fileId=fileId, scoreStyle=scoreStyle, scoreStructure=scoreStructure, scoreCohesion=scoreCohesion, 
    scoreIntegration=scoreIntegration, feedbackVersion = feedbackVersion)
    # upload
    uploadToDatabase(scoreIndb)
    return 'successfully uploaded Scores'

def setExplanationDB(fileId, type, explanation, explId = -1, mistakeText = '', X1 = -1, X2 = -1, Y1 = -1, Y2 = -1, 
    replacement1 = '', replacement2 = '', replacement3 = '', feedbackVersion = 0):
    '''
        This functions handles adding an explanation to the database
        attributes: 
            current: Possibly current instance of this explanation if a explId has been supplied. 
        arguments:
            fileId: Id for the file
            explId: Id for the explanation, if -1, create new explanation
            type: Explanation type, what type of mistake is explained,
                    0=style, 1=cohesion, 2=structure, 3=integration
            explanation: String containing a comment on a part of the text in the file
            mistakeText: String, What text in the document is wrong, default empty string if this is not supplied.
            X1: X of the top right corner of the boxing rectangle. Default -1, to indicate no position in the text, if this is not supplied.
            X2: X of the bottom left corner of the boxing rectangle. Default -1, to indicate no position in the text has been supplied.
            Y1: Y of the top right corner of the boxing rectangle. Default -1, to indicate that no position in the text has been supplied.
            Y2: Y of the bottom left corner of the boxing rectangle. Default -1, to indicate that no position in the text has been supplied.
            replacement1: First possible replacements for the mistakeText, default empty string to indicate there is no replacement.
            replacement2: Second possible replacements for the mistakeText, default empty string to indicate there is no replacement.
            replacement3: Third possible replacements for the mistakeText, default empty string to indicate there is no replacement.
        returns:
            return true if the upload to the database was successful else false, for example if a explId was given that was not found.
            a message containing an error message or a message with a succesful upload to the database.
    '''
    if (Files.query.filter_by(id=fileId).first() is None):
        return False, 'No file found with fileId'

    # if explId = -1, create new record, else override one
    if explId == -1:
        # create new record
        # create Explanations object
        explanationIndb = Explanations(
            fileId          = fileId,
            type            = type,
            explanation     = explanation,
            mistakeText     = mistakeText,
            X1              = X1,
            X2              = X2,
            Y1              = Y1,
            Y2              = Y2,
            replacement1    = replacement1,
            replacement2    = replacement2,
            replacement3    = replacement3,
            feedbackVersion = feedbackVersion
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
            fileId          = fileId,
            explId          = explId,
            type            = type,
            explanation     = explanation,
            mistakeText     = mistakeText,
            X1              = X1,
            X2              = X2,
            Y1              = Y1,
            Y2              = Y2,
            replacement1    = replacement1,
            replacement2    = replacement2,
            replacement3    = replacement3,
            feedbackVersion = feedbackVersion
        )
    
    # upload
    uploadToDatabase(explanationIndb)

    return True, 'successfully uploaded Explanations'

def getExplanationsFileType(fileId, explType):
    '''
        Returns list for all explanationIds for explanations for a certain explanation type and fileId.
        Attributes:
            explanations: Explanation database instances for all explanations for a certain fileId and explanation type.
        Arguments:
            fileId: File id, together with the explanation type, we need to find all the explanations for.
            explType: Explanation type, together with the file id, we need to find all explanations for.
        Returns:
            List with all explanation ids for the explanations with this explanation type and fileId.
    '''
    explanations = Explanations.query.filter_by(fileId=fileId, type=explType).all()
    return [explanation.explId for explanation in explanations]

def removeExplanationsFileType(fileId, explType):
    '''
        Removes the explanations belonging to a certain fileId and explType from the database.
        Arguments:
            fileId: File id, together with the explanation type, we need to remove all the explanations for.
            explType: Explanation type, together with the file id, we need to remove all explanations for.
        Attributes:
            explanations: Explanation database instances for all explanations for a certain fileId and explanation type.
    '''
    explanations = Explanations.query.filter_by(fileId=fileId, type=explType).all()
    for explanation in explanations:
        removeFromDatabase(explanation)

def getCurrentExplanationVersion(fileId):
    '''
        Retrieves the most current explanation type for which scores (and explanations) have been generated 
        for the file associated with this fileId. 
        Arguments: 
            fileId: File id we need to find the most recent explanation version for which feedback has been generated.
        Attributes:
            scores: All scores in the database for the current file:
            explanations: All explanations for the current file in the database.
            feedbackVersion: The most recent feedback version that has been found in the scores.
        Returns:
            -1 if there is no feedback added for this file yet, or if there is an error in the database,
                that is if there is a explanation with a different feedbackversion than the score. In this case
                the method also removes all scores and explanations associated to this file.
            The most recent feedback version of this file otherwise.
    '''
    scores = Scores.query.filter_by(fileId=fileId).all()
    explanations = Explanations.query.filter_by(fileId=fileId).all()
    if len(scores) == 0:
        return -1
    feedbackVersion = scores[0].feedbackVersion
    if len(explanations) > 0:
        for explanation in explanations:
            if explanation.feedbackVersion != feedbackVersion:
                for score in scores:
                    removeFromDatabase(score)
                for explanation in explanations:
                    removeFromDatabase(explanation)
            return -1
    return scores[0].feedbackVersion

def removeExplanationsAndScores(fileId):
    '''
        Removes all explanations and scores associated to the file given by fileId.
        Arguments: 
            fileId: File id we need to remove all explanations and scores for.
        Attributes:
            scores: All scores in the database for the current file:
            explanations: All explanations for the current file in the database.
    '''
    scores = Scores.query.filter_by(fileId=fileId).all()
    explanations = Explanations.query.filter_by(fileId=fileId).all()
    for score in scores:
        removeFromDatabase(score)
    for explanation in explanations: 
        removeFromDatabase(explanation)