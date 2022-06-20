from app.scoreapi.scores import setScoreDB, setExplanationDB, getExplanationsFileType, removeExplanationsFileType

class BaseFeedback:
    scoreStyle = -1
    scoreCohesion = -1 
    scoreStructure = -1 
    scoreIntegration = -1
    explanations = []
    explanationType = 0

    def __init__(self, text, referencesText, fileId, userId, filePath):
        self.text = text
        self.referencesText = referencesText
        self.fileId = fileId
        self.userId = userId
        self.filePath = filePath

    def genFeedback(self):
        pass

    def uploadToDatabase(self):
        setScoreDB(self.fileId, self.scoreStyle, self.scoreCohesion, self.scoreStructure, self.scoreIntegration)
        if len(self.explanations > 0):
            explanationIds = getExplanationsFileType(self.fileId, self.explanationType)
            if len(explanationIds) == len(self.explanations):
                for idexp, (X1, Y1, X2, Y2, explType, expl, mistake, replacements) in enumerate(self.explanations):
                    self.uploadExplanation(X1, Y1, X2, Y2, self.fileId, explanationIds[idexp], explType, expl, mistake, replacements)
            else:
                if len(explanationIds) > 0:
                    removeExplanationsFileType(self.fileId, self.explanationType)
                for (X1, Y1, X2, Y2, explType, expl, mistake, replacements) in self.explanations:
                    self.uploadExplanation(X1, Y1, X2, Y2, self.fileId, -1, explType, expl, mistake, replacements)
    
    def uploadExplanation(self, X1, Y1, X2, Y2, explId, explanationType, explanation, mistake, replacements):
        replacement1 = replacement2 = replacement3 = ''
        # Add as much replacements as required, at most 3 and at least 0:
        if len(replacements) > 0:
            replacement1 = replacements[0]
        if len(replacements) > 1:
            replacement2 = replacements[1]
        if len(replacements) > 2:
            replacement3 = replacements[2]
        setExplanationDB(X1 = X1, Y1 = Y1, X2 = X2, Y2 = Y2, fileId = self.fileId, explId = explId, 
        type = explanationType, explanation = explanation, mistakeText = mistake, replacement1 = replacement1, replacement2 = replacement2, 
        replacement3 = replacement3)

    def addSingleExplanation(self, X1, Y1, X2, Y2, explanationType, explanation, mistake, replacements):
        self.explanations.append([X1, Y1, X2, Y2, explanationType, explanation, mistake, replacements])