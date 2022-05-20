from decimal import ROUND_HALF_UP, Decimal

def getParagraphScore(text):
    '''
        Return: scoreRounded: the score from 0 to 10 based on the average of the scores based on the amount of words in each paragraph.
        Attributes:
            paragraphScores: List that contains the scores of each paragraph.
            paragraphScore: The score of a paragraph.
            paragraphScoreRounded: The paraGraphScore rounded to one decimal behind the comma.
            score: The average score taken over all paragraphs.
            scoreRounded: The score rounded to one decimal behind the comma.
        Arguments:
            text: The text on which this will be run.

    '''
    # If the input text is empty.
    if len(text) == 0:
        return None

    # A list containing the scores for each paragraph in the text.
    paragraphScores = []

    # Split the text on white space to get each paragraph.
    for paragraph in text.splitlines():
        # If there are multiple white spaces in a row, continue.
        if len(paragraph.split()) == 0:
            continue
        # If the paragraph is more than 300 words.
        elif len(paragraph.split()) > 300:
            # paragraphScore is calculated by taking the max between 0.0 and (100.0 - 0.4 * (the amount of words - 300)) / 10.0 
            # to get a grade between 0.0 and 10.0. Having a high amount of words is worse than having a low amount of words.
            paragraphScore = max((100.0 - 0.4 * (len(paragraph.split()) - 300)) / 10.0, 0.0)
            paragraphScoreRounded = Decimal(paragraphScore).quantize(Decimal('0.1'), rounding=ROUND_HALF_UP) 
            paragraphScores.append(paragraphScoreRounded)
        # If the paragraph is less than 100 words.
        elif len(paragraph.split()) < 100:
            # paragraphScore is calculated by taking the max between 0.0 and (100.0 - 0.6 * (100 - the amount of words)) / 10.0 
            # to get a grade between 0.0 and 10.0. Having a low amount of words is not as bad as having a high amount of words.
            paragraphScore = max((100.0 - 0.6 * (100 - len(paragraph.split()))) / 10.0, 0.0)
            paragraphScoreRounded = Decimal(paragraphScore).quantize(Decimal('0.1'), rounding=ROUND_HALF_UP)
            paragraphScores.append(paragraphScoreRounded)        
        else:
        # If the paragraph is between 100 and 300 words.
            paragraphScores.append(Decimal(10.0).quantize(Decimal('0.1'), rounding=ROUND_HALF_UP))

    # Take the average score of each paragraph and round it to one decimal behind the comma.
    score = sum(paragraphScores) / len(paragraphScores)
    scoreRounded = Decimal(score).quantize(Decimal('0.1'), rounding=ROUND_HALF_UP)

    return scoreRounded



def getStructureScore(text):
    '''
        Return: scoreRouned: the score for the structure writing skill (in this case based on paragraph size only).
        Attributes:
            scores: a list of scores that contains the scores of all different structure aspects (in this case paragraph size only).
            score: the score for the structure writing skill.
            scoreRounded = the score rounded to one decimal behind the comma.
        Arguments:
            text: the text on which the structure score should be calculated.
    '''
    # If the input text is empty
    if len(text) == 0:
        return None
    
    scores = []
    # Multiple different ways of getting scores for the structure writing skill can be added here.
    scores.append(getParagraphScore(text))

    # Take the average score of each submethod of getting scores for the structure writing skill 
    # and round it to one decimal behind the comma.
    score = sum(scores) / len(scores)
    scoreRounded = Decimal(score).quantize(Decimal('0.1'), rounding=ROUND_HALF_UP)

    return scoreRounded

# TODO remove after more implementation is done.
text = 'Lorem ipsum dolor sit amet, \n consectetur adipiscing elit, \n sed do eiusmod tempor incididunt \n ut labore et dolore magna aliqua.'
getStructureScore(text)
