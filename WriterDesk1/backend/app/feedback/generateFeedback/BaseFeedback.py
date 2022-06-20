from app.scoreapi.scores import setScoreDB, setExplanationDB, getExplanationFileType

class BaseFeedback:
    scoreStyle = -1
    scoreCohesion = -1 
    scoreStructure = -1 
    scoreIntegration = -1
    explanations = []
    explanationType = 0

    def __init__(self, text, referencesText, fileId, userId):
        self.text = text
        self.referencesText = referencesText
        self.fileId = fileId
        self.userId = userId

    def genFeedback(self):
        pass

    def uploadToDatabase(self):
        explanationIds = getExplanationFileType(self.fileId, self.explanationType)
        if len(explanationIds) == len(self.explanations):
            for idexp, (X1, Y1, X2, Y2, type, expl, mistake, replacements) in enumerate(self.explanations):
                self.uploadExplanation(X1, Y1, X2, Y2, self.fileId, explanationIds[idexp], type, expl, mistake, replacements)
        else:
            pass
    
    def uploadExplanation(X1, Y1, X2, Y2, fileId, explId, type, explanation, mistake, replacements):
        replacement1 = replacement2 = replacement3 = ''
        # Add as much replacements as required, at most 3 and at least 0:
        if len(replacements) > 0:
            replacement1 = replacements[0]
        if len(replacements) > 1:
            replacement2 = replacements[1]
        if len(replacements) > 2:
            replacement3 = replacements[2]
        setExplanationDB(X1 = X1, Y1 = Y1, X2 = X2, Y2 = Y2, fileId = fileId, explId = explId, 
        type = type, explanation = explanation, mistakeText = mistake, replacement1 = replacement1, replacement2 = replacement2, 
        replacement3 = replacement3)