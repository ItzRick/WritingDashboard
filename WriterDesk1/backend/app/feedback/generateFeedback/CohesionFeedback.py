from app.feedback.generateFeedback.BaseFeedback import BaseFeedback
import nltk
from nltk.stem import WordNetLemmatizer
from collections import Counter
from app.feedback.nltkDownload import downloadNltkCohesion
import os

class CohesionFeedback(BaseFeedback):

    def __init__(self, text, referencesText, fileId, userId, filePath):
        super().__init__(text, referencesText, fileId, userId, filePath)
        self.explanationType 

    def genFeedback(self):
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
        downloadNltkCohesion()
        # If the text string is empty the function returns null.
        if self.text == "":
            return None

        # Retrieve variables from getTTRScore and getConnectiveScore.
        TTRScore, mostCommon = self.getTTRScore(self.text)
        connectivesScore, indexScore = self.getConnectiveScore(self.text)

        # Calculate the cohesionScore.    
        self.scoreCohesion = round((TTRScore + connectivesScore)/2, 2)

        # Message that gives the final score.
        scoreExplanation = "Your score for cohesion is " + str(self.scoreCohesion) + "."

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
        self.feedback = scoreExplanation + "\n" + TTRScoreExplanation + "\n" + \
            connectivesScoreExplanation + "\n" + connectivesExplanation

        self.addSingleExplanation(-1, -1, -1, -1, 1, self.feedback, '', [])

        return self.scoreCohesion, self.explanations

    def getConnectiveScore(self, text):
        """
            Calculates the score of the connectives use, this score is in the 
            range [0,10]. This is calculated by putting the division of the number
            of connectives used in a text by the total number of tokens in a text 
            into a formula which calculates the score. This formula is a 2nd order 
            polynomial in which we took into account the borders of the client for 
            a proper grade. 
            Attributes:
                connectivesCheck: list filled with all connectives from the TAACO
                        user manual as strings.
                tokens: list containing the text split up into tokens as strings.
                numberOfConnectives: integer, number of connectives in text.        
            Arguments:
                text: string, the text on which the connective score should be 
                        calculated.
            Return:
                connectivesScore: float, connectives score calculated as follows: 
                        -3.5 + 300*indexScore - 1666.667*indexScore^2. We take the
                        max of this result and 0, then we round the result to 2 
                        decimals.
                indexScore: float, calculated by dividing numberOfConnectives by
                        the size of tokens (the total number of tokens/words) in 
                        the text.
        """

        # If the text string is empty the function returns null.
        if text == "":
            return None

        BASEDIR = os.path.abspath(os.path.dirname(__file__))
        # Array containing a list of connectives, from the TAACO user guide.
        with open(os.path.join(BASEDIR, 'CohesionConnectives.txt'), 'rt') as fd:
            connectives = fd.read().split(', ')

        # Function that splits text into tokens.
        tokens = nltk.word_tokenize(text.lower())

        # Check how many connectives are in the text by checking if each token is 
        # in connectivesCheck. 
        # There are also connectives consisting of multiple words, this is at most
        # 4 words.
        numberOfConnectives = 0
        for i in tokens:
            if i in connectives:
                numberOfConnectives += 1
        # Check for connectives consisting of 2 tokens/words.
        if len(tokens) > 1:
            for i in range(len(tokens)-1):            
                if tokens[i] + ' ' + tokens[i+1] in connectives:
                    numberOfConnectives += 1
        # Check for connectives consisting of 3 tokens/words.
        if len(tokens) > 2:
            for i in range(len(tokens)-2):            
                if tokens[i] + ' ' + tokens[i+1] + ' ' + tokens[i+2] in connectives:
                    numberOfConnectives += 1
        # Check for connectives consisting of 4 tokens/words.
        if len(tokens) > 3:
            for i in range(len(tokens)-3):            
                if tokens[i] + ' ' + tokens[i+1] + ' ' + tokens[i+2] + ' ' + tokens[i+3] in connectives:                
                    numberOfConnectives += 1

        # Only keep words in token list.
        # (get rid of things like dots or comma's)
        for i in tokens:
            if i.isalpha() == False:
                tokens.pop(tokens.index(i))

        # Calculate index score by dividing the number of connectives in the text
        # by the total number of tokens (words) in the text.
        indexScore = numberOfConnectives/len(tokens)

        """
            Calculate the connectives score by putting the indexScore into the
            following 2nd order polynomial: y = -3.5 + 300*x - 1666.667*x^2, 
            where y is the connectives score and x is the indexScore. 
            In this polynomial we took into account the borders of the client for 
            a proper grade. The client told us that 0.03 is quite little and 0.15 
            is quite a lot. Thus we took the center of these as a perfect 10; 0.09.
            This polynomial has a y value of 10 for an index score (thus x value) 
            of 0.09. An x value of 0.03 and 0.15 both result in a y-value of 3, 
            which is how we interpeted "quite little" and "quite a lot".
            We take the max of this result and 0, since we grade in the range [0,10].
            Then we round the result to 2 decimals.
        """
        connectivesScore = round(max(-3.5 + 300*indexScore - 1666.667*indexScore**\
            2, 0), 2)
        
        # Return the calculated connectives score and indexScore.
        return connectivesScore, indexScore

    def getTTRScore(self, text):
        """
            Calculates the score of the Type-Token Ratio, this score is in the 
            range [0,10]. This is calculated by dividing the number of unique 
            lemmas in a text by the total number of lemmas in a text times 10. This
            is done in a window of 50 tokens.
            Attributes:
                tokens: list containing the text split up into tokens as strings.
                tagged: list containing tokens from text with an assigned 
                        part-of-speach tag as tuples consisting of two strings.
                lemmatizedTokens: list containing all the words from the text in
                        their lemmatized form as strings.
                uniqueTokensInWindow: list containing the number of unique 
                        tokens in every window of windowSize as integers.            
                uniqueTokens: float that is the average number of unique tokens 
                        per windowSize.
                windowSize: integer that decides the size of the window mentioned
                        before; initially this is 50, if there are less than 50 
                        tokens then that is the number of tokens.            
            Arguments:
                text: string, the text on which the TTR score should be calculated.
            Return:
                TTRScore: float, TTR score calculated as follows: (average of) 
                        unique tokens / window length * 10, rounded to 2 decimals.
                mostCommon: list containing the three most used words in the text
                        as strings (if there are less than three then that many),
                        to be used in generateFeedback.
        """
        # If the text string is empty the function returns null.
        if text == "":
            return None

        # Function from nltk that lemmatizes tokens/words.
        lemmatizer = WordNetLemmatizer()

        # Function that splits text into tokens.
        tokens = nltk.word_tokenize(text)    

        # Only keep words in token list.
        # (get rid of things like dots or comma's)
        for i in tokens:
            if i.isalpha() == False:
                tokens.pop(tokens.index(i))

        # Make all tokens lowercase.
        for i in range(len(tokens)):
            tokens[i] = tokens[i].lower()

        # Function that assigns a part-of-speach tag to each token.
        tagged = nltk.pos_tag(tokens)

        # Create list with all tokens lemmatized.
        lemmatizedTokens = []
        for i in tagged:
            # Verbs        
            if (i[1][0:2] == "VB"):
                lemmatizedTokens.append(lemmatizer.lemmatize(i[0], pos="v"))               
            # Adjectives
            elif (i[1][0:2] == "JJ"):
                lemmatizedTokens.append(lemmatizer.lemmatize(i[0], pos="a"))               
            # Adverbs
            elif (i[1][0:2] == "RB"):
                lemmatizedTokens.append(lemmatizer.lemmatize(i[0], pos="r"))                
            # Nouns (and everything else)
            else:
                lemmatizedTokens.append(lemmatizer.lemmatize(i[0]))
        
        # Calculate the number of unique tokens for every 50 tokens.
        uniqueTokensInWindow = []
        if len(lemmatizedTokens) > 50:
            for i in range(len(lemmatizedTokens)-49):
                uniqueTokensInWindow.append(len(Counter(lemmatizedTokens\
                    [i:50+i]).values()))            
        else:
            uniqueTokensInWindow.append(len(Counter(lemmatizedTokens)\
                .values()))     

        # Get the three most common words out of the text.
        # If there are less then those are the most common words.
        # This is for the feedback.
        mostCommon = [word[0] for word in Counter(lemmatizedTokens).most_common(3)]

        # Take average of unique tokens.
        uniqueTokens = sum(uniqueTokensInWindow)/len(uniqueTokensInWindow)

        # Size of window (in case the text is smaller than the window).
        windowSize = len(lemmatizedTokens)
        if len(lemmatizedTokens) > 50:
            windowSize = 50

        # Calculate the score:
        # (average of) unique tokens / window length
        # Then we round the result to 2 decimals.
        TTRScore = round(uniqueTokens/windowSize*10, 2)
        
        # Return calculated TTR score and 3 most common words.
        return TTRScore, mostCommon

    
