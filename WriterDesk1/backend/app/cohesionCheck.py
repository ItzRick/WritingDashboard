def generateExplanation(text):
    """
        Calculates the final score of the cohesion in the text, this score is
        in the range [0,10]. This is calculated by taking the "gemiddelde" of
        the TTRScore and the connectivesScore. 
        Generates feedback text as a string. This feedback is determined by how
        high the TTR score and connective score are.
        Attributes:
            TTRScore: float, TTR score retrieved from function getTTRScore.
            mostCommon: list containing the three most used words in the text
                    as strings, retrieved from getTTRScore.
            connectivesScore: float, connectives score retrieved from function
                    getConnectivesScore.
            indexScore: float, index score retrieved from function
                    getConnectivesScore.
            cohesionScore: float, calculated by calculating the average of
                    TTRScore and connectivesScore, rounded to 2 decimals. This
                    is the final score that the user will get.
            scoreExplanation: string, gives the final score; cohesionScore.
            TTRScoreExplanation: string, gives feedback on how to improve the
                    TTRScore.
            connectivesScoreExplanation: string, gives feedback on how to
                    improve the connectivesScore, the indexScore has some
                    influence on this as well.
            feedback: string, combination of scoreExplanation, 
                    TTRScoreExplanation and connectivesScoreExplanation. This
                    is the feedback that the user will see.
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

    # Retrieve variables from getTTRScore and getConnectiveScore.
    TTRScore, mostCommon = getTTRScore(text)
    connectivesScore, indexScore = getConnectiveScore(text)

    # Calculate the cohesionScore.    
    cohesionScore = round((TTRScore + connectivesScore)/2, 2)

    # Message that gives the final score.
    scoreExplanation = "Your score for cohesion is " + str(cohesionScore) + "."

    # Generate feedback on the TTR score.
    # Depending on how high the TTR score is, different feedback is provided. 
    # If the grade is lower than a 9, the feedback also provides the three most
    # used words.
    if TTRScore >= 9:
        TTRScoreExplanation = "The amount of variation of words you use is\
            very good."
    elif TTRScore >= 7:
        TTRScoreExplanation = "You used enough variation of words, however you\
            could improve this some more. These are your three most used words\
            : \"" + mostCommon[0] + "\", \"" + mostCommon[1] + "\" and \"" + \
            mostCommon[2] + "\"."
    elif TTRScore >= 5:
        TTRScoreExplanation = "You barely have enough variation of words, you\
            should improve on this. These are your three most used words: \"" \
            + mostCommon[0] + "\", \"" + mostCommon[1] + "\" and \"" + \
            mostCommon[2] + "\"."
    else: 
        TTRScoreExplanation - "You did not use enough variation in terms of\
            words, you are using the same words too much. These are your three\
            most used words: \"" + mostCommon[0] + "\", \"" + mostCommon[1] + \
            "\" and \"" + mostCommon[2] + "\"."

    # Generate feedback on the connectives score.
    # Depending on how high the connectives score is, different feedback is 
    # provided. 
    # This is also dependend of the indexScore, since if you have a low index
    # score then you are not using enough connectives, whereas if it is too 
    # high then you are using too many. 
    if connectivesScore >= 9:
        connectivesScoreExplanation = "The amount of connectives you used is\
            very good."
    elif connectivesScore >= 7:
        if indexScore < 0.9:
            connectivesScoreExplanation = "You could use some more connectives\
                in your text."
        else: 
            connectivesScoreExplanation = "You could use a bit less\
                connectives in your text."
    elif connectivesScore >= 5:
        if indexScore < 0.9:
            connectivesScoreExplanation = "You should use more connectives in\
                your text."
        else: 
            connectivesScoreExplanation = "You should use less connectives in\
                your text."
    else: 
        if indexScore < 0.9:
            connectivesScoreExplanation = "You don't have enough connectives\
                in your text."
        else: 
            connectivesScoreExplanation = "You have too many connectives in\
                your text."    

    # A small explanation of what connectives are.
    connectivesExplanation = "Connectives are words or phrases that link other\
        linguistic units."

    # The resulting feedback, containing the overall score, feedback on how to
    # improve your score and a small explanation on what connectives are.
    feedback = scoreExplanation + "\n" + TTRScoreExplanation + "\n" + \
        connectivesScoreExplanation + "\n" + connectivesExplanation

    return cohesionScore, feedback