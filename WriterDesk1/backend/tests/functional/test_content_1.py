from app.feedback.generateFeedback.IntegrationContentFeedback import IntegrationContentFeedback
from math import ceil

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
    feedbackObject = IntegrationContentFeedback(text, '', 1, 1, '')
    assert feedbackObject.countParagraphs(text) == 1

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
    feedbackObject = IntegrationContentFeedback(text, '', 1, 1, '')
    assert feedbackObject.countParagraphs(text) == 2

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
    feedbackObject = IntegrationContentFeedback(text, '', 1, 1, '')
    assert feedbackObject.countParagraphs(text) == 3

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
    feedbackObject = IntegrationContentFeedback(text, '', 1, 1, '')
    wordsWoStopwords = feedbackObject.wordsSource(text, set())
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
    feedbackObject = IntegrationContentFeedback('', '', 1, 1, '')
    wordsWoStopwords = feedbackObject.wordsSource(textFirst, wordsWoStopwordsInitial)
    assert wordsWoStopwords == wordsWoStopwordsExpected
    textSecond = ('This is the second text, we need to get some more words from this second text.' + 
    ' This text contains lots of interesting words, which are not in the stopwords set.')
    wordsWoStopWordsExpectedSecond = {'take', 'words', 'need', 'lots', 'second', 'contains', 
    'information', 'without', 'set', 'add', 'useful', 'punctuation', 'get', 'interesting', 'text', 'stopwords'}
    wordsWoStopwords = feedbackObject.wordsSource(textSecond, wordsWoStopwordsInitial)
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
    feedbackObject = IntegrationContentFeedback(text, '', 1, 1, '')
    wordsDict, count = feedbackObject.wordsText(text)
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
    feedbackObject = IntegrationContentFeedback(text, '', 1, 1, '')
    wordsDict, count = feedbackObject.wordsText(text)
    assert count == 60
    assert wordsDict == expectedDictWords

def testGetUrlSources(testClient):
    '''
        Test the getUrlsSources method, using a sample sources string, where each string is divided by 2 whitespace characters.
        Attributes: 
            sources: String with the example sources, each source separated by 2 whitespace characters. 
            links: The links as retrieved from the getUrlsSources method.
            links_doi: The links containing doi.org as retrieved from the getUrlsSources method.
            numSources: The number of sources inside the sources string, as retrieved from the getUrlsSources method.
        Arguments:
            testClient:  The test client we test this for.
    '''
    del testClient
    sources = ('Cambridge Dictionary. (2021c, june 2). multitasking definition: 1. a person’s ability to do more than one thing' +
    ' at a time: 2. the ability of a computer to operate. . .. Learn more. Cambridge University.' +
    ' https://dictionary.cambridge.org/dictionary/english/multitasking \n\n  Uncapher, M. R., & Wagner, A. D. (2018).' +
    ' Minds and brains of media multitaskers: Current findings - and future directions. Proceedings of the National Academy' +
    ' of Sciences, 115(40), 9889–9896. https://doi.org/10.1073/pnas.1611612115')
    feedbackObject = IntegrationContentFeedback('', '', 1, 1, '')
    links, links_doi, numSources = feedbackObject.getUrlsSources(sources)
    assert links == ['https://dictionary.cambridge.org/dictionary/english/multitasking']
    assert links_doi == ['https://doi.org/10.1073/pnas.1611612115']
    assert numSources == 2

def testCalcScoreAndExplanationSourcesNotDownloadedZero(testClient):
    '''
        Test of the calcScoreAndExplanationSourcesNotDownloaded method, while giving numSources and numParagraphs.
        This is for a number of sources and number of paragraphs that gives a score 0. We also test the explanation.
        Attributes: 
            numSources: The number of sources we test this method for. 
            numParagraphs: The number of paragraphs we test this method for.
            score: The score as retrieved from the calcScoreAndExplanationSourcesNotDownloaded method.
            explanation: The explanation as retrieved from the calcScoreAndExplanationSourcesNotDownloaded method.
            explanationText: The text manually set, we should retrieve from the method, to check against.
        Arguments:
            testClient:  The test client we test this for.
    '''
    del testClient
    numSources = 2
    numParagraphs = 11
    # Assert that we should indeed get a score of 0:
    assert ceil(numParagraphs / numSources) > 5
    feedbackObject = IntegrationContentFeedback('', '', 1, 1, '')
    score, explanation = feedbackObject.calcScoreAndExplanationSourcesNotDownloaded(numSources, numParagraphs)
    assert score == 0
    explanationText = ('Your score for source integration and content is 0. You only used 2 sources ' + 
    'in 11 paragraphs of text. Try adding more sources. Writing Dashboard Could not check if text from the sources ' + 
    'are actually used in the text.' )
    assert explanation == explanationText

def testCalcScoreAndExplanationSourcesNotDownloadedNoSources(testClient):
    '''
        Test of the calcScoreAndExplanationSourcesNotDownloaded method, while giving numSources and numParagraphs.
        This is for no sources, so we will get a score 0. We also test the explanation.
        Attributes: 
            numSources: The number of sources we test this method for. 
            numParagraphs: The number of paragraphs we test this method for.
            score: The score as retrieved from the calcScoreAndExplanationSourcesNotDownloaded method.
            explanation: The explanation as retrieved from the calcScoreAndExplanationSourcesNotDownloaded method.
            explanationText: The text manually set, we should retrieve from the method, to check against.
        Arguments:
            testClient:  The test client we test this for.
    '''
    del testClient
    numSources = 0
    numParagraphs = 11
    feedbackObject = IntegrationContentFeedback('', '', 1, 1, '')
    score, explanation = feedbackObject.calcScoreAndExplanationSourcesNotDownloaded(numSources, numParagraphs)
    assert score == 0
    explanationText = ('Your score for source integration and content is 0. You only used 0 sources ' + 
    'in 11 paragraphs of text. Try adding more sources. Writing Dashboard Could not check if text from the sources ' + 
    'are actually used in the text.' )
    assert explanation == explanationText

def testCalcScoreAndExplanationSourcesNotDownloadedTwo(testClient):
    '''
        Test of the calcScoreAndExplanationSourcesNotDownloaded method, while giving numSources and numParagraphs.
        This is for a number of sources and number of paragraphs that gives a score 2. We also test the explanation.
        Attributes: 
            numSources: The number of sources we test this method for. 
            numParagraphs: The number of paragraphs we test this method for.
            score: The score as retrieved from the calcScoreAndExplanationSourcesNotDownloaded method.
            explanation: The explanation as retrieved from the calcScoreAndExplanationSourcesNotDownloaded method.
            explanationText: The text manually set, we should retrieve from the method, to check against.
        Arguments:
            testClient:  The test client we test this for.
    '''
    del testClient
    numSources = 3
    numParagraphs = 13
    # Assert that we should indeed get a score of 2:
    assert ceil(numParagraphs / numSources) > 4
    feedbackObject = IntegrationContentFeedback('', '', 1, 1, '')
    score, explanation = feedbackObject.calcScoreAndExplanationSourcesNotDownloaded(numSources, numParagraphs)
    assert score == 2
    explanationText = ('Your score for source integration and content is 2. You only used 3 sources ' + 
    'in 13 paragraphs of text. Try adding more sources. Writing Dashboard Could not check if text from the sources ' + 
    'are actually used in the text.' )
    assert explanation == explanationText

def testCalcScoreAndExplanationSourcesNotDownloadedFour(testClient):
    '''
        Test of the calcScoreAndExplanationSourcesNotDownloaded method, while giving numSources and numParagraphs.
        This is for a number of sources and number of paragraphs that gives a score 4. We also test the explanation.
        Attributes: 
            numSources: The number of sources we test this method for. 
            numParagraphs: The number of paragraphs we test this method for.
            score: The score as retrieved from the calcScoreAndExplanationSourcesNotDownloaded method.
            explanation: The explanation as retrieved from the calcScoreAndExplanationSourcesNotDownloaded method.
            explanationText: The text manually set, we should retrieve from the method, to check against.
        Arguments:
            testClient:  The test client we test this for.
    '''
    del testClient
    numSources = 4
    numParagraphs = 13
    # Assert that we should indeed get a score of 4:
    assert ceil(numParagraphs / numSources) > 3
    feedbackObject = IntegrationContentFeedback('', '', 1, 1, '')
    score, explanation = feedbackObject.calcScoreAndExplanationSourcesNotDownloaded(numSources, numParagraphs)
    assert score == 4
    explanationText = ('Your score for source integration and content is 4. You only used 4 sources ' + 
    'in 13 paragraphs of text. Try adding more sources. Writing Dashboard Could not check if text from the sources ' + 
    'are actually used in the text.' )
    assert explanation == explanationText

def testCalcScoreAndExplanationSourcesNotDownloadedSix(testClient):
    '''
        Test of the calcScoreAndExplanationSourcesNotDownloaded method, while giving numSources and numParagraphs.
        This is for a number of sources and number of paragraphs that gives a score 6. We also test the explanation.
        Attributes: 
            numSources: The number of sources we test this method for. 
            numParagraphs: The number of paragraphs we test this method for.
            score: The score as retrieved from the calcScoreAndExplanationSourcesNotDownloaded method.
            explanation: The explanation as retrieved from the calcScoreAndExplanationSourcesNotDownloaded method.
            explanationText: The text manually set, we should retrieve from the method, to check against.
        Arguments:
            testClient:  The test client we test this for.
    '''
    del testClient
    numSources = 6
    numParagraphs = 13
    # Assert that we should indeed get a score of 6:
    assert ceil(numParagraphs / numSources) > 2
    feedbackObject = IntegrationContentFeedback('', '', 1, 1, '')
    score, explanation = feedbackObject.calcScoreAndExplanationSourcesNotDownloaded(numSources, numParagraphs)
    assert score == 6
    explanationText = ('Your score for source integration and content is 6. You only used 6 sources ' + 
    'in 13 paragraphs of text. Try adding more sources. Writing Dashboard Could not check if text from the sources ' + 
    'are actually used in the text.' )
    assert explanation == explanationText

def testCalcScoreAndExplanationSourcesNotDownloadedEight(testClient):
    '''
        Test of the calcScoreAndExplanationSourcesNotDownloaded method, while giving numSources and numParagraphs.
        This is for a number of sources and number of paragraphs that gives a score 8. We also test the explanation.
        Attributes: 
            numSources: The number of sources we test this method for. 
            numParagraphs: The number of paragraphs we test this method for.
            score: The score as retrieved from the calcScoreAndExplanationSourcesNotDownloaded method.
            explanation: The explanation as retrieved from the calcScoreAndExplanationSourcesNotDownloaded method.
            explanationText: The text manually set, we should retrieve from the method, to check against.
        Arguments:
            testClient:  The test client we test this for.
    '''
    del testClient
    numSources = 10
    numParagraphs = 11
    # Assert that we should indeed get a score of 8:
    assert ceil(numParagraphs / numSources) > 1
    feedbackObject = IntegrationContentFeedback('', '', 1, 1, '')
    score, explanation = feedbackObject.calcScoreAndExplanationSourcesNotDownloaded(numSources, numParagraphs)
    assert score == 8
    explanationText = ('Your score for source integration and content is 8. You only used 10 sources ' + 
    'in 11 paragraphs of text. Try adding more sources. Writing Dashboard Could not check if text from the sources ' + 
    'are actually used in the text.' )
    assert explanation == explanationText

def testCalcScoreAndExplanationSourcesNotDownloadedTen(testClient):
    '''
        Test of the calcScoreAndExplanationSourcesNotDownloaded method, while giving numSources and numParagraphs.
        This is for a number of sources and number of paragraphs that gives a score 10. We also test the explanation.
        Attributes: 
            numSources: The number of sources we test this method for. 
            numParagraphs: The number of paragraphs we test this method for.
            score: The score as retrieved from the calcScoreAndExplanationSourcesNotDownloaded method.
            explanation: The explanation as retrieved from the calcScoreAndExplanationSourcesNotDownloaded method.
            explanationText: The text manually set, we should retrieve from the method, to check against.
        Arguments:
            testClient:  The test client we test this for.
    '''
    del testClient
    numSources = 12
    numParagraphs = 11
    # Assert that we should indeed get a score of 10:
    assert ceil(numParagraphs / numSources) > 0
    feedbackObject = IntegrationContentFeedback('', '', 1, 1, '')
    score, explanation = feedbackObject.calcScoreAndExplanationSourcesNotDownloaded(numSources, numParagraphs)
    assert score == 10
    explanationText = ('Your score for source integration and content is 10. You only used 12 sources ' + 
    'in 11 paragraphs of text. Try adding more sources. Writing Dashboard Could not check if text from the sources ' + 
    'are actually used in the text.' )
    assert explanation == explanationText


