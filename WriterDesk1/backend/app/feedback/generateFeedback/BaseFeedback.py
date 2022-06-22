from app.scoreapi.scores import setScoreDB, setExplanationDB, getExplanationsFileType, removeExplanationsFileType

class BaseFeedback:
    '''
        A BaseFeedback class, with basic functionality for the various classes that create feedback. 
        This class will be inherited by the classes that will calculate the actual feedback for each of the 
        four writing skills.
        Attributes: 
            explanationType: The explanationType of the current class.
    '''
    explanationType = -1

    def __init__(self, text, referencesText, fileId, userId, filePath):
        '''
            A method to initialize this class, which sets the text, referencesText, fileId, userId, filePath variables 
            and resets other various variables.
            Arguments: 
                self: The current class object.
                text: Text for which the feedback will be generated.
                referencesText: The text containing the references for which the feedback will be generated.
                fileId: File id of the file for which feedback will be generated.
                userId: userId of the file for which the feedback will be generated.
                filePath: The filePath of which the file for which we generate feedback is located.
        '''
        self.text = text
        self.referencesText = referencesText
        self.fileId = fileId
        self.userId = userId
        self.filePath = filePath
        self.resetVariables()

    def resetVariables(self):
        '''
            Resets variables for the scores, so scoreStyle, scoreCohesion, scoreStructure and scoreIntegration, and 
            resets the explanation list, to make sure these get reset for each new file and not shared between various 
            class instances. These scores get reset to -1, since the backend will then not replace these scores in setScoreDB.
            Arguments: 
                self: The current class object.
        '''
        self.scoreStyle = -1
        self.scoreCohesion = -1 
        self.scoreStructure = -1 
        self.scoreIntegration = -1
        self.explanations = []

    def genFeedback(self):
        '''
            A method to generate feedback for the current class (so the current writing category).
            This is an empty method, which will be implemented in the various child classes. 
            Arguments: 
                self: The current class object.
        '''
        pass

    def uploadToDatabase(self):
        setScoreDB(self.fileId, self.scoreStyle, self.scoreCohesion, self.scoreStructure, self.scoreIntegration)
        if len(self.explanations) > 0:
            explanationIds = getExplanationsFileType(self.fileId, self.explanationType)
            if len(explanationIds) == len(self.explanations):
                for idexp, (X1, Y1, X2, Y2, explType, expl, mistake, replacements) in enumerate(self.explanations):
                    self.uploadExplanation(X1, Y1, X2, Y2, explanationIds[idexp], explType, expl, mistake, replacements)
            else:
                if len(explanationIds) > 0:
                    removeExplanationsFileType(self.fileId, self.explanationType)
                for (X1, Y1, X2, Y2, explType, expl, mistake, replacements) in self.explanations:
                    self.uploadExplanation(X1, Y1, X2, Y2, -1, explType, expl, mistake, replacements)
    
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