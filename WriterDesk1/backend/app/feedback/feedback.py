from app.feedback.retrieveText.convertDocxTxtToText import getTXTText, getDOCXText
from app.feedback.retrieveText.convertPdfToText import getPDFText
from app.feedback.content import sourceIntegration
from app.feedback.languageAndStyle import feedbackLanguageStyle
from app import cache
import nltk
from nltk.corpus import stopwords


def genFeedback(file):
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
    mistakesStyle, scoreStyle = feedbackLanguageStyle(text)
    scoreContent, explanationsContent = sourceIntegration(text, references, englishStopwords, userId)
    
    return True

@cache.memoize(30*24*60*60)
def getEnglishStopwords():
    nltk.download('stopwords')
    nltk.download('punkt')
    englishStopwords = stopwords.words('english')
    return englishStopwords