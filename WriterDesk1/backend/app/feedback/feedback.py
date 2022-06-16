from app.feedback.retrieveText.convertDocxTxtToText import getTXTText, getDOCXText
from app.feedback.retrieveText.convertPdfToText import getPDFText
from app.feedback.content import sourceIntegration
from app.feedback.languageAndStyle import feedbackLanguageStyle
from app.feedback.getMistakesInformation import getMistakesInformationStructure, getMistakesInformationStyle
from app.feedback.structureCheck import getStructureScore
from app.fileapi.convert import convertDocx, convertTxt
from app.scoreapi.scores import setScoreDB, setExplanationDB
from app import cache
import nltk
from nltk.corpus import stopwords


def genFeedback(file):
    '''
        Generate the feedback for a certain file, by calling the methods to retrieve the text, 
        generate the feedback for the four different skill categories. Next, add this feedback including the explanations
        to the database. 
        arguments:
            file: File we need to generate this feedback for.
        attributes:
            fileId: fileId of the file we need to generate this feedback for.
            fileType: fileType, of the file we generate this feedback for. 
            path: Path of the file we generate this feedback for.
            userId: userId of the user we generate this feedback for. 
            references: References as retrieved by any of the get...Text methods.
            text: Text as retrieved by any of the get...Text methods.
            englishStopwords: English stopwords, as returned by the getEnglishStopwords method.
            mistakesStyle: explanations for the mistakes for the style, as returned by the feedbackLanguageStyle method.
            scoreStyle: Score for the style, as returned by the feedbackLanguageStyle method.
            scoreContent: Score for the source integration and content, as returned by the sourceIntegration method.
            explanationContent: Explanations for the source integration and content, as retrieved by the sourceIntegration method.
            scoreStructure: Score for the structure, as returned by the getStructureScore method.
            explanationsStructures, as returned by the getStructureScore method.
    '''
    fileId = file.id
    fileType = file.fileType
    path = file.path
    userId = file.userId
    try:
        references = ''
        if fileType == '.docx':
            text, references = getDOCXText(path)
            path = convertDocx(path)
        elif fileType == '.pdf':
            text, references = getPDFText(path, returnReferences=True)
        elif fileType == '.txt':
            text = getTXTText(path)
            path = convertTxt(path)
        englishStopwords = getEnglishStopwords()
        scoreContent, explanationContent = sourceIntegration(text, references, englishStopwords, userId)
        mistakesStyle, scoreStyle = feedbackLanguageStyle(text)
        scoreStructure, explanationsStructure = getStructureScore(text)
        setScoreDB(fileId, scoreStyle, -2, scoreStructure, scoreContent)
        setFeedbackStyle(mistakesStyle, path, fileId)
        setFeedbackStructure(explanationsStructure, path, fileId)
        setExplanationDB(fileId = fileId, explId = -1, type = 3, explanation = explanationContent)
    except Exception as e:
        return False, str(e)
    return True

def setFeedbackStyle(mistakesStyle, path, fileId):
    '''
        Run the getMistakesInformationStructure method to get the location of the mistakes in the language & style 
        category and upload these explanations to the database.
        attributes:
            feedbacks: List with feedback as retrieved by the getMistakesInformationStyle method.
            feedback: Single feedback instance from the feedbacks list.
        arguments: 
            mistakesStyle: mistakes as gotten from the feedbackLanguageStyle method.
            path: path corresponding to the pdf file, the coordinates of the mistakes should be retrieved from.
            fileId: fileId of the file we retrieve the mistakes from and put the mistakes from in the database.
    '''
    # Retrieve the mistakes with locations and possible replacements from the getMistakesInformationStyle method:
    feedbacks = getMistakesInformationStyle(mistakesStyle, path)
    # For each mistake, add it to the database together with required information:
    for feedback in feedbacks:
        # Get the replacements:
        replacements = feedback[7]
        # Add as much replacements as required, at most 3 and at least 0:
        if len(replacements) == 0:
            setExplanationDB(X1 = feedback[0], Y1 = feedback[1], X2 = feedback[2], Y2 = feedback[3], fileId = fileId, explId = -1, 
            type = feedback[4], explanation = feedback[5], mistakeText = feedback[6])
        elif len(replacements) == 1:
            setExplanationDB(X1 = feedback[0], Y1 = feedback[1], X2 = feedback[2], Y2 = feedback[3], fileId = fileId, explId = -1, 
            type = feedback[4], explanation = feedback[5], mistakeText = feedback[6], replacement1 = replacements[0])
        elif len(replacements) == 2:
            setExplanationDB(X1 = feedback[0], Y1 = feedback[1], X2 = feedback[2], Y2 = feedback[3], fileId = fileId, explId = -1, 
            type = feedback[4], explanation = feedback[5], mistakeText = feedback[6], replacement1 = replacements[0], 
            replacement2 = replacements[1])
        elif len(replacements) == 3:
            setExplanationDB(X1 = feedback[0], Y1 = feedback[1], X2 = feedback[2], Y2 = feedback[3], fileId = fileId, explId = -1, 
            type = feedback[4], explanation = feedback[5], mistakeText = feedback[6], replacement1 = replacements[0], 
            replacement2 = replacements[1], replacement3 = replacements[2])

def setFeedbackStructure(mistakesStructure, path, fileId):
    '''
        Run the getMistakesInformationStructure method to get the location of the mistakes in the structure category 
        and add each mistake to the database using the setExplanationDB method. 
        attributes:
            mistakes: Mistakes as retrieved by the getMistakesInformationStructure method.
            mistake: Single mistake from the mistakes list.
        arguments: 
            mistakesStructure: mistakes as gotten from the getStructureScore method.
            path: path corresponding to the pdf file, the coordinates of the mistakes should be retrieved from.
            fileId: fileId of the file we retrieve the mistakes from and put the mistakes from in the database.
    '''
    # Retrieve the mistakes with locations from the getMistakesInformationStructure method:
    mistakes = getMistakesInformationStructure(mistakesStructure, path)
    # For each mistake, add it to the database together with all required data:
    for mistake in mistakes:
        setExplanationDB(X1 = mistake[0], Y1 = mistake[1], X2 = mistake[2], Y2 = mistake[3], fileId = fileId, explId = -1, 
            type = mistake[4], explanation = mistake[5], mistakeText = mistake[6])


@cache.memoize(30*24*60*60)
def getEnglishStopwords():
    ''' 
        Method to retrieve english stop words from the nltk library. Downloads the punkt and stopwords, to be able to use the 
        word_tokenize method. This is memoized for a month using flask_cache.
        returns:
            englishStopwords: The english stopwords from the nltk library.
    '''
    nltk.download('stopwords')
    nltk.download('punkt')
    englishStopwords = stopwords.words('english')
    return englishStopwords