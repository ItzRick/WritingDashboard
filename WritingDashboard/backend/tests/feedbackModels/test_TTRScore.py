from app.feedback.generateFeedback.CohesionFeedback import CohesionFeedback
from string import ascii_lowercase

'''
    The following tests concern the function getTTRscore. 
    Within this function, all elements become lemmatized. 
    I.e. "cool", "cooler", "coolest" are all converted to "cool".
    The function then calculates the score by dividing the number 
    of unique tokens by the windowsize, in which tokens are words
    and windowsize is 50 or if there are less than 50 tokens, the
    number of tokens.
'''
def testTTRSpace(testClient, downloadNltk):
    '''
        Test if a text with only a space character returns None.
        Arguments: 
            testClient: The test client we test this for.
            downloadNltk: Function needed to download nltk corpora used in this
                    method.
        Attributes: 
            score: The score given for the TTR score.
    '''
    del testClient, downloadNltk
    feedbackObject = CohesionFeedback(' ', '', 1, 1, '')
    score = feedbackObject.getTTRScore(" ")
    assert score == None

def testTTRZeroWords(testClient, downloadNltk):
    '''
        Test if a text with zero words returns None.
        Arguments: 
            testClient: The test client we test this for.
            downloadNltk: Function needed to download nltk corpora used in this
                    method.
        Attributes: 
            score: The score given for the TTR score.
    '''
    del testClient, downloadNltk
    feedbackObject = CohesionFeedback('', '', 1, 1, '')
    score = feedbackObject.getTTRScore("")
    assert score == None

def testTTRSentenceWithMinScore(testClient, downloadNltk):
    '''
        Test if a sentence with only similar elements has the correct score and
        returns correct most used words.
        The score should be 1/total number of words*10 rounded to 2 decimals.
        So in this case, for 3 words that is 1/3*10 = 3.33. 
        Since the sentence only has one similar element, this should be the 
        most used word.
        Arguments: 
            testClient: The test client we test this for.
            downloadNltk: Function needed to download nltk corpora used in this
                    method.
        Attributes: 
            text: Input text for the test.
            score: The score given for the TTR score.
    '''
    del testClient, downloadNltk
    text = "Big bigger biggest."
    feedbackObject = CohesionFeedback(text, '', 1, 1, '')
    score = feedbackObject.getTTRScore(text)
    assert score == (3.33, ["big"])

def testTTRTextWithMinScore(testClient, downloadNltk):
    '''
        Test if a text with only similar elements has the correct score and 
        returns correct most used words.
        The score should be 1/total number of words*10 rounded to 2 decimals.
        So in this case, for 10 words that is 1/10*10 = 10.0. 
        Since the sentence only has one similar element, this should be the 
        most used word.
        Arguments: 
            testClient: The test client we test this for.
            downloadNltk: Function needed to download nltk corpora used in this
                    method.
        Attributes: 
            text: Input text for the test.
            score: The score given for the TTR score.
    '''
    del testClient, downloadNltk
    text = ("Big bigger biggest. Bigger. Biggest. Big bigger. Bigger biggest "
        "big!")
    feedbackObject = CohesionFeedback(text, '', 1, 1, '')
    score = feedbackObject.getTTRScore(text)
    assert score == (1.0, ["big"])

def testTTRSentenceWithMaxScore(testClient, downloadNltk):
    '''
        Test if a sentence with only unique elements has the maximum score, 
        this is 10.0, and returns correct most used words.
        Since every word in the sentence is unique, this should be the first
        3 words (lematized).
        Arguments: 
            testClient: The test client we test this for.
            downloadNltk: Function needed to download nltk corpora used in this
                    method.
        Attributes: 
            text: Input text for the test.
            score: The score given for the TTR score.
    '''
    del testClient, downloadNltk
    text = "He is a very unique animal."
    feedbackObject = CohesionFeedback(text, '', 1, 1, '')
    score = feedbackObject.getTTRScore(text)
    assert score == (10.0, ["he", "be", "a"])

def testTTRTextWithMaxScore(testClient, downloadNltk):
    '''
        Test if a text with only unique elements has the maximum score,
        this is 10.0, and returns correct most used words.
        Since every word in the text is unique, this is should be the first
        3 words (lematized).
        Arguments: 
            testClient: The test client we test this for.
            downloadNltk: Function needed to download nltk corpora used in this
                    method.
        Attributes: 
            text: Input text for the test.
            score: The score given for the TTR score.
    '''
    del testClient, downloadNltk
    text = ("He is a very unique animal. That shows amazing results. No wonder"
        " they exist in here.")
    feedbackObject = CohesionFeedback(text, '', 1, 1, '')
    score = feedbackObject.getTTRScore(text)
    assert score == (10.0, ["he", "be", "a"])

def testTTRSingleSentence(testClient, downloadNltk):
    '''
        Test if a simple text of one sentence returns the correct score
        and returns the correct most used words.
        The sentence contains "big" and "bigger", which both get lematized to 
        "big" and thus together count as one unique token. 
        The sentence contains "are" and "is", which both get lematized to "be"
        and thus together count as one unique token.
        This means that there are 2 less unique tokens than there are total 
        tokens.
        Hence, the score should be (10-2)/10*10=8.0.
        The correct most used words should thus be these two lematized tokens 
        ("be" and "big") and then the first token (which is not one of these
        two).
        Arguments: 
            testClient: The test client we test this for.
            downloadNltk: Function needed to download nltk corpora used in this
                    method.
        Attributes: 
            text: Input text for the test.
            score: The score given for the TTR score.
    '''
    del testClient, downloadNltk
    text = "They are very big and that person is also bigger."
    feedbackObject = CohesionFeedback(text, '', 1, 1, '')
    score = feedbackObject.getTTRScore(text)
    assert score == (8.0, ["be", "big", "they"])

def testTTRThreeSentences(testClient, downloadNltk):
    '''
        Test if a simple text of three sentences returns the correct score
        and returns the correct most used words.
        The sentences contain "big", "bigger" and "biggest", which all get
        lematized to "big" and thus together count as one unique token. 
        The sentences contain "are", "is" and "is", which all get lematized to
        "be" and thus together count as one unique token.
        This means that there are 4 less unique tokens than there are total
        tokens.
        Hence, the score should be (12-4)/12*10=8.0.
        The correct most used words should thus be these two lematized tokens 
        ("be" and "big") and then the first token (which is not one of these 
        two).
        Arguments: 
            testClient: The test client we test this for.
            downloadNltk: Function needed to download nltk corpora used in this
                    method.
        Attributes: 
            text: Input text for the test.
            score: The score given for the TTR score.
    '''
    del testClient, downloadNltk
    text = "They are very big. That person is bigger. He is the biggest."
    feedbackObject = CohesionFeedback(text, '', 1, 1, '')
    score = feedbackObject.getTTRScore(text)
    assert score == (round(8/12*10,2), ["be", "big", "they"])

def testTTRWindowsizeMinScore(testClient, downloadNltk): 
    '''
        Test if a text with a windowsize bigger than 50 still gets the 
        correct score despite the text after the 50 similar words containing
        different words and returns the correct most used words. 
        This text has 57 tokens, thus 8 windows of 50. The number of unique
        tokens is 1 in the first two windows and after this each window
        contains one more unique word. 
        Hence, the score should be (1+1+2+3+4+5+6+7)/8/50*10.
        The correct most used words are then the oftenly repeated word and then
        the first two other tokens.
        Arguments: 
            testClient: The test client we test this for.
            downloadNltk: Function needed to download nltk corpora used in this
                    method.
        Attributes: 
            text: Input text for the test.
            score: The score given for the TTR score.
    '''
    del testClient, downloadNltk
    text = "big "*51 + "hello this is a different text"
    feedbackObject = CohesionFeedback(text, '', 1, 1, '')
    score = feedbackObject.getTTRScore(text)
    assert score == (round((1+1+2+3+4+5+6+7)/8/5,2), ["big", "hello", "this"])

def testTTRWindowsizeMaxScore(testClient, downloadNltk): 
    '''
        Test if a text with a windowsize bigger than 50 still gets the 
        correct score despite the text after the 50 different words containing
        similar words and returns the correct most used words. 
        This text has 26*26+10=686 words, thus 637 windows. The number of 
        unique tokens is 50 in the first 627 windows and for the last then it 
        has one less each window. 
        Hence, the score should be 9.98 (same calculation as last test).
        And the correct most used words.
    '''
    del testClient, downloadNltk
    text = ""
    for first_letter in ascii_lowercase:
        for second_letter in ascii_lowercase:
            text += first_letter + second_letter + " "
    text += "big "*10
    feedbackObject = CohesionFeedback(text, '', 1, 1, '')
    score = feedbackObject.getTTRScore(text)
    assert score == (9.98, ["big", "be", "aa"])
