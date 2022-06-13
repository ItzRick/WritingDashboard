import language_tool_python
import re


def feedbackLanguageStyle(text):
    """
    Generates feedback on the language & style of the input string.
    This includes grammar mistakes and spelling mistakes.
    Attributes:
        tool: LanguageTool object to generate feedback.
        matches: List of Match objects containing the feedback.
        match: Match object containing the feedback.
        prevMatchEnd: End character of previous match in loop.
        occurrenceCount: count the occurrences of a mistake in the context.
        occurrenceInContext: The number of the correct occurrence of the mistake in the context.
        wordMatch: Match of word in context.
        context: context of mistake text.
    Arguments:
        text: Input string that will be given feedback on.
    Returns:
        mistakes: List of mistakes in text including matched text, context,
                  occurrence of text in context, explanation, and possible replacements.
        score: Score between 0 and 10 given to the text based on the feedback.
    """

    # Instantiate language tool
    # TODO: Remove out of function to improve performance
    tool = language_tool_python.LanguageTool('en-US')

    # Check for mistakes
    matches = tool.check(text)

    mistakes = []
    for match in matches:

        prevMatchEnd = -1  # Position of last character of previous match in loop, initiated on -1
        occurrenceCount = 0  # Number of occurrences of a mistake
        occurrenceInContext = 0  # Final count of occurrences of a mistake

        # Find all occurrences of a mistake in the context
        for wordMatch in re.finditer(match.matchedText.lower().replace('(', '\(').replace(')', '\)'),
                                     match.context.lower()):
            if not (wordMatch.start() <= prevMatchEnd):
                # Mistake overlaps previous mistake and does not count to occurrences

                if wordMatch.start() == match.offsetInContext:
                    occurrenceInContext = occurrenceCount  # Set occurrenceInContext
                else:
                    occurrenceCount += 1
            prevMatchEnd = wordMatch.end()

        context = match.context

        # Remove starting and ending ...
        if context[:3] == '...':
            context = context[3:]
        if context[-3:] == '...':
            context = context[:-3]

        # Append matched text, context, occurrence in context, explanation, and top 3 replacements to a list
        mistakes.append([match.matchedText, context, occurrenceInContext, match.message, match.replacements[:3]])

    # Compute score
    score = calculateScore(len(matches), len(text.split()))

    return mistakes, score


def calculateScore(nrOfMistakes, nrOfWords):
    """
    Calculates a score for a text given the number of mistakes and number of words.
    Arguments:
        nrOfMistakes: Number of mistakes in a text.
        nrOfWords: Number of total words of a text.
    Returns:
        score: Score between 0 and 10 given to the feedback.
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