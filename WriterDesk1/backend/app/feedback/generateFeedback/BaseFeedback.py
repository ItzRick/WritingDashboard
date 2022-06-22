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
        '''
            Method to upload the current scores, saved in the score variables of the current class and to 
            upload the explanations as stored in the explanations list in the current class to the database.
            Arguments: 
                self: The current class object.
            Attributes: 
                explanationIds: Possibly existing explanations of the current file, and explanationtype.
                idexp: Index of the current explanation id if there are any explanationIds returned.
                X1: The X1 coordinate of the current explanation.
                Y1: The Y1 coordinate of the current explanation.
                X2: The X2 coordinate of the current explanation.
                Y2: The Y2 coordinate of the current explanation.
                explType: The explanation type of the current explanation.
                expl: The explanation text for the current explanation.
                mistake: The mistake for the current explanation.
                replacements: The replacements for the current explanation.
        '''
        # Upload the scores:
        setScoreDB(self.fileId, self.scoreStyle, self.scoreCohesion, self.scoreStructure, self.scoreIntegration)
        # If there are any explanations upload them:
        if len(self.explanations) > 0:
            # See if there are any previously uploaded explanations for the current file:
            explanationIds = getExplanationsFileType(self.fileId, self.explanationType)
            # If there are as much previously uploaded explanations as new explanations, we use the existing explanationIds:
            if len(explanationIds) == len(self.explanations):
                for idexp, (X1, Y1, X2, Y2, explType, expl, mistake, replacements) in enumerate(self.explanations):
                    self.uploadExplanation(X1, Y1, X2, Y2, explanationIds[idexp], explType, expl, mistake, replacements)
            else:
                # If there are not as much currently existing explanations, we remove all explanations 
                # for the current file from the database:
                if len(explanationIds) > 0:
                    removeExplanationsFileType(self.fileId, self.explanationType)
                # Upload all new explanations to the database:
                for (X1, Y1, X2, Y2, explType, expl, mistake, replacements) in self.explanations:
                    self.uploadExplanation(X1, Y1, X2, Y2, -1, explType, expl, mistake, replacements)
    
    def uploadExplanation(self, X1, Y1, X2, Y2, explId, explanationType, explanation, mistake, replacements):
        '''
            Method to upload a single explanation to the database.
            Arguments:
                self: The current class object.
                X1: The X1 coordinate of the current explanation.
                Y1: The Y1 coordinate of the current explanation.
                X2: The X2 coordinate of the current explanation.
                Y2: The Y2 coordinate of the current explanation.
                explType: The explanation type of the current explanation.
                expl: The explanation text for the current explanation.
                mistake: The mistake for the current explanation.
                replacements: The replacements for the current explanation.
            Attributes: 
                replacement1: The possibly first replacement which is to be uploaded.
                replacement2: The possibly second replacement which is to be uploaded.
                replacement3: The possibly second replacement which is to be uploaded.
        '''
        # Initialize the replacement variables to empty string:
        replacement1 = replacement2 = replacement3 = ''
        # Add as much replacements as required, at most 3 and at least 0, by replacing these strings:
        if len(replacements) > 0:
            replacement1 = replacements[0]
        if len(replacements) > 1:
            replacement2 = replacements[1]
        if len(replacements) > 2:
            replacement3 = replacements[2]
        # Upload the explanation to the database.
        setExplanationDB(X1 = X1, Y1 = Y1, X2 = X2, Y2 = Y2, fileId = self.fileId, explId = explId, 
        type = explanationType, explanation = explanation, mistakeText = mistake, replacement1 = replacement1, replacement2 = replacement2, 
        replacement3 = replacement3)

    def addSingleExplanation(self, X1, Y1, X2, Y2, explanationType, explanation, mistake, replacements):
        '''
            Add a single explanation to the database variable of the current class. 
            Arguments:
                self: The current class object.
                X1: The X1 coordinate of the explanation to add.
                Y1: The Y1 coordinate of the explanation to add.
                X2: The X2 coordinate of the explanation to add.
                Y2: The Y2 coordinate of the explanation to add.
                explType: The explanation type of the explanation to add.
                expl: The explanation text for the explanation to add.
                mistake: The mistake for the explanation to add.
                replacements: The replacements for the explanation to add.
        '''
        self.explanations.append([X1, Y1, X2, Y2, explanationType, explanation, mistake, replacements])