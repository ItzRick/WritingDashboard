from decimal import ROUND_HALF_UP, Decimal
from app.feedback.generateFeedback.StructureFeedback import StructureFeedback


def test_zero_words(testClient):
    '''
        Test if a text with zero words returns None.
        Attributes:
            output: the returning value from running the function
            feedbackObject: Object of the class that generates the feedback for this language and style category.
        Arguments:
            testClient:  The test client we test this for.
    '''
    del testClient
    feedbackObject = StructureFeedback('', '', 1, 1, '')
    # generate the output on an empty text
    output = feedbackObject.getParagraphScoreAndExplanations('')
    assert output == None


def test_400_words(testClient):
    '''
        Test if a text with 400 words returns 
        (100.0 - 0.4 * max(0.0, 400 - 300)) / 10.0 = 6.0 as score and
        returns a dictionary with the paragraph as key and the string 
        'This paragraph is too long, try to make paragraphs with approximately 200 words.'
        as value.
        Attributes:
            testText: the text the function is run on.
            score: the score given for the structure writing skill.
            explanations: the explanations given for this text for the structure
            writing skill.
            feedbackObject: Object of the class that generates the feedback for this language and style category.
        Arguments:
            testClient:  The test client we test this for.
    '''
    del testClient
    # generate a text with 400 words by multiplying a text with 8 words 50 times
    testText = ('This is a large text with 400 words. ' * 50).strip()
    # retrieve the scores and explanations by running the function on the text
    feedbackObject = StructureFeedback(testText, '', 1, 1, '')
    score = feedbackObject.getParagraphScoreAndExplanations(testText)[0]
    explanations = feedbackObject.getParagraphScoreAndExplanations(testText)[1]
    # check if the output scores and explanations match 
    assert score == Decimal(6.0).quantize(
        Decimal('0.1'), rounding=ROUND_HALF_UP)
    assert list(explanations.keys()) == [testText]
    assert list(explanations.values()) == [
        'This paragraph is too long, try to make paragraphs with approximately 200 words.']

def test_50_words(testClient):
    '''
        Test if a text with 50 words returns 
        (100.0 - 0.6 * max(0.0, 100 - 50)) / 10.0 = 7.0 as score and
        returns a dictionary with the paragraph as key and the string 
        'This paragraph is too short, try to make paragraphs with approximately 200 words.'
        as value.
        Attributes:
            testText: the text the function is run on.
            score: the score given for the structure writing skill.
            explanations: the explanations given for this text for the structure
            writing skill.
            feedbackObject: Object of the class that generates the feedback for this language and style category.
        Arguments:
            testClient:  The test client we test this for.
    '''
    del testClient
    # generate a text with 50 words by multiplying a text with 5 words 10 times
    testText = ('A short 50 word text. ' * 10).strip()
    # retrieve the scores and explanations by running the function on the text
    feedbackObject = StructureFeedback(testText, '', 1, 1, '')
    score = feedbackObject.getParagraphScoreAndExplanations(testText)[0]
    explanations = feedbackObject.getParagraphScoreAndExplanations(testText)[1]
    # check if the output scores and explanations match 
    assert score == Decimal(7.0).quantize(
        Decimal('0.1'), rounding=ROUND_HALF_UP)
    assert list(explanations.keys()) == [testText]
    assert list(explanations.values()) == [
        'This paragraph is too short, try to make paragraphs with approximately 200 words.']

def test_200_words(testClient):
    '''
        Test if a text with 200 words returns 10.0 as score and returns an empty
        dictionary since 200 words in a paragraph is good.
        Attributes:
            testText: the text the function is run on.
            score: the score given for the structure writing skill.
            explanations: the explanations given for this text for the structure
            writing skill.
            feedbackObject: Object of the class that generates the feedback for this language and style category.
        Arguments:
            testClient:  The test client we test this for.
    '''
    del testClient
    # generate a text with 200 words by multiplying a text with 8 words 25 times
    testText = ('This is a good text with 200 words. ' * 25).strip()
    # retrieve the scores and explanations by running the function on the text
    feedbackObject = StructureFeedback(testText, '', 1, 1, '')
    score = feedbackObject.getParagraphScoreAndExplanations(testText)[0]
    explanations = feedbackObject.getParagraphScoreAndExplanations(testText)[1]
    # check if the output scores and explanations match 
    assert score == Decimal(10.0).quantize(
        Decimal('0.1'), rounding=ROUND_HALF_UP)
    assert list(explanations.keys()) == []
    assert list(explanations.values()) == []

def test_2_paragraphs_large_different_lengths(testClient):
    '''
        Test if a text with 2 paragraphs of 350 and 450 words returns 6.0
        (100.0 - 0.4 * max(0.0, 350 - 300)) / 10.0 = 8.0 and 
        (100.0 - 0.4 * max(0.0, 450 - 300)) / 10.0 = 4.0
        So the score should be (8.0 + 4.0) / 2 = 6.0 and it returns a dictionary
        with the paragraphs as keys and the string 
        'This paragraph is too long, try to make paragraphs with approximately 200 words.'
        as values.
        Attributes:
            testText: the text the function is run on.
            score: the score given for the structure writing skill.
            explanations: the explanations given for this text for the structure
            writing skill.
            feedbackObject: Object of the class that generates the feedback for this language and style category.
        Arguments:
            testClient:  The test client we test this for.
    '''
    del testClient
    # generate a text with 350 and 450 words by multiplying a text with 5 words 
    # 70 times and 90 times and then adding them together
    testTextPart1 = ('A big 350 word text. ' * 70).strip()
    testTextPart2 = ('A bigger 450 word text. ' * 90).strip()
    testText = testTextPart1 + '\n' + testTextPart2
    # retrieve the scores and explanations by running the function on the text
    feedbackObject = StructureFeedback(testText, '', 1, 1, '')
    score = feedbackObject.getParagraphScoreAndExplanations(testText)[0]
    explanations = feedbackObject.getParagraphScoreAndExplanations(testText)[1]
    # check if the output scores and explanations match 
    assert score == Decimal(6.0).quantize(
        Decimal('0.1'), rounding=ROUND_HALF_UP)
    assert list(explanations.keys()) == [testTextPart1, testTextPart2]
    assert list(explanations.values()) == [
        'This paragraph is too long, try to make paragraphs with approximately 200 words.',
        'This paragraph is too long, try to make paragraphs with approximately 200 words.']

def test_2_paragraphs_small_different_lengths(testClient):
    '''
        Test if a text with 2 paragraphs of 30 and 70 words returns 7.0
        (100.0 - 0.6 * max(0.0, 100 - 30)) / 10.0 = 5.8 and 
        (100.0 - 0.6 * max(0.0, 100 - 70)) / 10.0 = 8.2
        So the score should be (5.8 + 8.2) / 2 = 7.0 and it returns a
        dictionary with the paragraphs as keys and the string 
        'This paragraph is too short, try to make paragraphs with approximately 200 words.'
        as values.
        Attributes:
            testText: the text the function is run on.
            score: the score given for the structure writing skill.
            explanations: the explanations given for this text for the structure
            writing skill.
            feedbackObject: Object of the class that generates the feedback for this language and style category.
        Arguments:
            testClient:  The test client we test this for.
    '''
    del testClient
    # generate a text with 30 and 70 words by multiplying a text with 6 words 
    # 5 times and a text with 7 words 10 times and then adding them together
    testTextPart1 = ('A very short 30 word text. ' * 5).strip()
    testTextPart2 = ('A small bit longer 70 word text. ' * 10).strip()
    testText = testTextPart1 + '\n' + testTextPart2
    # retrieve the scores and explanations by running the function on the text
    feedbackObject = StructureFeedback(testText, '', 1, 1, '')
    score = feedbackObject.getParagraphScoreAndExplanations(testText)[0]
    explanations = feedbackObject.getParagraphScoreAndExplanations(testText)[1]
    # check if the output scores and explanations match 
    assert score == Decimal(7.0).quantize(
        Decimal('0.1'), rounding=ROUND_HALF_UP)
    assert list(explanations.keys()) == [testTextPart1, testTextPart2]
    assert list(explanations.values()) == [
        'This paragraph is too short, try to make paragraphs with approximately 200 words.',
        'This paragraph is too short, try to make paragraphs with approximately 200 words.']

def test_2_paragraphs_good_different_lengths(testClient):
    '''
        Test if a text with 2 paragraphs of 150 and 250 words returns 10.0
        The score should be (10.0 + 10.0) / 2 = 10.0 and it returns an empty
        dictionary since 150 and 250 words in a paragraph is good.
        Attributes:
            testText: the text the function is run on.
            score: the score given for the structure writing skill.
            explanations: the explanations given for this text for the structure
            writing skill.
            feedbackObject: Object of the class that generates the feedback for this language and style category.
        Arguments:
            testClient:  The test client we test this for.
    '''
    del testClient
    # generate a text with 150 and 250 words by multiplying a text with 5 words 
    # 30 times and 50 times and then adding them together
    testTextPart1 = ('A good 150 word text. ' * 30).strip()
    testTextPart2 = ('Another good 250 word text ' * 50).strip()
    testText = testTextPart1 + '\n' + testTextPart2
    # retrieve the scores and explanations by running the function on the text
    feedbackObject = StructureFeedback(testText, '', 1, 1, '')
    score = feedbackObject.getParagraphScoreAndExplanations(testText)[0]
    explanations = feedbackObject.getParagraphScoreAndExplanations(testText)[1]
    # check if the output scores and explanations match 
    assert score == Decimal(10.0).quantize(
        Decimal('0.1'), rounding=ROUND_HALF_UP)
    assert list(explanations.keys()) == []
    assert list(explanations.values()) == []

def test_4_paragraphs_all_lengths(testClient):
    '''
        Test if a text with 4 paragraphs of 0, 400, 50 and 200 words returns 
        7.7. Note that (100.0 - 0.4 * max(0.0, 400 - 300)) / 10.0 = 6.0 and 
        (100.0 - 0.6 * max(0.0, 100 - 50)) / 10.0 = 7.0
        The score should be (6.0 + 7.0 + 10.0) / 3 = 7.7 and it returns a
        dictionary with the paragraphs of 400 and 50 words as keys and the 
        strings 'This paragraph is too long, try to make paragraphs with approximately 200
        words.' and 'This paragraph is too short, try to make paragraphs with 
        approximately 200 words.' as correspoding values.
        Attributes:
            testText: the text the function is run on.
            score: the score given for the structure writing skill.
            explanations: the explanations given for this text for the structure
            writing skill.
            feedbackObject: Object of the class that generates the feedback for this language and style category.
        Arguments:
            testClient:  The test client we test this for.
    '''
    del testClient
    # generate a text with 0, 400, 50 and 200 words by multiplying a text with 8
    # words 50 times, a text with 5 words 10 times and a text with 9 words 25
    # times and then adding them together
    testTextPart1 = ' '
    testTextPart2 = ('This is a large text with 400 words. ' * 50).strip()
    testTextPart3 = ('A short 50 word text. ' * 10).strip()
    testTextPart4 = ('This is a good text with 200 words. ' * 25).strip()
    testText = (testTextPart1 + '\n' + testTextPart2 + '\n' + testTextPart3 +
     '\n' + testTextPart4)
    # retrieve the scores and explanations by running the function on the text
    feedbackObject = StructureFeedback(testText, '', 1, 1, '')
    score = feedbackObject.getParagraphScoreAndExplanations(testText)[0]
    explanations = feedbackObject.getParagraphScoreAndExplanations(testText)[1]
    # check if the output scores and explanations match 
    assert score == Decimal(7.7).quantize(
        Decimal('0.1'), rounding=ROUND_HALF_UP)
    assert list(explanations.keys()) == [testTextPart2, testTextPart3]
    assert list(explanations.values()) == [
        'This paragraph is too long, try to make paragraphs with approximately 200 words.',
        'This paragraph is too short, try to make paragraphs with approximately 200 words.']

def test_2_paragraphs_large_same_content(testClient):
    '''
        Test if a text with 2 paragraphs of 400 words returns 6.0 because
        (100.0 - 0.4 * max(0.0, 400 - 300)) / 10.0 = 6.0 and 
        (100.0 - 0.4 * max(0.0, 400 - 300)) / 10.0 = 6.0
        So the score should be (6.0 + 6.0) / 2 = 6.0 and it returns a dictionary
        with the content as key and the string 
        'This paragraph is too long, try to make paragraphs with approximately 200 words.'
        as value.
        Attributes:
            testText: the text the function is run on.
            score: the score given for the structure writing skill.
            explanations: the explanations given for this text for the structure
            writing skill.
            feedbackObject: Object of the class that generates the feedback for this language and style category.
        Arguments:
            testClient:  The test client we test this for.
    '''
    del testClient
    # generate a text with 400 and 400 words by multiplying a text with 8 words 
    # 50 times twice and then adding them together
    testTextPart1 = ('This is a large text with 400 words. ' * 50).strip()
    testTextPart2 = testTextPart1
    testText = testTextPart1 + '\n' + testTextPart2
    # retrieve the scores and explanations by running the function on the text
    feedbackObject = StructureFeedback(testText, '', 1, 1, '')
    score = feedbackObject.getParagraphScoreAndExplanations(testText)[0]
    explanations = feedbackObject.getParagraphScoreAndExplanations(testText)[1]
    # Since both testTextPart1 and testTextPart2 are the same, there should be
    # one key in explanations that is equal to testTextPart1 and testTextPart2
    # then check if the output scores and explanations match 
    assert score == Decimal(6.0).quantize(
        Decimal('0.1'), rounding=ROUND_HALF_UP)
    assert list(explanations.keys()) == [testTextPart1]
    assert list(explanations.keys()) == [testTextPart2]
    assert list(explanations.values()) == [
        'This paragraph is too long, try to make paragraphs with approximately 200 words.']

def test_empty_paragraphScores_list(testClient):
    '''
        Test if a text that has the paragraphScores list empty returns 0 as
        the score. The explanations will also be empty
        Attributes:
            testText: the text the function is run on.
            score: the score given for the structure writing skill.
            explanations: the explanations given for this text for the structure
            writing skill.
            feedbackObject: Object of the class that generates the feedback for this language and style category.
        Arguments:
            testClient: the test client we test this for.
    '''
    del testClient
    # make a text that will return the paragraphScores list as empty
    testText = 'empty paragraphScores list.'
    # retrieve the scores and explanations by running the function on the text
    feedbackObject = StructureFeedback(testText, '', 1, 1, '')
    score = feedbackObject.getParagraphScoreAndExplanations(testText)[0]
    explanations = feedbackObject.getParagraphScoreAndExplanations(testText)[1]
    # the score should be 0 and there should be no explanations
    assert score == Decimal(0).quantize(
        Decimal('0.1'), rounding=ROUND_HALF_UP)
    assert list(explanations.keys()) == []
    assert list(explanations.values()) == []