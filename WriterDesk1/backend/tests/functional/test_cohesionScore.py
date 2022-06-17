from app.cohesionCheck import generateExplanation
from string import ascii_lowercase

'''
    The following tests concern the function generateExplanation.
    This function combines the functions getTTRScore and getConnectiveScore
    such that a final score can be achieved. Next to that, 
    it gives explanations for the scores (feedback). 
    This explanation is based on what the other two functions return.
'''

def testGenerateFeedbackZeroWords(testClient):
    '''
        Test if a text with zero words returns None.
    '''
    del testClient
    score = generateExplanation('')
    assert score == None

def testOneWordText(testClient):
    '''
        Test if a text consisting of only one word which is not a connective
        returns the correct feedback and score.
        The TTR score of this is 10.0 and the connective score is 0.0, thus
        this results in a score of 5.0.
        The expected feedback is that of the highest score of TTR and 
        the lowest score of connectives. 
    '''
    del testClient
    text = "Hello"
    score = generateExplanation(text)
    expected_feedback = ("Your score for cohesion is 5.0.\nThe amount of "
        "variation of words you use is very good.\nYou don't have enough "
        "connectives in your text.\nConnectives are words or phrases that link"
        " other linguistic units.")
    assert score == (5.0, expected_feedback)


def testOneWordText(testClient):
    '''
        Test if a text consisting of only one word which is a connective
        returns the correct feedback and score.
        The TTR score of this is 10.0 and the connective score is 0.0, thus
        this results in a score of 5.0.
        The expected feedback is that of the highest score of TTR and 
        the lowest score of connectives. 
    '''
    del testClient
    text = "But"
    score = generateExplanation(text)
    expected_feedback = ("Your score for cohesion is 5.0.\nThe amount of "
        "variation of words you use is very good.\nYou have too many "
        "connectives in your text.\nConnectives are words or phrases that "
        "link other linguistic units.")
    assert score == (5.0, expected_feedback)

def testTTRHighest(testClient):
    '''
        Test if a text with a TTR score bigger or equal to 9 returns the
        correct feedback and score.
        This specific text has a TTR score of 9.98 and a connective score of
        0, thus resulting in a score of 4.99.
        Hence, the feedback on TTR score should be: "The amount of variation of
        words you use is very good."
    '''
    del testClient
    text = ''
    for first_letter in ascii_lowercase:
        for second_letter in ascii_lowercase:
            text += first_letter + second_letter + " "
    text += 'big '*10
    score = generateExplanation(text)
    expected_feedback = ('The amount of variation of words you use is very '
        'good.')
    assert score[0] == 4.99
    assert score[1].splitlines()[1] == expected_feedback

def testTTRSecondHighest(testClient):
    '''
        Test if a text with a TTR score bigger or equal to 7 and lower than 9
        returns the correct feedback and score. 
        This specific text has a TTR score of 8.0 and a connective score of
        0, thus resulting in a score of 4.0.
        The most used words should be "be", "big" and "they".
        Hence, the feedback on TTR score should be: "You used enough variation
        of words, however you could improve this some more. These are your most
        used words: "be", "big" and "they"."
    '''
    del testClient
    text = ('They are very big and that person is also bigger.')
    score = generateExplanation(text)
    expected_feedback = ("You used enough variation of words, however you "
        "could improve this some more. These are your most used words: "
        "\"be\", \"big\" and \"they\".")
    assert score[0] == 4.0
    assert score[1].splitlines()[1] == expected_feedback

def testTTRSecondLowest(testClient):
    '''
        Test if a text with a TTR score bigger or equal to 5 and lower than 7
        returns the correct feedback and score.
        This specific text has a TTR score of 6.67 and a connective score of
        0, thus resulting in a score of 3.33.
        The most used words should be "be", "big" and "they".
        Hence, the feedback on TTR score should be: "You barely have enough
        variation of words, you should improve on this. These are your most
        used words: "be", "big" and "they"."
    '''
    del testClient
    text = ('They are very big. That person is bigger. He is the biggest.')
    score = generateExplanation(text)
    expected_feedback = ("You barely have enough variation of words, you "
        "should improve on this. These are your most used words: "
        "\"be\", \"big\" and \"they\".")
    assert score[0] == 3.33
    assert score[1].splitlines()[1] == expected_feedback

def testTTRLowest(testClient):
    '''
        Test if a text with a TTR score lower than 5 returns the correct 
        feedback and score.
        This specific text has a TTR score of 0.72 and a connective score of
        0, thus resulting in a score of 0.36.
        The most used words should be "big", "hello" and "this".
        Hence, the feedback on TTR score should be: "You did not use enough
        variation in terms of words, you are using the same words too much.
        These are your most used words: "big", "hello" and "this"."
    '''
    del testClient
    text = 'big '*51 + 'hello this is a different text'
    score = generateExplanation(text)
    expected_feedback = ("You did not use enough variation in terms of words, "
        "you are using the same words too much. These are your most used"
        " words: \"big\", \"hello\" and \"this\".")
    assert score[0] == 0.36
    assert score[1].splitlines()[1] == expected_feedback


def testConnectivesHighest(testClient):
    '''
        Test if a text with a connectives score bigger or equal to 9 returns
        the correct feedback and score.
        This specific text has a connective score of 9.26 and a TTR score of
        7.78, thus resulting in a score of 8.52.
        Hence, the feedback on connective score should be: "The amount of
        connectives you used is very good."

    '''
    del testClient
    text = ('They are very big, although he is the biggest.')
    score = generateExplanation(text)
    expected_feedback = "The amount of connectives you used is very good."
    assert score[0] == 8.52
    assert score[1].splitlines()[2] == expected_feedback


def testConnectivesSecondHighestFewConnectives(testClient):
    '''
        Test if a text with a connectives score bigger or equal to 7 and lower
        than 9 and an index score lower than 0.09 returns the correct feedback
        and score.
        This specific text has an index score of 0.058..., a connective score
        of 8.38 and a TTR score of 1.18, thus resulting in a score of 4.78. 
        Hence, the feedback on connective score should be: "You could use some
        more connectives in your text."
    '''
    del testClient
    text = 'However' + 16*' hey'
    score = generateExplanation(text)
    expected_feedback = "You could use some more connectives in your text."
    assert score[0] == 4.78
    assert score[1].splitlines()[2] == expected_feedback

def testConnectivesSecondHighestManyConnectives(testClient):
    '''
        Test if a text with a connectives score bigger or equal to 7 and lower
        than 9 and an index score higher than 0.09 returns the correct feedback
        and score.
        This specific text has an index score of 0.125, a connective score of
        7.96 and a TTR score of 7.5, thus resulting in a score of 7.73. 
        Hence, the feedback on connective score should be: "You could use a bit
        less connectives in your text."
    '''
    del testClient
    text = ('Despite the fact that they are very big, unfortunantely he is the'
        ' biggest all in all.')
    score = generateExplanation(text)
    expected_feedback = "You could use a bit less connectives in your text."
    assert score[0] == 7.73
    assert score[1].splitlines()[2] == expected_feedback

def testConnectivesSecondLowestFewConnectives(testClient):
    '''
        Test if a text with a connectives score bigger or equal to 5 and lower
        than 7 and an index score lower than 0.09 returns the correct feedback
        and score.
        This specific text has an index score of 0.038..., a connective score
        of 5.57 and a TTR score of 0.77, thus resulting in a score of 3.17. 
        Hence, the feedback on connective score should be: "You should use mor
        connectives in your text."
    '''
    del testClient
    text = 'However' + 25*' hey'
    score = generateExplanation(text)
    expected_feedback = "You should use more connectives in your text."
    assert score[0] == 3.17
    assert score[1].splitlines()[2] == expected_feedback

def testConnectivesSecondLowestManyConnectives(testClient):
    '''
        Test if a text with a connectives score bigger or equal to 5 and lower
        than 7 and an index score higher than 0.09 returns the correct feedback
        and score.
        This specific text has an index score of 0.142..., a connective score
        of 5.34 and a TTR score of 2.86, thus resulting in a score of 4.1.
        Hence, the feedback on connective score should be: "You should use less
        connectives in your text."
    '''
    del testClient
    text = 'However' + 6*' hey'
    score = generateExplanation(text)
    expected_feedback = "You should use less connectives in your text."
    assert score[0] == 4.1
    assert score[1].splitlines()[2] == expected_feedback

def testConnectivesLowestFewConnectives(testClient):
    '''
        Test if a text with a connectives score lower than 5 and an index score
        lower than 0.09 returns the correct feedback and score.
        This specific text has an index score of 0, a connective score of
        0.0 and a TTR score of 10.0, thus resulting in a score of 5.0. 
        Hence, the feedback on connective score should be: "You don't have
        enough connectives in your text."     
    '''
    del testClient
    text = ('They are very big.')
    score = generateExplanation(text)
    expected_feedback = "You don't have enough connectives in your text."
    assert score[0] == 5.0
    assert score[1].splitlines()[2] == expected_feedback

def testConnectivesLowestManyConnectives(testClient):
    '''
        Test if a text with a connectives score lower than 5 and an index score
        higher than 0.09 returns the correct feedback and score.
        This specific text has an index score of 1.0, a connective score of
        0.0 and a TTR score of 3.33, thus resulting in a score of 1.67.
        Hence, the feedback on connective score should be: "You have too many
        connectives in your text."
    '''
    del testClient
    text = 'Although, although although.'
    score = generateExplanation(text)
    expected_feedback = "You have too many connectives in your text."
    assert score[0] == 1.67
    assert score[1].splitlines()[2] == expected_feedback