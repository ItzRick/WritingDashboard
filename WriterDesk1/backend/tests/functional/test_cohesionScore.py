from app.getTTRScore import getTTRScore
from app.getConnectiveScore import getConnectiveScore




'''
    The following tests concern the function getTTRscore. 
    Within this function, all elements become lemmatized. 
    I.e. "cool", "cooler", "coolest" are all converted to "cool".
    The function then calculates the score by dividing the number 
    of unique tokens by the windowsize, in which tokens are words
    and windowsize is the number of tokens/words within the text.
'''

def test_ttr_zero_words():
    '''
        Test if a text with zero words returns None.
    '''
    score = getTTRScore('')
    assert score == None

def test_ttr_sentence_with_min_score():
    '''
        Test if a sentence with only similar elements has minimum score, so None.
    '''
    text = ('Big bigger biggest.')
    score = getTTRScore(text)
    assert score == None

def test_ttr_text_with_min_score():
    '''
        Test if a text with only similar elements has minimum score, so None.
    '''
    text = ('Big bigger biggest. Bigger. Biggest. Big bigger. Bigger biggest big!')
    score = getTTRScore(text)
    assert score == None

def test_ttr_sentence_with_max_score():
    '''
        Test if a sentence with only unique elements has maximum score, so None.
    '''
    text = ('He is a very unique animal.')
    score = getTTRScore(text)
    assert score == 10

def test_ttr_text_with_max_score():
    '''
        Test if a text with only unique elements has maximum score, so None.
    '''
    text = ('He is a very unique animal. That shows amazing results. No wonder that they exist in here.')
    score = getTTRScore(text)
    assert score == 10

def test_ttr_single_sentence():
    '''
        Test if a simple text of one sentence returns the correct score.
        The sentence contains "big" and "bigger", and "are" and "is".
        Hence, the score should be (10-4)/10=0.6
    '''
    text = ('They are very big and that person is also bigger.')
    score = getTTRScore(text)
    assert score == 0.6

def test_ttr_three_sentences():
    '''
        Test if a simple text of three sentences returns the correct score.
        The sentences contain "big", "bigger" and "biggest", and "are", "is" and "is".
        Hence, the score should be (12-6)/12=0.5
    '''
    text = ('They are very big. That person is bigger. He is the biggest.')
    score = getTTRScore(text)
    assert score == 0.5




'''
    The following tests concern the function getConnectiveScore. 
    Within this function, the number of connectives are looked into.
    The number of connectives used in a text are divided by the 
    total number of tokens (words) in a text. This number is then
    inserted into a 2nd order polynomial to achieve a score. 
'''

def test_con_zero_words():
    '''
        Test if a text with zero words returns None.
    '''
    score = getConnectiveScore('')
    assert score == None

def test_con_three_sentences():
    '''
        Test if a simple text of three sentences returns the correct score.
        The sentences do not contain any connectives, so it should return 0.
    '''
    text = ('They are very big. That person is bigger. He is the biggest.')
    score = getConnectiveScore(text)
    assert score == 0

def test_con_one_sentence_single_connective():
    '''
        Test if a single sentence with a single connective returns
        the correct score. There is one connective and nine
        words within the sentence, achieving the score in 
        variable expected. 
    '''
    text = ('They are very big, although he is the biggest.')
    nrOfConnectives = 1
    nrOfTokens = 9
    index = nrOfConnectives/nrOfTokens
    expected = round(max(-3.5 + 300*index - 1666.667*index**2, 0), 2)
    score = getConnectiveScore(text)
    assert score == expected

def test_con_one_sentence_multiple_connectives():
    '''
        Test if a single sentence with multiple connective returns
        the correct score. There are three connectives and sixteen
        words within the sentence, achieving the score in 
        variable expected. 
    '''
    text = ('Despite the fact that they are very big, unfortunantely he is the biggest all in all.')
    nrOfConnectives = 3
    nrOfTokens = 16
    index = nrOfConnectives/nrOfTokens
    expected = round(max(-3.5 + 300*index - 1666.667*index**2, 0), 2)
    score = getConnectiveScore(text)
    assert score == expected

def test_con_more_sentences_single_connective():
    '''
        Test if two sentences with a single connective in total returns
        the correct score. There is one connective and nine
        words within the sentences, achieving the score in 
        variable expected. 
    '''
    text = ('They are very big. Although he is the biggest.')
    nrOfConnectives = 1
    nrOfTokens = 9
    index = nrOfConnectives/nrOfTokens
    expected = round(max(-3.5 + 300*index - 1666.667*index**2, 0), 2)
    score = getConnectiveScore(text)
    assert score == expected

def test_con_more_sentences_multiple_connectives():
    '''
        Test if a single sentence with multiple connective returns
        the correct score. There are three connectives and sixteen
        words within the sentences, achieving the score in 
        variable expected. 
    '''
    text = ('Despite the fact that they are very big. Unfortunantely he is the biggest all in all.')
    nrOfConnectives = 3
    nrOfTokens = 16
    index = nrOfConnectives/nrOfTokens
    expected = round(max(-3.5 + 300*index - 1666.667*index**2, 0), 2)
    score = getConnectiveScore(text)
    assert score == expected




'''
    The following tests concern the function generateExplanation.
    This function combines the functions getTTRScore and getConnectiveScore
    such that a final score can be achieved. Next to that, 
    it gives explanations for the scores. 
'''

# Test generateExplanation
# concluding score with explanation


