from decimal import ROUND_HALF_UP, Decimal
from app.structureCheck import getParagraphScore


def test_zero_words():
    '''
        Test if a text with zero words returns None.
    '''
    score = getParagraphScore('')
    assert score == None


def test_400_words():
    '''
        Test if a text with 400 words returns 
        (100.0 - 0.4 * max(0.0, 400 - 300)) / 10.0 = 6.0
    '''
    testText = ('This is a large text with 400 words. ' * 50).strip()
    score = getParagraphScore(testText)
    assert score == Decimal(6.0).quantize(
        Decimal('0.1'), rounding=ROUND_HALF_UP)

def test_50_words():
    '''
        Test if a text with 50 words returns 
        (100.0 - 0.6 * max(0.0, 100 - 50)) / 10.0 = 7.0
    '''
    testText = ('A short 50 word text. ' * 10).strip()
    score = getParagraphScore(testText)
    assert score == Decimal(7.0).quantize(
        Decimal('0.1'), rounding=ROUND_HALF_UP)

def test_200_words():
    '''
        Test if a text with 200 words returns 10.0
    '''
    testText = ('This is a good text with 200 words. ' * 25).strip()
    score = getParagraphScore(testText)
    assert score == Decimal(10.0).quantize(
        Decimal('0.1'), rounding=ROUND_HALF_UP)

def test_2_paragraphs_large_different_lengths():
    '''
        Test if a text with 2 paragraphs of 350 and 450 words returns 6.0
        (100.0 - 0.4 * max(0.0, 350 - 300)) / 10.0 = 8.0 and 
        (100.0 - 0.4 * max(0.0, 450 - 300)) / 10.0 = 4.0
        So the score should be (8.0 + 4.0) / 2 = 6.0
    '''
    testTextPart1 = ('A big 350 word text. ' * 70).strip()
    testTextPart2 = ('A bigger 450 word text. ' * 90).strip()
    testText = testTextPart1 + '\n' + testTextPart2
    score = getParagraphScore(testText)
    assert score == Decimal(6.0).quantize(
        Decimal('0.1'), rounding=ROUND_HALF_UP)

def test_2_paragraphs_small_different_lengths():
    '''
        Test if a text with 2 paragraphs of 30 and 70 words returns 7.0
        (100.0 - 0.6 * max(0.0, 100 - 30)) / 10.0 = 5.8 and 
        (100.0 - 0.6 * max(0.0, 100 - 70)) / 10.0 = 8.2
        So the score should be (5.8 + 8.2) / 2 = 7.0
    '''
    testTextPart1 = ('A very short 30 word text. ' * 5).strip()
    testTextPart2 = ('A small bit longer 70 word text. ' * 10).strip()
    testText = testTextPart1 + '\n' + testTextPart2
    score = getParagraphScore(testText)
    assert score == Decimal(7.0).quantize(
        Decimal('0.1'), rounding=ROUND_HALF_UP)

def test_2_paragraphs_good_different_lengths():
    '''
        Test if a text with 2 paragraphs of 150 and 250 words returns 10.0
        The score should be (10.0 + 10.0) / 2 = 10.0
    '''
    testTextPart1 = ('A good 150 word text. ' * 30).strip()
    testTextPart2 = ('Another good 250 word text ' * 50).strip()
    testText = testTextPart1 + '\n' + testTextPart2
    score = getParagraphScore(testText)
    assert score == Decimal(10.0).quantize(
        Decimal('0.1'), rounding=ROUND_HALF_UP)

def test_4_paragraphs_all_lengths():
    '''
        Test if a text with 4 paragraphs of 0, 400, 50 and 200 words returns 
        7.7. Note that (100.0 - 0.4 * max(0.0, 400 - 300)) / 10.0 = 6.0 and 
        (100.0 - 0.6 * max(0.0, 100 - 50)) / 10.0 = 7.0
        The score should be (6.0 + 7.0 + 10.0) / 3 = 7.7
    '''
    testTextPart1 = ' '
    testTextPart2 = ('This is a large text with 400 words. ' * 50).strip()
    testTextPart3 = ('A short 50 word text. ' * 10).strip()
    testTextPart4 = ('This is a good text with 200 words. ' * 25).strip()
    testText = (testTextPart1 + '\n' + testTextPart2 + '\n' + testTextPart3 +
     '\n' + testTextPart4)
    score = getParagraphScore(testText)
    assert score == Decimal(7.7).quantize(
        Decimal('0.1'), rounding=ROUND_HALF_UP)
