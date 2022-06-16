from nltk.corpus import stopwords
from app.feedback.feedback import getEnglishStopwords

def testEnglishstopwords(englishStopwords):
    '''
        Test the englishStopwords list by downloading the englishStopwords list again.
        Attributes: 
            english_stopwords: Newly downloaded englishStopwords list. 
        Arguments: 
            englishStopwords: English stopwords downloaded from nltk from conftest.py.
    '''
    english_stopwords = stopwords.words('english')
    assert english_stopwords == englishStopwords

def testEnglishstopwordsManually(englishStopwords):
    '''
        Test the englishStopwords list by manually constructing this list.
        Attributes: 
            english_stopwords: Manually put together version of these stopwords. 
        Arguments: 
            englishStopwords: English stopwords downloaded from nltk from conftest.py.
    '''
    english_stopwords = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're", "you've", "you'll", 
    "you'd", 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', "she's", 'her', 'hers', 'herself', 
    'it', "it's", 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', 
    "that'll", 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 
    'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 
    'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 
    'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 
    'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 
    'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', "don't", 
    'should', "should've", 'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', "aren't", 'couldn', "couldn't", 
    'didn', "didn't", 'doesn', "doesn't", 'hadn', "hadn't", 'hasn', "hasn't", 'haven', "haven't", 'isn', "isn't", 'ma', 
    'mightn', "mightn't", 'mustn', "mustn't", 'needn', "needn't", 'shan', "shan't", 'shouldn', "shouldn't", 'wasn', "wasn't", 
    'weren', "weren't", 'won', "won't", 'wouldn', "wouldn't"]
    assert englishStopwords == english_stopwords

def testMemoizeStopwords(testClient, englishStopwords):
    '''
        Test the getEnglishStopwords method from the app.feedback.feedback class. This method memoizes the words. 
        Arguments: 
            englishStopwords: English stopwords downloaded from nltk from conftest.py.
        Arguments:
            testClient:  The test client we test this for. 
    ''' 
    del testClient
    english_stopwords = getEnglishStopwords()
    assert englishStopwords == english_stopwords