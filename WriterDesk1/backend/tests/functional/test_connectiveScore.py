from getConnectiveScore import getConnectiveScore
from string import ascii_lowercase

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

def test_con_one_sentences_no_connectives():
    '''
        Test if one sentence with no connectives return
        the correct score. 
    '''
    text = ('They are very big.')
    nrOfConnectives = 0
    nrOfTokens = 4
    index = nrOfConnectives/nrOfTokens
    expected = round(max(-3.5 + 300*index - 1666.667*index**2, 0), 2)
    score = getConnectiveScore(text)
    assert score == (expected, index)

def test_con_three_sentences_no_connective():
    '''
        Test if a simple text of three sentences returns the correct score.
        The sentences do not contain any connectives, so it should return 0.
    '''
    text = ('They are very big. That person is bigger. He is the biggest.')
    score = getConnectiveScore(text)
    assert score == (0,0)

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
    assert score == (expected, index)

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
    assert score == (expected, index)

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
    assert score == (expected, index)

def test_con_more_sentences_multiple_connectives():
    '''
        Test if multiple sentencse with multiple connectives return
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
    assert score == (expected, index)

def test_con_one_sentences_all_connectives():
    '''
        Test if one sentence with only connectives return
        the correct score. 
    '''
    text = 'Although, although although.'
    nrOfConnectives = 3
    nrOfTokens = 3
    index = nrOfConnectives/nrOfTokens
    expected = round(max(-3.5 + 300*index - 1666.667*index**2, 0), 2)
    score = getConnectiveScore(text)
    assert score == (expected, index)

def test_con_more_sentences_all_connectives():
    '''
        Test if multiple sentences with only connectives return
        the correct score. 
    '''
    text = 'Although, although although.'*4
    nrOfConnectives = 12
    nrOfTokens = 12
    index = nrOfConnectives/nrOfTokens
    expected = round(max(-3.5 + 300*index - 1666.667*index**2, 0), 2)
    score = getConnectiveScore(text)
    assert score == (expected, index)

def test_con_windowsize_max_score(): 
    '''
        Test if a text with a windowsize bigger than 50 still gets the 
        maximum score despite the text after the 50 words containing
        no connectives.
    '''
    text = 'Although'*51 + 'They are very big.'
    nrOfConnectives = 50
    nrOfTokens = 50
    index = nrOfConnectives/nrOfTokens
    expected = round(max(-3.5 + 300*index - 1666.667*index**2, 0), 2)
    score = getConnectiveScore(text)
    assert score == (expected, index)

def test_con_windowsize_min_score(): 
    '''
        Test if a text with a windowsize bigger than 50 still gets the 
        minimum score despite the text after the 50 words containing
        connectives
    '''
    text = ('They are very big.')*15 + 'although although although'
    nrOfConnectives = 0
    nrOfTokens = 50
    index = nrOfConnectives/nrOfTokens
    expected = round(max(-3.5 + 300*index - 1666.667*index**2, 0), 2)
    score = getConnectiveScore(text)
    assert score == (expected, index)
