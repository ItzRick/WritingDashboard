from app.languageAndStyle import feedbackLanguageStyle


def testFeedbackLanguageAn(testClient):
    """
    Function to test language and style feedback with single sentence with 'an' mistake.
    Arguments:
        testClient: The test client we test this for.
    Attributes:
        mistakes: List of mistakes in text including matched text, context,
                  occurrence of text in context, explanation, and possible replacements.
        score: Score given to the text based on the feedback.
    """
    del testClient

    mistakes, score = feedbackLanguageStyle("This is an sentence with a mistake.")
    assert 0 <= score <= 10  # Score is between 0 and 10
    assert mistakes[0][0] == "an"  # Word of mistake
    assert mistakes[0][1] == "This is an sentence with a mistake."  # Context of mistake
    assert len(mistakes) == 1  # There is only one language and style mistake in the sentence


def testFeedbackLanguageEmpty(testClient):
    """
    Function to test language and style feedback with empty sentence.
    Arguments:
        testClient: The test client we test this for.
    Attributes:
        mistakes: List of mistakes in text including matched text, context,
                  occurrence of text in context, explanation, and possible replacements.
        score: Score given to the text based on the feedback.
    """
    del testClient

    mistakes, score = feedbackLanguageStyle('')
    assert score == 0  # Score is 0 when there is no text
    assert len(mistakes) == 0  # No language and style mistakes


def testFeedbackLanguageMultipleSentences(testClient):
    """
    Function to test language and style feedback with multiple sentence and multiple mistakes.
    Arguments:
        testClient: The test client we test this for.
    Attributes:
        mistakes: List of mistakes in text including matched text, context,
                  occurrence of text in context, explanation, and possible replacements.
        score: Score given to the text based on the feedback.
    """
    del testClient

    mistakes, score = feedbackLanguageStyle("Hello, My name is Susan. I'm forteen and I life in germany.")
    assert 0 <= score <= 10  # Score is between 0 and 10

    assert mistakes[0][0] == "forteen"  # First mistake in text
    assert "fourteen" in mistakes[0][4]  # Correction of mistake

    assert mistakes[1][0] == "life"  # Second mistake in text
    assert "live" in mistakes[1][4]  # Correction of mistake

    assert mistakes[2][0] == "germany"  # Third mistake in text
    assert "Germany" in mistakes[2][4]  # Correction of mistake

    assert len(mistakes) == 3  # 3 language and style mistakes in the text


def testFeedbackLanguageMissingLetter(testClient):
    """
    Function to test language and style feedback with word with missing letter.
    Arguments:
        testClient: The test client we test this for.
    Attributes:
        mistakes: List of mistakes in text including matched text, context,
                  occurrence of text in context, explanation, and possible replacements.
        score: Score given to the text based on the feedback.
    """
    del testClient

    mistakes, score = feedbackLanguageStyle("The computr was hot and overheated.")
    assert 0 <= score <= 10

    assert mistakes[0][0] == "computr"  # Word of mistake
    assert mistakes[0][1] == "The computr was hot and overheated."  # Context of mistake
    assert "computer" in mistakes[0][4]  # Correction of mistake

    assert len(mistakes) == 1  # There is only one language and style mistake in the sentence


def testFeedbackLanguagePerfectSentence(testClient):
    """
    Function to test language and style feedback with correct sentence.
    Arguments:
        testClient: The test client we test this for.
    Attributes:
        mistakes: List of mistakes in text including matched text, context,
                  occurrence of text in context, explanation, and possible replacements.
        score: Score given to the text based on the feedback.
    """
    del testClient

    mistakes, score = feedbackLanguageStyle("Are you opening the door?")
    assert score == 10  # Perfect score for correct sentence

    assert len(mistakes) == 0  # No mistakes in sentence

