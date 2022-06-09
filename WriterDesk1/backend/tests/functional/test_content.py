from app.feedback.content import countParagraphs, wordsSource, wordsText

def testCountParagraphsOne(testClient):
    '''
    Test the countParagraphs method, which counts the number of paragraphs where each paragraph is divided by 
    2 newline characters. Test this for a text with 1 paragraph.
    Attributes:  
        text: The text we run the method on, containing 1 paragraph.
    Arguments:
        testClient:  The test client we test this for.
    '''
    del testClient
    text = "this is a very nice text with 1 paragraph."
    assert countParagraphs(text) == 1

def testCountParagraphsTwo(testClient):
    '''
    Test the countParagraphs method, which counts the number of paragraphs where each paragraph is divided by 
    2 newline characters. Test this for a text with 2 paragraphs.
    Attributes:  
        text: The text we run the method on, containing 2 paragraphs.
    Arguments:
        testClient:  The test client we test this for.
    '''
    del testClient
    text = ('this is a very nice text with 2 paragraphs. \n\n' + 
    'This is the second paragraph.')
    assert countParagraphs(text) == 2

def testCountParagraphsThree(testClient):
    '''
    Test the countParagraphs method, which counts the number of paragraphs where each paragraph is divided by 
    2 newline characters. Test this for a text with 3 paragraphs.
    Attributes:  
        text: The text we run the method on, containing 3 paragraphs.
    Arguments:
        testClient:  The test client we test this for.
    '''
    del testClient
    text = ('this is a very nice text with 3 paragraphs. \n\n' + 
    'This is the second paragraph. \n\n This is the third paragraph.' )
    assert countParagraphs(text) == 3

def testWordsSources(testClient, englishStopwords):
    '''
        Test the wordsSource method on a single string of words, which mimics a source text.
        Attributes: 
            text: The text we want to run the wordsSource method on. 
            wordsWoStopwordsExpected: The words set we expect to find. 
            wordsWoStopwords: The words set as we get from the wordsSource method.
        Arguments:
            testClient:  The test client we test this for.
            englishStopwords: English stopwords downloaded from nltk from conftest.py.
    '''
    del testClient
    text = ('This is some text, we take the words of, without punctuation.' + 
    ' We need to add some more useful information to this text.')
    wordsWoStopwordsExpected = {'take', 'words', 'need', 'information', 'without', 
    'add', 'useful', 'punctuation', 'text'}
    wordsWoStopwords = wordsSource(text, set(), englishStopwords)
    assert wordsWoStopwords == wordsWoStopwordsExpected

def testWordsSourcesMultiple(testClient, englishStopwords):
    '''
        Test the wordsSource method on two strings of words, which mimics two source texts.
        Attributes: 
            textFirst: The first text we want to run the wordsSource method on. 
            textSecond: The second text we want to run the wordsSource method on. 
            wordsWoStopwordsExpected: The words set we expect to find. 
            wordsWoStopwords: The words set as we get from the wordsSource method.
            wordsWoStopwordsInitial: Initial empty set of words, we put into the wordsSource method.
            wordsWoStopWordsExpectedSecond: The words set as we get from the wordsSource method, after the two texts.
        Arguments:
            testClient:  The test client we test this for.
            englishStopwords: English stopwords downloaded from nltk from conftest.py.
    '''
    del testClient
    wordsWoStopwordsInitial = set()
    textFirst = ('This is some text, we take the words of, without punctuation.' + 
    ' We need to add some more useful information to this text.')
    wordsWoStopwordsExpected = {'take', 'words', 'need', 'information', 'without', 
    'add', 'useful', 'punctuation', 'text'}
    wordsWoStopwords = wordsSource(textFirst, wordsWoStopwordsInitial, englishStopwords)
    assert wordsWoStopwords == wordsWoStopwordsExpected
    textSecond = ('This is the second text, we need to get some more words from this second text.' + 
    ' This text contains lots of interesting words, which are not in the stopwords set.')
    wordsWoStopWordsExpectedSecond = {'take', 'words', 'need', 'lots', 'second', 'contains', 
    'information', 'without', 'set', 'add', 'useful', 'punctuation', 'get', 'interesting', 'text', 'stopwords'}
    wordsWoStopwords = wordsSource(textSecond, wordsWoStopwords, englishStopwords)
    assert wordsWoStopWordsExpectedSecond == wordsWoStopwords

def testWordsText(testClient, englishStopwords):
    '''
        Test the wordsText method on a text of words, which mimics a source texts.
        Attributes: 
            text: The text we want to run the wordsSource method on.  
            expectedDictWords: the Dictionary we expect to get from this function. 
            wordsDict: The dictionary with words we get from this function. 
            count: Count of the number of words we get from the wordsText function.
        Arguments:
            testClient:  The test client we test this for.
            englishStopwords: English stopwords downloaded from nltk from conftest.py.
    '''
    del testClient
    text = ('This is some text, we take the words of, without punctuation.' + 
    ' We need to add some more useful information to this text. We add some more words to this text.')
    expectedDictWords = {'text': 3, 'take': 1, 'words': 2, 'without': 1, 'punctuation': 1, 'need': 1, 
    'add': 2, 'useful': 1, 'information': 1}
    wordsDict, count = wordsText(text, englishStopwords)
    assert count == 13
    assert wordsDict == expectedDictWords

def testWordsTextSecond(testClient, englishStopwords):
    '''
        Test the wordsText method on a small text, consisting of 1 paragraph.
        Attributes: 
            text: The text we want to run the wordsSource method on.  
            expectedDictWords: the Dictionary we expect to get from this function. 
            wordsDict: The dictionary with words we get from this function. 
            count: Count of the number of words we get from the wordsText function.
        Arguments:
            testClient:  The test client we test this for.
            englishStopwords: English stopwords downloaded from nltk from conftest.py.
    '''
    del testClient
    text = ('The most dedicated and well-organized community using these types of technology might be the Quantified-Self' +
    ' (QS) movement, seeking “self-knowledge through numbers”. This community of self-trackers and life-loggers experiments' +
    ' to find the best ways to collect data, and therefore insights, about themselves, and organizes "meetups" to share' +
    ' knowledge and experiences. However, much more people keep track of some information about themselves than these ‘hard-core’' +
    ' QS-users. In 2013, Fox and Duggan estimated that 69% of Americans keeps track of at least one health-related parameter for' +
    ' themselves or a loved one, and while no more recent numbers were found, we can imagine the rise in self-tracking technology' +
    ' has only increased this percentage.')
    expectedDictWords = {'dedicated': 1, 'wellorganized': 1, 'community': 2, 'using': 1, 'types': 1, 'technology': 2, 'might': 1, 
    'quantifiedself': 1, 'qs': 1, 'movement': 1, 'seeking': 1, 'selfknowledge': 1, 'numbers': 2, 'selftrackers': 1, 'lifeloggers': 1, 
    'experiments': 1, 'find': 1, 'best': 1, 'ways': 1, 'collect': 1, 'data': 1, 'therefore': 1, 'insights': 1, 'organizes': 1, 
    'meetups': 1, 'share': 1, 'knowledge': 1, 'experiences': 1, 'however': 1, 'much': 1, 'people': 1, 'keep': 1, 'track': 2, 
    'information': 1, 'hardcore': 1, 'qsusers': 1, '2013': 1, 'fox': 1, 'duggan': 1, 'estimated': 1, '69': 1, 'americans': 1, 
    'keeps': 1, 'least': 1, 'one': 2, 'healthrelated': 1, 'parameter': 1, 'loved': 1, 'recent': 1, 'found': 1, 'imagine': 1, 
    'rise': 1, 'selftracking': 1, 'increased': 1, 'percentage': 1}
    wordsDict, count = wordsText(text, englishStopwords)
    assert count == 60
    assert wordsDict == expectedDictWords

