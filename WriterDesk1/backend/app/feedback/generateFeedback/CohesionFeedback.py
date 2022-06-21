from app.feedback.generateFeedback.BaseFeedback import BaseFeedback

class LanguageStyleFeedback(BaseFeedback):

    def __init__(self, text, referencesText, fileId, userId, filePath):
        super().__init__(text, referencesText, fileId, userId, filePath)
        self.explanationType = 1