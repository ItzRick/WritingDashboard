from app.feedback.generateFeedback.BaseFeedback import BaseFeedback
from app import languageToolEn
import re
import fitz

class LanguageStyleFeedback(BaseFeedback):
    '''
        Class, which inherits BaseFeedback, to generate the feedback for the Language and Style writing category.
    '''

    def __init__(self, text, referencesText, fileId, userId, filePath):
        '''
            A method to initialize this class, which sets the text, referencesText, fileId, userId, filePath variables, 
            sets the explanationType variable to 0, to indicate a language and style feedback and does all functionality of the 
            init function of BaseFeedback.
            Arguments: 
                self: The current class object.
                text: Text for which the feedback will be generated.
                referencesText: The text containing the references for which the feedback will be generated.
                fileId: File id of the file for which feedback will be generated.
                userId: userId of the file for which the feedback will be generated.
                filePath: The filePath of which the file for which we generate feedback is located.
            Attributes: 
                explanationType: explanationType of the current class, 2, to indicate Cohesion.
        '''
        super().__init__(text, referencesText, fileId, userId, filePath)
        self.explanationType = 0

    def genFeedback(self):
        """
            Generates feedback on the language & style of the input string.
            This includes grammar mistakes and spelling mistakes.
            Attributes:
                languageToolEn: LanguageTool object to generate feedback, this is a single object in the application.
                matches: List of Match objects containing the feedback.
                match: Match object containing the feedback.
                prevMatchEnd: End character of previous match in loop.
                occurrenceCount: count the occurrences of a mistake in the context.
                occurrenceInContext: The number of the correct occurrence of the mistake in the context.
                wordMatch: Match of word in context.
                context: context of mistake text.
                text: Input string that will be given feedback on.
                mistakes: List of mistakes in text including matched text, context,
                    occurrence of text in context, explanation, and possible replacements.
            Arguments:
                self: The current class object.
            Returns:
                explanations: List of explanations as they will be added to the database, created from 
                the mistake of this execution of the Language and Style score.
                scoreStyle: Score between 0 and 10 given to the text based on the feedback.
        """
        # Check for mistakes
        matches = languageToolEn.check(self.text)

        self.explanationsList = []
        for match in matches:

            prevMatchEnd = -1  # Position of last character of previous match in loop, initiated on -1
            occurrenceCount = 0  # Number of occurrences of a mistake
            occurrenceInContext = 0  # Final count of occurrences of a mistake

            # Find all occurrences of a mistake in the context
            for wordMatch in re.finditer(match.matchedText.lower().replace('(', '\(').replace(')', '\)'),
                                        match.context.lower()):
                if (wordMatch.start() > prevMatchEnd):
                    # Mistake overlaps previous mistake and does not count to occurrences

                    if wordMatch.start() == match.offsetInContext:
                        occurrenceInContext = occurrenceCount  # Set occurrenceInContext
                    else:
                        occurrenceCount += 1
                prevMatchEnd = wordMatch.end()

            context = match.context

            # Remove starting and ending ...
            if context[:3] == '...':
                context = context[3:]
            if context[-3:] == '...':
                context = context[:-3]

            # Append matched text, context, occurrence in context, explanation, and top 3 replacements to a list
            self.explanationsList.append([match.matchedText, context, occurrenceInContext, match.message, match.replacements[:3]])

        # Compute score
        self.scoreStyle = self.calculateScore(len(matches), len(self.text.split()))
        self.getMistakesInformationStyle(self.explanationsList)

        return self.scoreStyle, self.explanations

    def calculateScore(self, nrOfMistakes, nrOfWords):
        """
            Calculates a score for a text given the number of mistakes and number of words.
            Arguments:
                self: The current class object.
                nrOfMistakes: Number of mistakes in a text.
                nrOfWords: Number of total words of a text.
            Returns:
                score: Score between 0 and 10 given to the feedback.
        """

        # No division by 0
        if nrOfWords > 0:
            # Function to calculate score between 0 and 10
            score = max(0, -221.785 + (10 + 221.785) /
                        (1 + ((nrOfMistakes / nrOfWords) / 0.01911166) ** 1.415104) ** 0.007848222)
        else:
            score = 0

        # Round score to 1 decimal
        score = round(score, 1)

        return score

    def getMistakesInformationStyle(self, mistakes):
        '''
            This function makes a add to the explanations list of the current class, 
            the coordinates, writing skill number (0), explanation, mistake text 
            and replacements of each occurence of each language and style mistake 
            in a specified document.
            Attributes:
                listForDatabase: used for returning all database entries.
                doc: The document to get information from.
                word: The word that is wrong.
                sentence: The sentence that contains the word that is wrong.
                pageHeight: The total height starting at the first page of the 
                document.
                wordInstances: all the Rect objects that contain the word text
                for every page of the document.
                sentenceInstances: all the Rect objects that contain the mistake 
                text for every page of the document.
                wordsInSentence: all the Rect objects that are contained within the
                sentence the word that is wrong is in.
                corWord: The word that is at the correct location in the sentence.
                values: list containing all the information needed for highlighting
                that is to be put in the database.
                filePath: the path to the document to get information from.
            Arguments:
                mistakes: a format of mistakes in a document for the language and
                self: The current class object.
        '''
        doc = fitz.open(self.filePath)

        # go over all mistakes in the input
        for mistake in mistakes:
            word = mistake[0]
            sentence = mistake[1]

            pageHeight = 0

            # go over all pages in the input document
            for page in doc:
                # search for all occurences of the mistake
                wordInstances = page.search_for(word)
                # search for all occurences of the sentence
                sentenceInstances = page.search_for(sentence)

                # add the height of the page to the coordinates for returning
                if page.number != 0:
                    # initial
                    pageHeight += page.rect.y1
                    # another option, should be the same but maybe it works
                    # pageHeight += page.mediabox.y1
                    # another option, should be the same but maybe it works
                    # pageHeight += page.cropbox.y1

                # check if the word found is in the sentence, if this is the case
                # it gets added to a list that contains all specific words found in
                # that sentence
                wordsInSentence = []
                for sentenceFound in sentenceInstances:
                    for wordFound in wordInstances:
                        if sentenceFound.contains(wordFound):
                            wordsInSentence.append(wordFound)
                
                # if there are no mistakes on this page
                if len(wordsInSentence) == 0:
                    continue
                # the coordinates of string that is wrong
                corWord = wordsInSentence[mistake[2]]
                # list contains coordinates, type number, explanation, 
                # mistake text and replacement(s)
                self.addSingleExplanation(corWord.x0, corWord.y0 + pageHeight, corWord.x1, 
                    corWord.y1 + pageHeight, 0, mistake[3], mistake[0], mistake[4])