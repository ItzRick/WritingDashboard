from app.feedback.generateFeedback.CohesionFeedback import CohesionFeedback

def testConnectivesLowestManyConnectives(testClient, downloadNltk):
    '''
        Test if a text with a connectives score lower than 5 and an index score
        higher than 0.09 returns the correct feedback and score.
        This specific text has an index score of 1.0, a connective score of
        0.0 and a TTR score of 3.33, thus resulting in a score of 1.67.
        Hence, the feedback on connective score should be that of < 5 and
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
    text = "Although, although although."
    feedbackObject = CohesionFeedback(text, '', 1, 1, '')
    score = feedbackObject.genFeedback()
    expectedFeedback = feedbackObject.feedback
    expected_feedback = ("You have too many connectives in your text. You have"
        " a percentage of 100 in your text, ideally this would be 9 percent.")
    assert score[0] == 1.67
    assert expectedFeedback.splitlines()[2] == expected_feedback