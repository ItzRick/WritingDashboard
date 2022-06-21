from app.getConnectiveScore import getConnectiveScore

'''
    The following tests concern the function getConnectiveScore. 
    Within this function, the number of connectives are looked into.
    The number of connectives used in a text are divided by the 
    total number of tokens (words) in a text. This number is then
    inserted into a 2nd order polynomial to achieve a score. 
'''

def testConZeroWords(testClient):
    '''
        Test if a text with zero words returns None.
        Arguments: 
            testClient: The test client we test this for.            
        Attributes:             
            score: The scores given for the connective and index score.
    '''
    del testClient
    score = getConnectiveScore("")
    assert score == None

def testConOneSentencesNoConnectives(testClient):
    '''
        Test if one sentence with no connectives returns
        the correct score and the correct index score. 
        The sentence does not contain any connective, so it should return 0.
        We then insert this index score into the 2nd order polynomial to get
        the expected score.
        Arguments: 
            testClient: The test client we test this for.            
        Attributes: 
            text: Input text for the test.
            index: Expected index score.
            expected: Expected connective score.
            score: The scores given for the connective and index score.
    '''
    del testClient
    text = "They are very big."    
    index = 0/4
    expected = round(max(-3.5 + 300*index - 1666.667*index**2, 0), 2)
    score = getConnectiveScore(text)
    assert score == (expected, index)

def testConThreeSentencesNoConnective(testClient):
    '''
        Test if a simple text of three sentences returns the correct score and
        the correct index score.
        The sentences do not contain any connectives, so the index score should
        be 0.
        We then insert this index score into the 2nd order polynomial to get
        the expected score.
        Arguments: 
            testClient: The test client we test this for.            
        Attributes: 
            text: Input text for the test.
            index: Expected index score.
            expected: Expected connective score.
            score: The scores given for the connective and index score.
    '''
    del testClient
    text = "They are very big. That person is bigger. He is the biggest."
    index = 0
    expected = round(max(-3.5 + 300*index - 1666.667*index**2, 0), 2)
    score = getConnectiveScore(text)
    assert score == (expected,index)

def testConOneSentenceSingleConnective(testClient):
    '''
        Test if a single sentence with a single connective returns the correct 
        score and the correct index score. 
        There is one connective and nine words within the sentence, thus the
        index score should be 1/9.
        We then insert this index score into the 2nd order polynomial to get
        the expected score.
        Arguments: 
            testClient: The test client we test this for.            
        Attributes: 
            text: Input text for the test.
            index: Expected index score.
            expected: Expected connective score.
            score: The scores given for the connective and index score.
    '''
    del testClient
    text = "They are very big, although he is the biggest."
    index = 1/9
    expected = round(max(-3.5 + 300*index - 1666.667*index**2, 0), 2)
    score = getConnectiveScore(text)
    assert score == (expected, index)

def testConOneSentenceMultipleConnectives(testClient):
    '''
        Test if a single sentence with multiple connective returns
        the correct score and the correct index score.
        There are two connectives and sixteen words within the sentence, thus
        the index score should be 2/16.
        We then insert this index score into the 2nd order polynomial to get
        the expected score.
        Arguments: 
            testClient: The test client we test this for.            
        Attributes: 
            text: Input text for the test.
            index: Expected index score.
            expected: Expected connective score.
            score: The scores given for the connective and index score.
    '''
    del testClient
    text = ("Despite the fact that they are very big, unfortunantely he is the"
        " biggest all in all.")    
    index = 2/16
    expected = round(max(-3.5 + 300*index - 1666.667*index**2, 0), 2)
    score = getConnectiveScore(text)
    assert score == (expected, index)

def testConMoreSentencesSingleConnective(testClient):
    '''
        Test if two sentences with a single connective in total returns
        the correct score and the correct index score.
        There is one connective and nine words within the sentences, 
        thus the index score should be 1/9.
        We then insert this index score into the 2nd order polynomial to get
        the expected score.
        Arguments: 
            testClient: The test client we test this for.            
        Attributes: 
            text: Input text for the test.
            index: Expected index score.
            expected: Expected connective score.
            score: The scores given for the connective and index score.
    '''
    del testClient
    text = "They are very big. Although he is the biggest."
    index = 1/9
    expected = round(max(-3.5 + 300*index - 1666.667*index**2, 0), 2)
    score = getConnectiveScore(text)
    assert score == (expected, index)

def testConMoreSentencesMultipleConnectives(testClient):
    '''
        Test if multiple sentences with multiple connectives return
        the correct score and the correct index score. 
        There are two connectives and sixteen words within the sentences, 
        thus the index score should be 2/16.
        We then insert this index score into the 2nd order polynomial to get
        the expected score.
        Arguments: 
            testClient: The test client we test this for.            
        Attributes: 
            text: Input text for the test.
            index: Expected index score.
            expected: Expected connective score.
            score: The scores given for the connective and index score.
    '''
    del testClient
    text = ("Despite the fact that they are very big. Unfortunantely he is the"
        " biggest all in all.")
    index = 2/16
    expected = round(max(-3.5 + 300*index - 1666.667*index**2, 0), 2)
    score = getConnectiveScore(text)
    assert score == (expected, index)

def testConOneSentencesAllConnectives(testClient):
    '''
        Test if one sentence with only connectives returns
        the correct score and the correct index score.
        The index score should then be 1.
        We then insert this index score into the 2nd order polynomial to get
        the expected score. 
        Arguments: 
            testClient: The test client we test this for.            
        Attributes: 
            text: Input text for the test.
            index: Expected index score.
            expected: Expected connective score.
            score: The scores given for the connective and index score.
    '''
    del testClient
    text = "Although, although although."
    index = 3/3
    expected = round(max(-3.5 + 300*index - 1666.667*index**2, 0), 2)
    score = getConnectiveScore(text)
    assert score == (expected, index)

def testConMoreSentencesAllConnectives(testClient):
    '''
        Test if multiple sentences with only connectives return
        the correct score and the correct index score.
        The index score should then be 1.
        We then insert this index score into the 2nd order polynomial to get
        the expected score. 
        Arguments: 
            testClient: The test client we test this for.            
        Attributes: 
            text: Input text for the test.
            index: Expected index score.
            expected: Expected connective score.
            score: The scores given for the connective and index score.
    '''
    del testClient
    text = "Although, although although. "*4
    index = 12/12
    expected = round(max(-3.5 + 300*index - 1666.667*index**2, 0), 2)
    score = getConnectiveScore(text)
    assert score == (expected, index)

def testBigTextMinScore(testClient): 
    '''
        Test if a text with a big size gets the correct score despite the text
        only containing connectives first and then a few non-connectives
        at the end.
        There are 50 connectives and 54 words within the text, 
        thus the index score should be 50/54.
        We then insert this index score into the 2nd order polynomial to get
        the expected score.
        Arguments: 
            testClient: The test client we test this for.            
        Attributes: 
            text: Input text for the test.
            index: Expected index score.
            expected: Expected connective score.
            score: The scores given for the connective and index score.
    '''
    del testClient
    text = "Although "*50 + "They are very big."
    index = 50/54
    expected = round(max(-3.5 + 300*index - 1666.667*index**2, 0), 2)
    score = getConnectiveScore(text)
    assert score == (expected, index)

def test_con_windowsize_min_score(testClient): 
    '''
        Test if a text with a big size gets the correct score despite the text
        only containing non-connectives first and then a few connectives 
        at the end.
        There are 3 connectives and 63 words within the text, 
        thus the index score should be 3/63.
        We then insert this index score into the 2nd order polynomial to get
        the expected score.
        Arguments: 
            testClient: The test client we test this for.            
        Attributes: 
            text: Input text for the test.
            index: Expected index score.
            expected: Expected connective score.
            score: The scores given for the connective and index score.
    '''
    del testClient
    text = "They are very big. "*15 + "although although although"
    index = 3/63
    expected = round(max(-3.5 + 300*index - 1666.667*index**2, 0), 2)
    score = getConnectiveScore(text)
    assert score == (expected, index)
