from this import d
from app.feedback.generateFeedback.BaseFeedback import BaseFeedback
from decimal import ROUND_HALF_UP, Decimal
import fitz
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser

class StructureFeedback(BaseFeedback):
    '''
        Class, which inherits BaseFeedback, to generate the feedback for the source integration and content writing category.
    '''

    def __init__(self, text, referencesText, fileId, userId, filePath):
        '''
            A method to initialize this class, which sets the text, referencesText, fileId, userId, filePath variables, 
            sets the explanationType variable to 2, to indicate cohesion feedback and does all functionality of the 
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
        self.explanationType = 2

    def genFeedback(self):
        '''
            Calculates the score for the structure writing skill currently based
            on the paragraph score only. At the end, the average score for all
            structure writing skill aspects is returned.
            Attributes:
                scores: a list of scores that contains the scores of all different
                structure aspects (in this case paragraph size only).
                score: the score for the structure writing skill.
                scoreRounded = the score rounded to one decimal behind the comma.
                explanationsDict: Dictionary with the explanations, which will also be added to the database.
                text: the text on which the structure score should be calculated.
            Arguments:
                self: The current class object.
            Return: 
                scoreStructure: the score for the structure writing skill (in this 
                case based on paragraph size only).
                explanations: List of explanations as added to the database.
        '''
        # If the input text is empty
        if len(self.text) == 0:
            self.scoreStructure = -2
            return None
        
        scores = []
        self.explanationsDict = dict()
        # Multiple different ways of getting scores for the structure writing 
        # skill can be added here.
        score, explanation = self.getParagraphScoreAndExplanations(self.text)
        scores.append(score)
        # Multiple different ways of getting explanations for the structure writing
        # skill can be added here.
        self.explanationsDict.update(explanation)

        # Take the average score of each submethod of getting scores for the 
        # structure writing skill and round it to one decimal behind the comma.
        score = sum(scores) / len(scores)
        self.scoreStructure = Decimal(score).quantize(
            Decimal('0.1'), rounding=ROUND_HALF_UP)
        self.getMistakesInformationStructure(self.explanationsDict)

        return self.scoreStructure, self.explanations


    def getParagraphScoreAndExplanations(self, text):
        '''
            Calculates the score for each paragraph based on the amount of words
            in each paragraph. At the end, the average score for all paragraphs is
            returned. Also generates feedback for "wrong" paragraphs and returns a
            dictionary with the text contained in the "wrong" paragraphs and their
            corresponding explanation.
            Attributes:
                paragraphScores: List that contains the scores of each paragraph.
                explanations: a dictionary containing explanations for certain 
                pieces of text that are wrong.
                paragraphScore: The score of a paragraph.
                paragraphScoreRounded: The paraGraphScore rounded to one decimal
                behind the comma.
                score: The average score taken over all paragraphs.
                scoreRounded: The score rounded to one decimal behind the comma.
            Arguments:
                self: The current class object.
                text: The text on which this will be run.
            Return: 
                scoreRounded: the score from 0 to 10 based on the average of the
                scores based on the amount of words in each paragraph.
                explanations: the wrong parts of text and their corresponding 
                explanations in a dictionary.

        '''
        # If the input text is empty.
        if len(text) == 0:
            return None

        # A list containing the scores for each paragraph in the text.
        paragraphScores = []

        # A dictionary that contains the paragraphs that are not good as keys and
        # their corresponding explanations as value.
        explanations = dict()

        # Split the text on white space to get each paragraph.
        for paragraph in text.splitlines():
            # If there are multiple white spaces in a row, continue.
            if len(paragraph.split()) == 0:
                continue
            # If the paragraph is more than 300 words.
            elif len(paragraph.split()) > 300:
                # paragraphScore is calculated by taking the max between 0.0 and
                # (100.0 - 0.4 * (the amount of words - 300)) / 10.0 to get a 
                # grade between 0.0 and 10.0. Having a high amount of words is 
                # worse than having a low amount of words.
                paragraphScore = max((100.0 - 0.4 * (len(paragraph.split()) - 300)
                    ) / 10.0, 0.0)
                paragraphScoreRounded = Decimal(paragraphScore).quantize(
                    Decimal('0.1'), rounding=ROUND_HALF_UP) 
                paragraphScores.append(paragraphScoreRounded)
                explanations[paragraph] = ('This paragraph is too long, '
                    'try to make paragraphs with approximately 200 words.')
            # If the paragraph is less than 100 words.
            elif len(paragraph.split()) < 100:
                # paragraphScore is calculated by taking the max between 0.0 and 
                # (100.0 - 0.6 * (100 - the amount of words)) / 10.0 to get a 
                # grade between 0.0 and 10.0. Having a low amount of words is not
                #  as bad as having a high amount of words.
                paragraphScore = max((100.0 - 0.6 * (100 - len(paragraph.split()))
                    ) / 10.0, 0.0)
                paragraphScoreRounded = Decimal(paragraphScore).quantize(
                    Decimal('0.1'), rounding=ROUND_HALF_UP)
                paragraphScores.append(paragraphScoreRounded)        
                explanations[paragraph] = ('This paragraph is too short, '
                    'try to make paragraphs with approximately 200 words.')         
            else:
            # If the paragraph is between 100 and 300 words.
                paragraphScores.append(Decimal(10.0).quantize(
                    Decimal('0.1'), rounding=ROUND_HALF_UP))

        # Take the average score of each paragraph and round it to 
        # one decimal behind the comma.
        score = sum(paragraphScores) / len(paragraphScores)
        scoreRounded = Decimal(score).quantize(
            Decimal('0.1'), rounding=ROUND_HALF_UP)

        return scoreRounded, explanations
    
    def getMistakesInformationStructure(self, mistakes):
        '''
            This function adds a single explanation to the explanations list of the current class, 
            that contains the coordinates, writing skill number (2), explanation and 
            mistake text of each occurence of each structure mistake in a specified document.
            Attributes:
                listForDatabase: used for returning all database entries.
                doc: The document to get information from.
                pageHeight: The total height starting at the first page of the 
                document.
                textInstances: all the Rect objects that contain the mistake text
                for every page of the document.
                values: list containing all the information needed for highlighting
                that is to be put in the database.
                filePath: the path to the document to get information from.
            Arguments:
                mistakes: a format of mistakes in a document for the structure
                writing skill.
                self: The current class object.
        '''
        doc = fitz.open(self.filePath)

        parser = PDFParser(open(self.filePath, 'rb'))
        doc2 = PDFDocument(parser)

        pageSizesList = []

        for page in PDFPage.create_pages(doc2):
            pageSizesList.append(page.mediabox[3])

        # go over all mistakes in the input
        for mistake in mistakes:
            pageHeight = 0
            # go over all pages in the input document
            for page in doc:
                # search for all occurences of the mistake
                textInstances = page.search_for(mistake)
                # add the height of the page to the coordinates for returning
                if page.number != 0:
                    # initial
                    # pageHeight += page.rect.y1
                    # another option, should be the same but maybe it works
                    # pageHeight += page.mediabox.y1
                    # another option, should be the same but maybe it works
                    # pageHeight += page.cropbox.y1
                    # pdfminer.six
                    pageHeight += pageSizesList[page.number - 1]
                # go over all occurences of the mistake
                for inst in textInstances:
                    # list contains coordinates, type number, explanation and 
                    # mistake text
                    self.addSingleExplanation(inst.x0, inst.y0 + pageHeight, inst.x1, 
                    inst.y1 + pageHeight, 2,  mistakes[mistake], mistake, [])