from getTTRScore import getTTRScore
from string import ascii_lowercase


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
        Test if a sentence with only similar elements has minimum score, so 0.
    '''
    text = ('Big bigger biggest.')
    score = getTTRScore(text)
    assert score == (0, ['big'])

def test_ttr_text_with_min_score():
    '''
        Test if a text with only similar elements has minimum score, so 0.
    '''
    text = ('Big bigger biggest. Bigger. Biggest. Big bigger. Bigger biggest big!')
    score = getTTRScore(text)
    assert score == (0, ['big'])

def test_ttr_sentence_with_max_score():
    '''
        Test if a sentence with only unique elements has maximum score, so 10.
    '''
    text = ('He is a very unique animal.')
    score = getTTRScore(text)
    assert score == (10.0, ['he', 'be', 'a'])

def test_ttr_text_with_max_score():
    '''
        Test if a text with only unique elements has maximum score, so 10.
    '''
    text = ('He is a very unique animal. That shows amazing results. No wonder they exist in here.')
    score = getTTRScore(text)
    assert score == (10.0, ['he', 'be', 'a'])

def test_ttr_single_sentence():
    '''
        Test if a simple text of one sentence returns the correct score.
        The sentence contains "big" and "bigger", and "are" and "is".
        Hence, the score should be (10-4)/10*10=6
    '''
    text = ('They are very big and that person is also bigger.')
    score = getTTRScore(text)
    assert score == (6.0, ['be', 'big', 'they'])

def test_ttr_three_sentences():
    '''
        Test if a simple text of three sentences returns the correct score.
        The sentences contain "big", "bigger" and "biggest", and "are", "is" and "is".
        Hence, the score should be (12-6)/12*10=6
    '''
    text = ('They are very big. That person is bigger. He is the biggest.')
    score = getTTRScore(text)
    assert score == (6.0, ['be', 'big', 'they'])

def test_ttr_windowsize_min_score(): 
    '''
        Test if a text with a windowsize bigger than 50 still gets the 
        minimum score despite the text after the 50 similar words containing
        different words. 
    '''
    text = 'big'*51 + 'hello this is a different text'
    score = getTTRScore(text)
    assert score == (0.0, ['big'])

def test_ttr_windowsize_max_score(): 
    '''
        Test if a text with a windowsize bigger than 50 still gets the 
        maximum score despite the text after the 50 different words containing
        similar words. 
    '''
    text = ''
    for first_letter in ascii_lowercase:
        for second_letter in ascii_lowercase:
            text += first_letter + second_letter + " "
    text += 'big'*10
    score = getTTRScore(text)
    assert score == (10.0, ['aa', 'ab', 'ac'])

