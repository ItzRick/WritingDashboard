from app.feedback.retrieveText.convertDocxTxtToText import getTXTText, getDOCXText
from app.feedback.retrieveText.convertPdfToText import getPDFText
from app.feedback.content import sourceIntegration
from app.feedback.languageAndStyle import feedbackLanguageStyle
from app.scoreapi.scores import setScoreDB, setExplanationDB
from app import cache
import nltk
from nltk.corpus import stopwords


def genFeedback(file):
    fileId = file.id
    fileType = file.fileType
    path = file.path
    userId = file.userId
    print(userId)
    references = ''
    print(path)
    if fileType == '.docx':
        text = getDOCXText(path)
    elif fileType == '.pdf':
        text, references = getPDFText(path, returnReferences=True)
    elif fileType == '.txt':
        text = getTXTText(path)
    englishStopwords = getEnglishStopwords()
    try:
        mistakesStyle, scoreStyle = feedbackLanguageStyle(text)
        scoreContent, explanationContent = sourceIntegration(text, references, englishStopwords, userId)
        setScoreDB(fileId, scoreStyle, -2, -2, scoreContent)
        setExplanationDB(fileId = fileId, explId = -1, type = 3, explanation = explanationContent)
    except Exception as e:
        return False, e
    return True

@cache.memoize(30*24*60*60)
def getEnglishStopwords():
    nltk.download('stopwords')
    nltk.download('punkt')
    englishStopwords = stopwords.words('english')
    return englishStopwords