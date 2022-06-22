# Import the functions that are called in this function.
from app.getTTRScore import getTTRScore
from app.getConnectiveScore import getConnectiveScore

def generateExplanation(text):
    """
        Calculates the final score of the cohesion in the text, this score is
        in the range [0,10]. This is calculated by taking the average of
        the TTRScore and the connectivesScore. 
        Generates feedback text as a string. This feedback is determined by how
        high the TTR score and connective score are.
        Attributes:
            TTRScore: float, TTR score retrieved from function getTTRScore.
            mostCommon: list containing the three most used words in the text
                    as strings (if there are less than three then that many),
                    retrieved from getTTRScore.
            connectivesScore: float, connectives score retrieved from function
                    getConnectivesScore.
            indexScore: float, index score retrieved from function
                    getConnectivesScore.
            scoreExplanation: string, gives the final score; cohesionScore.
            TTRScoreExplanation: string, gives feedback on how to improve the
                    TTRScore.
            connectivesScoreExplanation: string, gives feedback on how to
                    improve the connectivesScore, the indexScore has some
                    influence on this as well.
        Arguments:
            text: string, the text on which the cohesion score should be
                    calculated.
        Return:
            cohesionScore: float, calculated by calculating the average of
                    TTRScore and connectivesScore, rounded to 2 decimals. This
                    is the final score that the user will get.
            feedback: string, combination of scoreExplanation, 
                    TTRScoreExplanation and connectivesScoreExplanation. This
                    is the feedback that the user will see.
    """

    # If the text string is empty the function returns null.
    if text == "":
        return None

    # Retrieve variables from getTTRScore and getConnectiveScore.
    TTRScore, mostCommon = getTTRScore(text)
    connectivesScore, indexScore = getConnectiveScore(text)

    # Calculate the cohesionScore.    
    cohesionScore = round((TTRScore + connectivesScore)/2, 2)

    # Message that gives the final score.
    scoreExplanation = "Your score for cohesion is " + str(cohesionScore) + "."

    # Generate string that contains the most used words.
    # Initially these are the 3 most used words, if there are less words in 
    # text then those are the most used words.
    if len(mostCommon) == 0:
        mostCommonFeedback = "None"
    elif len(mostCommon) == 1:
        mostCommonFeedback = "\"" + mostCommon[0] + "\"."
    elif len(mostCommon) == 2: 
        mostCommonFeedback = "\"" + mostCommon[0] + "\" and \"" + mostCommon[1] + "\"."
    else:
        mostCommonFeedback = "\"" + mostCommon[0] + "\", \"" + mostCommon[1] + "\" and \"" + mostCommon[2] + "\"."
    
    """
        Generate feedback on the TTR score.
        Depending on how high the TTR score is, different feedback is provided.
        If the grade is lower than a 9, the feedback also provides the three
        most used words (if there are less than three then that many).
    """
    if TTRScore >= 9:
        TTRScoreExplanation = ("The amount of variation of words you use is "
            "good. You have more than 90 percent variation in your text.")
    elif TTRScore >= 7:
        TTRScoreExplanation = ("You used enough variation of words. You have "
            "in between 70 and 90 percent variation in your text. These are "
            "your most used words: "+ mostCommonFeedback)
    elif TTRScore >= 5:
        TTRScoreExplanation = ("You barely have enough variation of words. You"
            " have in between 50 and 70 percent variation in your text. These "
            "are your most used words: " + mostCommonFeedback)
    else: 
        TTRScoreExplanation = ("You did not use enough variation in terms of "
            "words. You have less than 50 percent variation in your text. "
            "These are your most used words: " + mostCommonFeedback)

    """
        Generate feedback on the connectives score.
        Depending on how high the connectives score is, different feedback is
        provided. 
        This is also dependend of the indexScore, since if you have a low index
        score then you are not using enough connectives, whereas if it is too
        high then you are using too many. 
    """
    if connectivesScore >= 9:
        connectivesScoreExplanation = ("The amount of connectives you used is "
            "good. You have a percentage of " + str(round(indexScore*100)) +
            " in your text, ideally this would be 9 percent.")
    elif connectivesScore >= 7:
        if indexScore < 0.09:
            connectivesScoreExplanation = ("You could use more "
            "connectives in your text. You have a percentage of " + 
            str(round(indexScore*100)) + " in your text, ideally this would"
            " be 9 percent.")
        else: 
            connectivesScoreExplanation = ("You could use less "
            "connectives in your text. You have a percentage of " + 
            str(round(indexScore*100)) + " in your text, ideally this would"
            " be 9 percent.")
    elif connectivesScore >= 5:
        if indexScore < 0.09:
            connectivesScoreExplanation = ("You should use more connectives in"
            " your text. You have a percentage of " + 
            str(round(indexScore*100)) + " in your text, ideally this would"
            " be 9 percent.")
        else: 
            connectivesScoreExplanation = ("You should use less connectives in"
            " your text. You have a percentage of " + 
            str(round(indexScore*100)) + " in your text, ideally this would"
            " be 9 percent.")
    else: 
        if indexScore < 0.09:
            connectivesScoreExplanation = ("You don't have enough connectives "
            "in your text. You have a percentage of " + 
            str(round(indexScore*100)) + " in your text, ideally this would"
            " be 9 percent.")
        else: 
            connectivesScoreExplanation = ("You have too many connectives in "
            "your text. You have a percentage of " + 
            str(round(indexScore*100)) + " in your text, ideally this would"
            " be 9 percent.")

    # A small explanation of what connectives are.
    connectivesExplanation = ("Connectives are words or phrases that link "
    "other linguistic units.")

    # The resulting feedback, containing the overall score, feedback on how to
    # improve your score and a small explanation on what connectives are.
    feedback = scoreExplanation + "\n" + TTRScoreExplanation + "\n" + \
        connectivesScoreExplanation + "\n" + connectivesExplanation
    
    return cohesionScore, feedback
