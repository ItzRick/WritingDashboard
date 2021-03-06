from app.feedback.generateFeedback.LanguageStyleFeedback import LanguageStyleFeedback


def testFeedbackLanguageAn(testClient):
    """
    Function to test language and style feedback with single sentence with 'an' mistake.
    Arguments:
        testClient: The test client we test this for.
    Attributes:
        mistakes: List of mistakes in text including matched text, context,
                  occurrence of text in context, explanation, and possible replacements.
        score: Score given to the text based on the feedback.
        feedbackObject: Object of the StructureFeedback class, to calculate scores for the Language and Style writing skill.
    """
    del testClient
    text = "This is an sentence with a mistake."
    feedbackObject = LanguageStyleFeedback(text, '', 1, 1, '')
    score, explanations = feedbackObject.genFeedback()
    assert 0 <= score <= 10  # Score is between 0 and 10
    assert explanations == []
    assert feedbackObject.explanationsList[0][0] == "an"  # Word of mistake
    assert feedbackObject.explanationsList[0][1] == "This is an sentence with a mistake."  # Context of mistake
    assert len(feedbackObject.explanationsList) == 1  # There is only one language and style mistake in the sentence


def testFeedbackLanguageEmpty(testClient):
    """
    Function to test language and style feedback with empty sentence.
    Arguments:
        testClient: The test client we test this for.
    Attributes:
        mistakes: List of mistakes in text including matched text, context,
                  occurrence of text in context, explanation, and possible replacements.
        score: Score given to the text based on the feedback.
        feedbackObject: Object of the StructureFeedback class, to calculate scores for the Language and Style writing skill.
    """
    del testClient
    text = ''
    feedbackObject = LanguageStyleFeedback(text, '', 1, 1, '')
    score, explanations = feedbackObject.genFeedback()
    assert explanations == []
    assert score == 0  # Score is 0 when there is no text
    assert len(feedbackObject.explanationsList) == 0  # No language and style mistakes


def testFeedbackLanguageMultipleSentences(testClient):
    """
    Function to test language and style feedback with multiple sentence and multiple mistakes.
    Arguments:
        testClient: The test client we test this for.
    Attributes:
        mistakes: List of mistakes in text including matched text, context,
                  occurrence of text in context, explanation, and possible replacements.
        score: Score given to the text based on the feedback.
        feedbackObject: Object of the StructureFeedback class, to calculate scores for the Language and Style writing skill.
    """
    del testClient
    text = "Hello, My name is Susan. I'm forteen and I life in germany."
    feedbackObject = LanguageStyleFeedback(text, '', 1, 1, '')
    score, explanations = feedbackObject.genFeedback()
    assert explanations == []
    assert 0 <= score <= 10  # Score is between 0 and 10

    assert feedbackObject.explanationsList[0][0] == "forteen"  # First mistake in text
    assert "fourteen" in feedbackObject.explanationsList[0][4]  # Correction of mistake

    assert feedbackObject.explanationsList[1][0] == "life"  # Second mistake in text
    assert "live" in feedbackObject.explanationsList[1][4]  # Correction of mistake

    assert feedbackObject.explanationsList[2][0] == "germany"  # Third mistake in text
    assert "Germany" in feedbackObject.explanationsList[2][4]  # Correction of mistake

    assert len(feedbackObject.explanationsList) == 3  # 3 language and style mistakes in the text


def testFeedbackLanguageMissingLetter(testClient):
    """
    Function to test language and style feedback with word with missing letter.
    Arguments:
        testClient: The test client we test this for.
    Attributes:
        mistakes: List of mistakes in text including matched text, context,
                  occurrence of text in context, explanation, and possible replacements.
        score: Score given to the text based on the feedback.
        feedbackObject: Object of the StructureFeedback class, to calculate scores for the Language and Style writing skill.
    """
    del testClient
    text = "The computr was hot and overheated."
    feedbackObject = LanguageStyleFeedback(text, '', 1, 1, '')
    score, explanations = feedbackObject.genFeedback()
    mistakes = feedbackObject.explanationsList
    assert explanations == []
    assert 0 <= score <= 10

    assert feedbackObject.explanationsList[0][0] == "computr"  # Word of mistake
    assert feedbackObject.explanationsList[0][1] == "The computr was hot and overheated."  # Context of mistake
    assert "computer" in mistakes[0][4]  # Correction of mistake

    assert len(feedbackObject.explanationsList) == 1  # There is only one language and style mistake in the sentence


def testFeedbackLanguagePerfectSentence(testClient):
    """
    Function to test language and style feedback with correct sentence.
    Arguments:
        testClient: The test client we test this for.
    Attributes:
        mistakes: List of mistakes in text including matched text, context,
                  occurrence of text in context, explanation, and possible replacements.
        score: Score given to the text based on the feedback.
        feedbackObject: Object of the StructureFeedback class, to calculate scores for the Language and Style writing skill.
    """
    del testClient
    text = "Are you opening the door?"
    feedbackObject = LanguageStyleFeedback(text, '', 1, 1, '')
    score, explanations = feedbackObject.genFeedback()
    assert explanations == []
    assert score == 10  # Perfect score for correct sentence

    assert len(feedbackObject.explanationsList) == 0  # No mistakes in sentence


def testFeedbackLanguageParenthesis(testClient):
    """
    Function to test language and style feedback with single sentence with '(' mistake.
    Arguments:
        testClient: The test client we test this for.
    Attributes:
        mistakes: List of mistakes in text including matched text, context,
                  occurrence of text in context, explanation, and possible replacements.
        score: Score given to the text based on the feedback.
        feedbackObject: Object of the StructureFeedback class, to calculate scores for the Language and Style writing skill.
    """
    del testClient
    text = "(This is a sentence with a missing parenthesis."
    feedbackObject = LanguageStyleFeedback(text, '', 1, 1, '')
    score, explanations = feedbackObject.genFeedback()
    assert explanations == []
    assert 0 <= score <= 10  # Score is between 0 and 10
    assert feedbackObject.explanationsList[0][0] == "("  # Word of mistake
    assert len(feedbackObject.explanationsList) == 1  # There is only one language and style mistake in the sentence


def testFeedbackLanguageParenthesis(testClient):
    """
    Function to test language and style feedback with single sentence with '(' mistake.
    Arguments:
        testClient: The test client we test this for.
    Attributes:
        mistakes: List of mistakes in text including matched text, context,
                  occurrence of text in context, explanation, and possible replacements.
        score: Score given to the text based on the feedback.
        feedbackObject: Object of the StructureFeedback class, to calculate scores for the Language and Style writing skill.
    """
    del testClient
    text = "(This is a sentence with a missing parenthesis."
    feedbackObject = LanguageStyleFeedback(text, '', 1, 1, '')
    score, explanations = feedbackObject.genFeedback()
    assert explanations == []
    assert 0 <= score <= 10  # Score is between 0 and 10
    assert feedbackObject.explanationsList[0][0] == "("  # Word of mistake
    assert len(feedbackObject.explanationsList) == 1  # There is only one language and style mistake in the sentence
