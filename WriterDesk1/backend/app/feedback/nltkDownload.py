import nltk 
from app import cache
from nltk.corpus import stopwords

@cache.memoize(30*24*60*60)
def downloadNltkCohesion():
    nltk.download('punkt')
    nltk.download('averaged_perceptron_tagger')
    nltk.download('wordnet')
    nltk.download('omw-1.4')

@cache.memoize(30*24*60*60)
def getEnglishStopwords():
    ''' 
        Method to retrieve english stop words from the nltk library. Downloads the punkt and stopwords, to be able to use the 
        word_tokenize method. This englishStopwords list as downloaded from nltk is memoized, that is stored, 
        for a month using flask_cache.
        returns:
            englishStopwords: The english stopwords from the nltk library.
    '''
    nltk.download('stopwords')
    nltk.download('punkt')
    englishStopwords = stopwords.words('english')
    return englishStopwords
