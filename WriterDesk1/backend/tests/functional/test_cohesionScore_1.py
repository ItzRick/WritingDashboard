from app.feedback.generateFeedback.CohesionFeedback import CohesionFeedback
from string import ascii_lowercase

'''
    The following tests concern the function generateExplanation.
    This function combines the functions getTTRScore and getConnectiveScore
    such that a final score can be achieved. Next to that, 
    it gives explanations for the scores (feedback). 
    This explanation is based on what the other two functions return.
'''

def testGenerateFeedbackZeroWords(testClient, downloadNltk):
    '''
        Test if a text with zero words returns None.
        Arguments: 
            testClient: The test client we test this for.
            downloadNltk: Function needed to download nltk corpora used in this
                    method.
        Attributes: 
            score: The score given for the cohesion score.
    '''
    del testClient, downloadNltk
    feedbackObject = CohesionFeedback('', '', 1, 1, '')
    score = feedbackObject.genFeedback()
    assert score == None

def testOneWordTextFirst(testClient, downloadNltk):
    '''
        Test if a text consisting of only one word which is not a connective
        returns the correct feedback and score.
        The TTR score of this is 10.0 and the connective score is 0.0, thus
        this results in a score of 5.0.
        The expected feedback is that of the highest score of TTR and 
        the lowest score of connectives. 
        Arguments: 
            testClient: The test client we test this for.   
            downloadNltk: Function needed to download nltk corpora used in this
                    method.         
        Attributes: 
            text: Input text for the test.            
            score: The scores given for the cohesion score.
            expected_feedback: The expected feedback string.
    '''
    del testClient, downloadNltk
    text = "Hello"
    feedbackObject = CohesionFeedback(text, '', 1, 1, '')
    score = feedbackObject.genFeedback()
    expectedFeedback = feedbackObject.feedback
    expected_feedback = ("Your score for cohesion is 5.0.\nThe amount of "
        "variation of words you use is good. You have more than 90 percent "
        "variation in your text.\nYou don't have enough connectives in your "
        "text. You have a percentage of 0 in your text, ideally this would be "
        "9 percent.\nConnectives are words or phrases that link other "
        "linguistic units.")
    assert score == (5.0, [[-1, -1, -1, -1, 1, expected_feedback, '', []]])
    assert expectedFeedback == expected_feedback

def testOneWordTextSecond(testClient, downloadNltk):
    '''
        Test if a text consisting of only one word which is a connective
        returns the correct feedback and score.
        The TTR score of this is 10.0 and the connective score is 0.0, thus
        this results in a score of 5.0.
        The expected feedback is that of the highest score of TTR and 
        the lowest score of connectives. 
        Arguments: 
            testClient: The test client we test this for.   
            downloadNltk: Function needed to download nltk corpora used in this
                    method.         
        Attributes: 
            text: Input text for the test.            
            score: The scores given for the cohesion score.
            expected_feedback: The expected feedback string.
    '''
    del testClient, downloadNltk
    text = "But"
    feedbackObject = CohesionFeedback(text, '', 1, 1, '')
    score = feedbackObject.genFeedback()
    expectedFeedback = feedbackObject.feedback
    expected_feedback = ("Your score for cohesion is 5.0.\nThe amount of "
        "variation of words you use is good. You have more than 90 percent "
        "variation in your text.\nYou have too many connectives in your text. "
        "You have a percentage of 100 in your text, ideally this would be 9 "
        "percent.\nConnectives are words or phrases that link other linguistic"
        " units.")
    assert score == (5.0, [[-1, -1, -1, -1, 1, expected_feedback, '', []]])
    assert expectedFeedback == expected_feedback

def testTTRHighest(testClient, downloadNltk):
    '''
        Test if a text with a TTR score bigger or equal to 9 returns the
        correct feedback and score.
        This specific text has a TTR score of 9.98 and a connective score of
        0, thus resulting in a score of 4.99.
        Hence, the feedback on TTR score should be that of >= 9.
        Arguments: 
            testClient: The test client we test this for.   
            downloadNltk: Function needed to download nltk corpora used in this
                    method.         
        Attributes: 
            text: Input text for the test.            
            score: The scores given for the cohesion score.
            expected_feedback: The expected feedback string.
    '''
    del testClient, downloadNltk
    text = ""
    for first_letter in ascii_lowercase:
        for second_letter in ascii_lowercase:
            text += first_letter + second_letter + " "
    text += "big "*10
    feedbackObject = CohesionFeedback(text, '', 1, 1, '')
    score = feedbackObject.genFeedback()
    expectedFeedback = feedbackObject.feedback
    expected_feedback = ("The amount of variation of words you use is good. "
        "You have more than 90 percent variation in your text.")
    assert score[0] == 4.99
    assert expectedFeedback.splitlines()[1] == expected_feedback

def testTTRSecondHighest(testClient, downloadNltk):
    '''
        Test if a text with a TTR score bigger or equal to 7 and lower than 9
        returns the correct feedback and score. 
        This specific text has a TTR score of 8.0 and a connective score of
        0, thus resulting in a score of 4.0.
        The most used words should be "be", "big" and "they".
        Hence, the feedback on TTR score should be that of >= 7.
        Arguments: 
            testClient: The test client we test this for.   
            downloadNltk: Function needed to download nltk corpora used in this
                    method.         
        Attributes: 
            text: Input text for the test.            
            score: The scores given for the cohesion score.
            expected_feedback: The expected feedback string.
    '''
    del testClient, downloadNltk
    text = "They are very big and that person is also bigger."
    feedbackObject = CohesionFeedback(text, '', 1, 1, '')
    score = feedbackObject.genFeedback()
    expectedFeedback = feedbackObject.feedback
    expected_feedback = ("You used enough variation of words. You have in "
        "between 70 and 90 percent variation in your text. These are your most"
        " used words: \"be\", \"big\" and \"they\".")
    assert score[0] == 4.0
    assert expectedFeedback.splitlines()[1] == expected_feedback

def testTTRSecondLowest(testClient, downloadNltk):
    '''
        Test if a text with a TTR score bigger or equal to 5 and lower than 7
        returns the correct feedback and score.
        This specific text has a TTR score of 6.67 and a connective score of
        0, thus resulting in a score of 3.33.
        The most used words should be "be", "big" and "they".
        Hence, the feedback on TTR score should be that of >= 5.
        Arguments: 
            testClient: The test client we test this for.   
            downloadNltk: Function needed to download nltk corpora used in this
                    method.         
        Attributes: 
            text: Input text for the test.            
            score: The scores given for the cohesion score.
            expected_feedback: The expected feedback string.
    '''
    del testClient, downloadNltk
    text = "They are very big. That person is bigger. He is the biggest."
    feedbackObject = CohesionFeedback(text, '', 1, 1, '')
    score = feedbackObject.genFeedback()
    expectedFeedback = feedbackObject.feedback
    expected_feedback = ("You barely have enough variation of words. You have "
        "in between 50 and 70 percent variation in your text. These are your "
        "most used words: \"be\", \"big\" and \"they\".")
    assert score[0] == 3.33
    assert expectedFeedback.splitlines()[1] == expected_feedback

def testTTRLowest(testClient, downloadNltk):
    '''
        Test if a text with a TTR score lower than 5 returns the correct 
        feedback and score.
        This specific text has a TTR score of 0.72 and a connective score of
        0, thus resulting in a score of 0.36.
        The most used words should be "big", "hello" and "this".
        Hence, the feedback on TTR score should be that of < 5.
        Arguments: 
            testClient: The test client we test this for.   
            downloadNltk: Function needed to download nltk corpora used in this
                    method.         
        Attributes: 
            text: Input text for the test.            
            score: The scores given for the cohesion score.
            expected_feedback: The expected feedback string.
    '''
    del testClient, downloadNltk
    text = "big "*51 + "hello this is a different text"
    feedbackObject = CohesionFeedback(text, '', 1, 1, '')
    score = feedbackObject.genFeedback()
    expectedFeedback = feedbackObject.feedback
    expected_feedback = ("You did not use enough variation in terms of "
            "words. You have less than 50 percent variation in your text. "
            "These are your most used words: \"big\", \"hello\" and \"this\".")
    assert score[0] == 0.36
    assert expectedFeedback.splitlines()[1] == expected_feedback


def testConnectivesHighest(testClient, downloadNltk):
    '''
        Test if a text with a connectives score bigger or equal to 9 returns
        the correct feedback and score.
        This specific text has a connective score of 9.26 and a TTR score of
        7.78, thus resulting in a score of 8.52.
        The index score is 0.11.
        Hence, the feedback on connective score should be that of >= 9.
        Arguments: 
            testClient: The test client we test this for.   
            downloadNltk: Function needed to download nltk corpora used in this
                    method.         
        Attributes: 
            text: Input text for the test.            
            score: The scores given for the cohesion score.
            expected_feedback: The expected feedback string.
    '''
    del testClient, downloadNltk
    text = "They are very big, although he is the biggest."
    feedbackObject = CohesionFeedback(text, '', 1, 1, '')
    score = feedbackObject.genFeedback()
    expectedFeedback = feedbackObject.feedback
    expected_feedback = ("The amount of connectives you used is good. You have"
        " a percentage of 11 in your text, ideally this would be 9 percent.")
    assert score[0] == 8.52
    assert expectedFeedback.splitlines()[2] == expected_feedback


def testConnectivesSecondHighestFewConnectives(testClient, downloadNltk):
    '''
        Test if a text with a connectives score bigger or equal to 7 and lower
        than 9 and an index score lower than 0.09 returns the correct feedback
        and score.
        This specific text has an index score of 0.058..., a connective score
        of 8.38 and a TTR score of 1.18, thus resulting in a score of 4.78. 
        Hence, the feedback on connective score should be that of >= 7 and 
        index score < 0.09.
        Arguments: 
            testClient: The test client we test this for.   
            downloadNltk: Function needed to download nltk corpora used in this
                    method.         
        Attributes: 
            text: Input text for the test.            
            score: The scores given for the cohesion score.
            expected_feedback: The expected feedback string.
    '''
    del testClient, downloadNltk
    text = "However" + 16*" hey"
    feedbackObject = CohesionFeedback(text, '', 1, 1, '')
    score = feedbackObject.genFeedback()
    expectedFeedback = feedbackObject.feedback
    expected_feedback = ("You could use more connectives in your text. "
        "You have a percentage of 6 in your text, ideally this would be 9 "
        "percent.")
    assert score[0] == 4.78
    assert expectedFeedback.splitlines()[2] == expected_feedback

def testConnectivesSecondHighestManyConnectives(testClient, downloadNltk):
    '''
        Test if a text with a connectives score bigger or equal to 7 and lower
        than 9 and an index score higher than 0.09 returns the correct feedback
        and score.
        This specific text has an index score of 0.125, a connective score of
        7.96 and a TTR score of 7.5, thus resulting in a score of 7.73. 
        Hence, the feedback on connective score should be that of >= 7 and
        index score > 0.09.
        Arguments: 
            testClient: The test client we test this for.   
            downloadNltk: Function needed to download nltk corpora used in this
                    method.         
        Attributes: 
            text: Input text for the test.            
            score: The scores given for the cohesion score.
            expected_feedback: The expected feedback string.
    '''
    del testClient, downloadNltk
    text = ("Despite the fact that they are very big, unfortunantely he is the"
        " biggest all in all.")
    feedbackObject = CohesionFeedback(text, '', 1, 1, '')
    score = feedbackObject.genFeedback()
    expectedFeedback = feedbackObject.feedback
    expected_feedback = ("You could use less connectives in your text. You "
        "have a percentage of 12 in your text, ideally this would be 9 "
        "percent.")
    assert score[0] == 7.73
    assert expectedFeedback.splitlines()[2] == expected_feedback

def testConnectivesSecondLowestFewConnectives(testClient, downloadNltk):
    '''
        Test if a text with a connectives score bigger or equal to 5 and lower
        than 7 and an index score lower than 0.09 returns the correct feedback
        and score.
        This specific text has an index score of 0.038..., a connective score
        of 5.57 and a TTR score of 0.77, thus resulting in a score of 3.17. 
        Hence, the feedback on connective score should be that of >= 5 and
        index score < 0.09.
        Arguments: 
            testClient: The test client we test this for.   
            downloadNltk: Function needed to download nltk corpora used in this
                    method.         
        Attributes: 
            text: Input text for the test.            
            score: The scores given for the cohesion score.
            expected_feedback: The expected feedback string.
    '''
    del testClient, downloadNltk
    text = "However" + 25*" hey"
    feedbackObject = CohesionFeedback(text, '', 1, 1, '')
    score = feedbackObject.genFeedback()
    expectedFeedback = feedbackObject.feedback
    expected_feedback = ("You should use more connectives in your text. You "
        "have a percentage of 4 in your text, ideally this would be 9 "
        "percent.")
    assert score[0] == 3.17
    assert expectedFeedback.splitlines()[2] == expected_feedback

def testConnectivesSecondLowestManyConnectives(testClient, downloadNltk):
    '''
        Test if a text with a connectives score bigger or equal to 5 and lower
        than 7 and an index score higher than 0.09 returns the correct feedback
        and score.
        This specific text has an index score of 0.142..., a connective score
        of 5.34 and a TTR score of 2.86, thus resulting in a score of 4.1.
        Hence, the feedback on connective score should be that of >= 5 and
        index score > 0.09.
        Arguments: 
            testClient: The test client we test this for.   
            downloadNltk: Function needed to download nltk corpora used in this
                    method.         
        Attributes: 
            text: Input text for the test.            
            score: The scores given for the cohesion score.
            expected_feedback: The expected feedback string.
    '''
    del testClient, downloadNltk
    text = "However" + 6*" hey"
    feedbackObject = CohesionFeedback(text, '', 1, 1, '')
    score = feedbackObject.genFeedback()
    expectedFeedback = feedbackObject.feedback
    expected_feedback = ("You should use less connectives in your text. You "
        "have a percentage of 14 in your text, ideally this would be 9 "
        "percent.")
    assert score[0] == 4.1
    assert expectedFeedback.splitlines()[2] == expected_feedback

def testConnectivesLowestFewConnectives(testClient, downloadNltk):
    '''
        Test if a text with a connectives score lower than 5 and an index score
        lower than 0.09 returns the correct feedback and score.
        This specific text has an index score of 0, a connective score of
        0.0 and a TTR score of 10.0, thus resulting in a score of 5.0. 
        Hence, the feedback on connective score should be that of < 5 and
        index score < 0.09.
        Arguments: 
            testClient: The test client we test this for.   
            downloadNltk: Function needed to download nltk corpora used in this
                    method.         
        Attributes: 
            text: Input text for the test.            
            score: The scores given for the cohesion score.
            expected_feedback: The expected feedback string.    
    '''
    del testClient, downloadNltk
    text = "They are very big."
    feedbackObject = CohesionFeedback(text, '', 1, 1, '')
    score = feedbackObject.genFeedback()
    expectedFeedback = feedbackObject.feedback
    expected_feedback = ("You don't have enough connectives in your text. You "
        "have a percentage of 0 in your text, ideally this would be 9 "
        "percent.")
    assert score[0] == 5.0
    assert expectedFeedback.splitlines()[2] == expected_feedback

