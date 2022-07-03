from app.feedback.generateFeedback.IntegrationContentFeedback import IntegrationContentFeedback

def testCalcPercentageWordsUsed(testClient):
    '''
        Test the calcPercentageWordsUsed method, using a given wordsFromText dictionary, together with numWords 
        and using a wordsFromSources set. 
        Attributes:
            wordsFromText: Dictionary with words that mimics a small text, for which we test this method.
            numWords: The number of words inside this dictionary, it mimics the number of words in the text.
            wordsFromSources: Set of words, that mimics words that are retrieved from sources.
            percentage: Percentage of words in this wordsFromText dictionary that are also in the wordsFromSources set.
            feedbackObject: Object to create feedback for the source integration and content writing category.
        Arguments:
            testClient:  The test client we test this for.
    '''
    del testClient
    wordsFromText = {'text': 4, 'take': 1, 'words': 2, 'without': 1, 'punctuation': 1, 'need': 1, 
    'add': 2, 'useful': 2, 'information': 2}
    numWords = 16
    wordsFromSources = {'useful', 'information'}
    feedbackObject = IntegrationContentFeedback('', '', 1, 1, '')
    percentage = feedbackObject.calcPercentageWordsUsed(wordsFromText, wordsFromSources, numWords)
    assert percentage == 0.25

def testCalcScoreAndExplanationSourcesDownloadedZero(testClient):
    '''
        Test the calcScoreAndExplanationSourcesDownloaded method passing too little sources for the number of paragraphs.
        Attributes:
            numSources: The number of sources we test this method for. 
            numParagraphs: The number of paragraphs we test this method for.
            score: The score as retrieved from the calcScoreAndExplanationSourcesDownloaded method.
            explanation: The explanation as retrieved from the calcScoreAndExplanationSourcesDownloaded method.
            explanationText: The text manually set, we should retrieve from the method, to check against.
            feedbackObject: Object to create feedback for the source integration and content writing category.
        Arguments:
            testClient:  The test client we test this for.
    '''
    del testClient
    numSources = 2
    numParagraphs = 11
    explanationText = ('Your score for source integration and content is 0. You only used 2 sources ' + 
    'in 11 paragraphs of text. Try adding more sources.' )
    feedbackObject = IntegrationContentFeedback('', '', 1, 1, '')
    score, explanation = feedbackObject.calcScoreAndExplanationSourcesDownloaded(dict(), set(), 0, numSources, numParagraphs)
    assert score == 0
    assert explanation == explanationText

def testCalcScoreAndExplanationSourcesDownloadedNoSources(testClient):
    '''
        Test the calcScoreAndExplanationSourcesDownloaded method passing no sources.
        Attributes:
            numSources: The number of sources we test this method for. 
            numParagraphs: The number of paragraphs we test this method for.
            score: The score as retrieved from the calcScoreAndExplanationSourcesDownloaded method.
            explanation: The explanation as retrieved from the calcScoreAndExplanationSourcesDownloaded method.
            explanationText: The text manually set, we should retrieve from the method, to check against.
            feedbackObject: Object to create feedback for the source integration and content writing category.
        Arguments:
            testClient:  The test client we test this for.
    '''
    del testClient
    numSources = 0
    numParagraphs = 11
    explanationText = ('Your score for source integration and content is 0. You only used 0 sources ' + 
    'in 11 paragraphs of text. Try adding more sources.' )
    feedbackObject = IntegrationContentFeedback('', '', 1, 1, '')
    score, explanation = feedbackObject.calcScoreAndExplanationSourcesDownloaded(dict(), set(), 0, numSources, numParagraphs)
    assert score == 0
    assert explanation == explanationText

def testCalcScoreAndExplanationSourcesDownloadedHalf(testClient):
    '''
        Test the calcScoreAndExplanationSourcesDownloaded method passing too little sources for the number of paragraphs.
        Attributes:
            numSources: The number of sources we test this method for. 
            numParagraphs: The number of paragraphs we test this method for.
            score: The score as retrieved from the calcScoreAndExplanationSourcesDownloaded method.
            explanation: The explanation as retrieved from the calcScoreAndExplanationSourcesDownloaded method.
            explanationText: The text manually set, we should retrieve from the method, to check against.
            feedbackObject: Object to create feedback for the source integration and content writing category.
        Arguments:
            testClient:  The test client we test this for.
    '''
    del testClient
    numSources = 3
    numParagraphs = 13
    explanationText = ('Your score for source integration and content is 0.5. You only used 3 sources ' + 
    'in 13 paragraphs of text. Try adding more sources.' )
    feedbackObject = IntegrationContentFeedback('', '', 1, 1, '')
    score, explanation = feedbackObject.calcScoreAndExplanationSourcesDownloaded(dict(), set(), 0, numSources, numParagraphs)
    assert score == 0.5
    assert explanation == explanationText

def testCalcScoreAndExplanationSourcesDownloadedOne(testClient):
    '''
        Test the calcScoreAndExplanationSourcesDownloaded method passing too little sources for the number of paragraphs.
        Attributes:
            numSources: The number of sources we test this method for. 
            numParagraphs: The number of paragraphs we test this method for.
            score: The score as retrieved from the calcScoreAndExplanationSourcesDownloaded method.
            explanation: The explanation as retrieved from the calcScoreAndExplanationSourcesDownloaded method.
            explanationText: The text manually set, we should retrieve from the method, to check against.
            feedbackObject: Object to create feedback for the source integration and content writing category.
        Arguments:
            testClient:  The test client we test this for.
    '''
    del testClient
    numSources = 4
    numParagraphs = 13
    explanationText = ('Your score for source integration and content is 1. You only used 4 sources ' + 
    'in 13 paragraphs of text. Try adding more sources.' )
    feedbackObject = IntegrationContentFeedback('', '', 1, 1, '')
    score, explanation = feedbackObject.calcScoreAndExplanationSourcesDownloaded(dict(), set(), 0, numSources, numParagraphs)
    assert score == 1
    assert explanation == explanationText

def testCalcScoreAndExplanationSourcesDownloadedPercentageOne(testClient):
    '''
        Test the calcScoreAndExplanationSourcesDownloaded method passing enough sources, so calculating the percentage of words used. 
        Attributes:
            numSources: The number of sources we test this method for. 
            numParagraphs: The number of paragraphs we test this method for.
            wordsFromText: Dictionary with words that mimics a small text, for which we test this method.
            numWords: The number of words inside this dictionary, it mimics the number of words in the text.
            wordsFromSources: Set of words, that mimics words that are retrieved from sources.
            score: The score as retrieved from the calcScoreAndExplanationSourcesDownloaded method.
            explanation: The explanation as retrieved from the calcScoreAndExplanationSourcesDownloaded method.
            explanationText: The text manually set, we should retrieve from the method, to check against.
            feedbackObject: Object to create feedback for the source integration and content writing category.
        Arguments:
            testClient:  The test client we test this for.
    '''
    del testClient
    numSources = 2
    numParagraphs = 2
    wordsFromText = {'text': 4, 'take': 1, 'words': 2, 'without': 1, 'punctuation': 1, 'need': 1, 
    'add': 2, 'useful': 2, 'information': 2}
    numWords = 16
    wordsFromSources = {'useful', 'information'}
    explanationText =  (f'Your score for source integration and content is 10.0. You used 2 sources ' + 
    'in 2 paragraphs of text. You used 25.0% of the words used in the sources in your text. ' +  
    'This gives a perfect score, you could try adding more words used in the sources in your text.')
    feedbackObject = IntegrationContentFeedback('', '', 1, 1, '')
    score, explanation = feedbackObject.calcScoreAndExplanationSourcesDownloaded(wordsFromText, wordsFromSources, 
        numWords, numSources, numParagraphs)
    assert score == 10
    assert explanation == explanationText

def testCalcScoreAndExplanationSourcesDownloadedPercentageTwo(testClient):
    '''
        Test the calcScoreAndExplanationSourcesDownloaded method passing enough sources, so calculating the percentage of words used. 
        Attributes:
            numSources: The number of sources we test this method for. 
            numParagraphs: The number of paragraphs we test this method for.
            wordsFromText: Dictionary with words that mimics a small text, for which we test this method.
            numWords: The number of words inside this dictionary, it mimics the number of words in the text.
            wordsFromSources: Set of words, that mimics words that are retrieved from sources.
            score: The score as retrieved from the calcScoreAndExplanationSourcesDownloaded method.
            explanation: The explanation as retrieved from the calcScoreAndExplanationSourcesDownloaded method.
            explanationText: The text manually set, we should retrieve from the method, to check against.
            feedbackObject: Object to create feedback for the source integration and content writing category.
        Arguments:
            testClient:  The test client we test this for.
    '''
    del testClient
    numSources = 2
    numParagraphs = 2
    wordsFromText = {'text': 4, 'take': 1, 'words': 2, 'without': 1, 'punctuation': 1, 'need': 1, 
    'add': 2, 'useful': 2, 'information': 2}
    numWords = 16
    wordsFromSources = {'information'}
    explanationText =  ('Your score for source integration and content is 5.5. You used 2 sources ' + 
    'in 2 paragraphs of text. You used 12.5% of the words used in the sources in your text. ' +  
    'For a higher score, you could try adding more words used in the sources in your text.')
    feedbackObject = IntegrationContentFeedback('', '', 1, 1, '')
    score, explanation = feedbackObject.calcScoreAndExplanationSourcesDownloaded(wordsFromText, wordsFromSources, 
        numWords, numSources, numParagraphs)
    assert score == 5.5
    assert explanation == explanationText

def testCalcScoreAndExplanationSourcesDownloadedPercentageThree(testClient):
    '''
        Test the calcScoreAndExplanationSourcesDownloaded method passing enough sources, so calculating the percentage of words used.
        Getting a percentage more than the max score that is 10. 
        Attributes:
            numSources: The number of sources we test this method for. 
            numParagraphs: The number of paragraphs we test this method for.
            wordsFromText: Dictionary with words that mimics a small text, for which we test this method.
            numWords: The number of words inside this dictionary, it mimics the number of words in the text.
            wordsFromSources: Set of words, that mimics words that are retrieved from sources.
            score: The score as retrieved from the calcScoreAndExplanationSourcesDownloaded method.
            explanation: The explanation as retrieved from the calcScoreAndExplanationSourcesDownloaded method.
            explanationText: The text manually set, we should retrieve from the method, to check against.
            feedbackObject: Object to create feedback for the source integration and content writing category.
        Arguments:
            testClient:  The test client we test this for.
    '''
    del testClient
    numSources = 2
    numParagraphs = 2
    wordsFromText = {'text': 4, 'take': 1, 'words': 2, 'without': 1, 'punctuation': 1, 'need': 1, 
    'add': 2, 'useful': 2, 'information': 2}
    numWords = 16
    wordsFromSources = {'information', 'add', 'useful'}
    explanationText =  ('Your score for source integration and content is 10. You used 2 sources ' + 
    'in 2 paragraphs of text. You used 37.5% of the words used in the sources in your text. ' +  
    'This gives a perfect score, you could try adding more words used in the sources in your text.')
    feedbackObject = IntegrationContentFeedback('', '', 1, 1, '')
    score, explanation = feedbackObject.calcScoreAndExplanationSourcesDownloaded(wordsFromText, wordsFromSources, 
        numWords, numSources, numParagraphs)
    assert score == 10
    assert explanation == explanationText

def testGetWordsSources(testClient):
    '''
        Test the getWordsSources method and implicitly test the textDoi method.
        Attributes:
            links_doi: List with links containing doi links for this test.
            links: List containing a link for this test.
            userId: Temporary userId.
            words: The wordslist set as retrieved from the getWordsSources method.
            numSources: The number of sources the getWordsSources method was able to retrieve the words from.
            expectedWords: The set of words we want to find, so we compare against.
            feedbackObject: Object to create feedback for the source integration and content writing category.
        Arguments:
            testClient:  The test client we test this for.
    '''
    del testClient
    links_doi = ['https://doi.org/10.1103/PhysRev.82.554.2']
    links = ['https://www2.latech.edu/~acm/helloworld/python.html']
    userId = 123
    feedbackObject = IntegrationContentFeedback('', '', 1, userId, '')
    words, numSources = feedbackObject.getWordsSources(links, links_doi)
    expectedWords = {'q', 'iz0', 'target', '183612005', 'ithe', 'germany', 'fine', '200i', 'i2w', 'initial', 'equivalent', 'smith', 'bd', 
    'holloway', '372', 'field', 'al', 'b', '81', '0', 'group', 'soc', 'moore', '120', 'program', 'barut', 'mass', 'hello', 'l4', 'aparticles', 
    'b8', 'equal', 'changes', 'exact', 'lsl', 'bombard', 'submitted', 'normal', 'id4', 'lauritsen', '273020', 'proc', 'may', 'nuclei', '2b', 
    'brookhaven', '96', 'eoociclit', 'bethe', 'erratum', 'movable', 'bombarding', 'present', '2oc', 'areas', 'percent', 'ci2d', 'friedrich', 
    'p0have', 'properties', '847', 'et', 'c', 'excited', 'python', '1519015', 'onr', 'procedure', 'peaks', 'g', 'lenz', 'oeo', 'unpublished', 
    'six', 'laboratory', 'assisted', '4x', 'approximately', 'f0', 'joint', 'groundstate', 'masses', 'phil', 'world', 'ii', 'rev', 'mev', 'counter', 
    'cambridge', 'boron', 'charge', 'first', 'vs', '298', 'made', 'proportional', 'band', 'rhv', '150', 'using', 'formulas', 'thus', '274t', 'note', 
    'mevabsorbing', 'nparticles', 'letter', 'spacecharge', 'w', 'velocities', 'proton', '8', 'range', 'ratio', 'h', 'whaling', 'bnlt7', 'print', 
    'peak', 'ground', 'voltow', 'current', 'bii', '2', '80', 'saturation', 'value', 'state', 'phys', 'dsseldorf', 'aparticle', 'two', 'haling', 
    'moving', 'li', 'national', 'z', '35', '4d', 'ioooz', 'fig', 'partial', 'lal', 'murrell', '4', 'e', 'letters', 'l', '1', 'cm', 'heights', 
    'number', 'gross', 'n', 'intensities', 'groups', 'atomic', 'aec', 'piling', 'cathode', '095020', 'fowler', '2e', 'true', 'pc', 'l2', 
    'energy', 'oied', 'conditions', 'protons', 'interest', 'air', 'converting', 'vl', 'diodes', 'read', 'determined', 'reaction', 'abe', 
    '78', 'electron', 'tollestrop', '58', 'foils', 'negligible'}
    assert words == expectedWords
    assert numSources == 2

def testSourceIntegarationCorrect(testClient, englishStopwords):
    '''
        Test the combined sourceIntegration method, on a toy text and toy references.
         Attributes:
            references: Toy references string to test this method on.
            text: 'Toy text to test this method on.
            userId: Temporary userId.
            score: Score as retrieved from the sourceIntegration method.
            explanation: explanation as retrieved from the sourceIntegration method.
            explanationText: Expected explanation text as retrieved from the sourceIntegration method.
            feedbackObject: Object to create feedback for the source integration and content writing category.
        Arguments:
            testClient:  The test client we test this for.
    '''
    del testClient, englishStopwords
    userId = 123
    references = 'https://www2.latech.edu/~acm/helloworld/python.html \n\n https://doi.org/10.1103/PhysRev.82.554.2'
    text = 'This is a very nice text with a single paragraph, which is of course a negligible text.'
    feedbackObject = IntegrationContentFeedback(text, references, 1, userId, '')
    score, explanation = feedbackObject.genFeedback()
    explanationText =  ('Your score for source integration and content is 6.14. You used 2 sources ' + 
    'in 1 paragraphs of text. You used 14.29% of the words used in the sources in your text. ' +  
    'For a higher score, you could try adding more words used in the sources in your text.')
    assert score == 6.14
    assert explanation == [[-1, 1, -1, -1, 3, explanationText, '', []]]
    assert feedbackObject.explanation == explanationText

def testSourceIntegarationWrong(testClient):
    '''
        Test the combined sourceIntegration method, on a toy text and toy references, which is a reference without a link.
        Attributes:
            references: Toy references string to test this method on.
            text: 'Toy text to test this method on.
            userId: Temporary userId.
            score: Score as retrieved from the sourceIntegration method.
            explanation: explanation as retrieved from the sourceIntegration method.
            explanationText: Expected explanation text as retrieved from the sourceIntegration method.
            feedbackObject: Object to create feedback for the source integration and content writing category.
        Arguments:
            testClient:  The test client we test this for.
    '''
    del testClient
    userId = 123
    references = 'This is a reference'
    text = 'This is a very nice text with a single paragraph, which is of course a negligible text.'
    feedbackObject = IntegrationContentFeedback(text, references, 1, userId, '')
    score, explanation = feedbackObject.genFeedback()
    explanationText = ('Your score for source integration and content is 10. You only used 1 sources ' + 
    'in 1 paragraphs of text. Try adding more sources. Writing Dashboard Could not check if text from the sources ' + 
    'are actually used in the text.' )
    assert score == 10
    assert explanation == [[-1, 1, -1, -1, 3, explanationText, '', []]]
    assert feedbackObject.explanation == explanationText

def testDoiDownloadUnsuccessful(testClient):
    '''
        Test if we get an empty string if we retrieve the text from a paper using the textDoi method, 
        using an url on which a paper can not be correctly downloaded.
        Attributes:
            userId: Temporary userId.
            feedbackObject: Object to create feedback for the source integration and content writing category.
            doi: link to this doi paper, from which we can not successfully retrieve this paper and text.
        Arguments:
            testClient:  The test client we test this for.
    '''
    del testClient
    userId = 123
    feedbackObject = IntegrationContentFeedback('', '', 1, userId, '')
    doi = 'https://doi.org/10.1007/s12555-018-0134-6'
    text = feedbackObject.textDoi(doi)
    assert text == ''