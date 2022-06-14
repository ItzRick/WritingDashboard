from decimal import ROUND_HALF_UP, Decimal
from app.structureCheck import getParagraphScoreAndExplanations


def test_zero_words():
    '''
        Test if a text with zero words returns None.
    '''
    output = getParagraphScoreAndExplanations('')
    assert output == None


def test_400_words():
    '''
        Test if a text with 400 words returns 
        (100.0 - 0.4 * max(0.0, 400 - 300)) / 10.0 = 6.0 as score and
        returns a dictionary with the paragraph as key and the string 
        'This paragraph is too long, try to make paragraphs with less words.'
        as value.
    '''
    testText = ('This is a large text with 400 words. ' * 50).strip()
    score = getParagraphScoreAndExplanations(testText)[0]
    explanations = getParagraphScoreAndExplanations(testText)[1]
    assert score == Decimal(6.0).quantize(
        Decimal('0.1'), rounding=ROUND_HALF_UP)
    assert list(explanations.keys()) == [testText]
    assert list(explanations.values()) == [
        'This paragraph is too long, try to make paragraphs with less words.']

def test_50_words():
    '''
        Test if a text with 50 words returns 
        (100.0 - 0.6 * max(0.0, 100 - 50)) / 10.0 = 7.0 as score and
        returns a dictionary with the paragraph as key and the string 
        'This paragraph is too short, try to make paragraphs with more words.'
        as value.
    '''
    testText = ('A short 50 word text. ' * 10).strip()
    score = getParagraphScoreAndExplanations(testText)[0]
    explanations = getParagraphScoreAndExplanations(testText)[1]
    assert score == Decimal(7.0).quantize(
        Decimal('0.1'), rounding=ROUND_HALF_UP)
    assert list(explanations.keys()) == [testText]
    assert list(explanations.values()) == [
        'This paragraph is too short, try to make paragraphs with more words.']

def test_200_words():
    '''
        Test if a text with 200 words returns 10.0 as score and returns an empty
        dictionary since 200 words in a paragraph is good.
    '''
    testText = ('This is a good text with 200 words. ' * 25).strip()
    score = getParagraphScoreAndExplanations(testText)[0]
    explanations = getParagraphScoreAndExplanations(testText)[1]
    assert score == Decimal(10.0).quantize(
        Decimal('0.1'), rounding=ROUND_HALF_UP)
    assert list(explanations.keys()) == []
    assert list(explanations.values()) == []

def test_2_paragraphs_large_different_lengths():
    '''
        Test if a text with 2 paragraphs of 350 and 450 words returns 6.0
        (100.0 - 0.4 * max(0.0, 350 - 300)) / 10.0 = 8.0 and 
        (100.0 - 0.4 * max(0.0, 450 - 300)) / 10.0 = 4.0
        So the score should be (8.0 + 4.0) / 2 = 6.0 and it returns a dictionary
        with the paragraphs as keys and the string 
        'This paragraph is too long, try to make paragraphs with less words.'
        as values.
    '''
    testTextPart1 = ('A big 350 word text. ' * 70).strip()
    testTextPart2 = ('A bigger 450 word text. ' * 90).strip()
    testText = testTextPart1 + '\n' + testTextPart2
    score = getParagraphScoreAndExplanations(testText)[0]
    explanations = getParagraphScoreAndExplanations(testText)[1]
    assert score == Decimal(6.0).quantize(
        Decimal('0.1'), rounding=ROUND_HALF_UP)
    assert list(explanations.keys()) == [testTextPart1, testTextPart2]
    assert list(explanations.values()) == [
        'This paragraph is too long, try to make paragraphs with less words.',
        'This paragraph is too long, try to make paragraphs with less words.']

def test_2_paragraphs_small_different_lengths():
    '''
        Test if a text with 2 paragraphs of 30 and 70 words returns 7.0
        (100.0 - 0.6 * max(0.0, 100 - 30)) / 10.0 = 5.8 and 
        (100.0 - 0.6 * max(0.0, 100 - 70)) / 10.0 = 8.2
        So the score should be (5.8 + 8.2) / 2 = 7.0 and it returns a
        dictionary with the paragraphs as keys and the string 
        'This paragraph is too short, try to make paragraphs with more words.'
        as values.
    '''
    testTextPart1 = ('A very short 30 word text. ' * 5).strip()
    testTextPart2 = ('A small bit longer 70 word text. ' * 10).strip()
    testText = testTextPart1 + '\n' + testTextPart2
    score = getParagraphScoreAndExplanations(testText)[0]
    explanations = getParagraphScoreAndExplanations(testText)[1]
    assert score == Decimal(7.0).quantize(
        Decimal('0.1'), rounding=ROUND_HALF_UP)
    assert list(explanations.keys()) == [testTextPart1, testTextPart2]
    assert list(explanations.values()) == [
        'This paragraph is too short, try to make paragraphs with more words.',
        'This paragraph is too short, try to make paragraphs with more words.']

def test_2_paragraphs_good_different_lengths():
    '''
        Test if a text with 2 paragraphs of 150 and 250 words returns 10.0
        The score should be (10.0 + 10.0) / 2 = 10.0 and it returns an empty
        dictionary since 150 and 250 words in a paragraph is good.
    '''
    testTextPart1 = ('A good 150 word text. ' * 30).strip()
    testTextPart2 = ('Another good 250 word text ' * 50).strip()
    testText = testTextPart1 + '\n' + testTextPart2
    score = getParagraphScoreAndExplanations(testText)[0]
    explanations = getParagraphScoreAndExplanations(testText)[1]
    assert score == Decimal(10.0).quantize(
        Decimal('0.1'), rounding=ROUND_HALF_UP)
    assert list(explanations.keys()) == []
    assert list(explanations.values()) == []

def test_4_paragraphs_all_lengths():
    '''
        Test if a text with 4 paragraphs of 0, 400, 50 and 200 words returns 
        7.7. Note that (100.0 - 0.4 * max(0.0, 400 - 300)) / 10.0 = 6.0 and 
        (100.0 - 0.6 * max(0.0, 100 - 50)) / 10.0 = 7.0
        The score should be (6.0 + 7.0 + 10.0) / 3 = 7.7 and it returns a
        dictionary with the paragraphs of 400 and 50 words as keys and the 
        strings 'This paragraph is too long, try to make paragraphs with less
        words.' and 'This paragraph is too short, try to make paragraphs with 
        more words.' as correspoding values.
    '''
    testTextPart1 = ' '
    testTextPart2 = ('This is a large text with 400 words. ' * 50).strip()
    testTextPart3 = ('A short 50 word text. ' * 10).strip()
    testTextPart4 = ('This is a good text with 200 words. ' * 25).strip()
    testText = (testTextPart1 + '\n' + testTextPart2 + '\n' + testTextPart3 +
     '\n' + testTextPart4)
    score = getParagraphScoreAndExplanations(testText)[0]
    explanations = getParagraphScoreAndExplanations(testText)[1]
    assert score == Decimal(7.7).quantize(
        Decimal('0.1'), rounding=ROUND_HALF_UP)
    assert list(explanations.keys()) == [testTextPart2, testTextPart3]
    assert list(explanations.values()) == [
        'This paragraph is too long, try to make paragraphs with less words.',
        'This paragraph is too short, try to make paragraphs with more words.']

def test_2_paragraphs_large_same_content():
    '''
        Test if a text with 2 paragraphs of 400 words returns 6.0 because
        (100.0 - 0.4 * max(0.0, 400 - 300)) / 10.0 = 6.0 and 
        (100.0 - 0.4 * max(0.0, 400 - 300)) / 10.0 = 6.0
        So the score should be (6.0 + 6.0) / 2 = 6.0 and it returns a dictionary
        with the content as key and the string 
        'This paragraph is too long, try to make paragraphs with less words.'
        as value.
    '''
    testTextPart1 = ('This is a large text with 400 words. ' * 50).strip()
    testTextPart2 = testTextPart1
    testText = testTextPart1 + '\n' + testTextPart2
    score = getParagraphScoreAndExplanations(testText)[0]
    explanations = getParagraphScoreAndExplanations(testText)[1]
    # Since both testTextPart1 and testTextPart2 are the same, there should be
    # one key in explanations that is equal to testTextPart1 and testTextPart2
    assert score == Decimal(6.0).quantize(
        Decimal('0.1'), rounding=ROUND_HALF_UP)
    assert list(explanations.keys()) == [testTextPart1]
    assert list(explanations.keys()) == [testTextPart2]
    assert list(explanations.values()) == [
        'This paragraph is too long, try to make paragraphs with less words.']