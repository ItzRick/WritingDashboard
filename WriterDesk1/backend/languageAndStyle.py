import language_tool_python


def feedbackLanguageStyle(text):
    """
    Generates feedback on the language & style of the input string.
    Attributes:
        tool: LanguageTool object to generate feedback.
        matches: List of Match objects containing the feedback.
        match: Match object containing the feedback.
    :param text: Input string that will be given feedback on.
    :returns:
        mistakes: List of mistakes in text including matched text, sentence, explanation, and possible replacements.
        score: Score between 0 and 10 given to the text based on the feedback.
    """

    # Instantiate language tool
    tool = language_tool_python.LanguageTool('en-US')

    # Check for mistakes
    matches = tool.check(text)

    mistakes = []
    for match in matches:
        # Append matched text, sentence, explanation, and top 3 replacements to a list
        mistakes.append([match.matchedText, match.sentence, match.message, match.replacements[:3]])

    # Compute score
    score = calculateScore(len(matches), len(text.split()))

    return mistakes, score


def calculateScore(nrOfMistakes, nrOfWords):
    """
    Calculates a score for a text given the number of mistakes and number of words.
    :param nrOfMistakes: Number of mistakes in a text.
    :param nrOfWords: Number of total words of a text.
    :return: Score between 0 and 10 given to the feedback.
    """

    # No division by 0
    if nrOfWords > 0:
        # Function to calculate score between 0 and 10
        score = max(0, -221.785 + (10 + 221.785) /
                    (1 + ((nrOfMistakes / nrOfWords) / 0.01911166) ** 1.415104) ** 0.007848222)
    else:
        score = 0

    # Round score to 1 decimal
    score = round(score, 1)

    return score
