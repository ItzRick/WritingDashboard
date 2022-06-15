# Import natural language toolkit.
import nltk
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('wordnet')
nltk.download('omw-1.4')
from nltk.stem import WordNetLemmatizer
from collections import Counter

from sqlalchemy import null

def getTTRScore(text):
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
            mostCommon: list containing the three most used words in the text
                    as strings, to be used in generateFeedback.
            uniqueTokens: float that is the average number of unique tokens 
                    per windowSize.
            windowSize: integer that decides the size of the window mentioned
                    before; initially this is 50, if there are less than 50 
                    tokens then it is the number of tokens.
            TTRScore: float, (average of) unique tokens / window length * 10,
                    rounded to 2 decimals.
        Arguments:
            text: string, the text on which the TTR score should be calculated.
        Return:
            TTRScore: float, TTR score calculated as follows: (average of) 
                    unique tokens / window length * 10, rounded to 2 decimals.
            mostCommon: list containing the three most used words in the text
                    as strings, to be used in generateFeedback.
    """
    
    # If the text string is empty the function returns null.
    if text == "":
        return null

    # Function from nltk that lemmatizes tokens/words.
    lemmatizer = WordNetLemmatizer()

    # Function that splits text into tokens.
    tokens = nltk.word_tokenize(text)    

    # Only keep words in token list.
    # (get rid of things like dots or comma's)
    for i in tokens:
        if i.isalpha() == False:
            tokens.pop(tokens.index(i))

    # Function that assigns a part-of-speach tag to each token.
    tagged = nltk.pos_tag(tokens)

    # Create list with all tokens lemmatized.
    # (and in lowercase for comparison)
    lemmatizedTokens = []
    for i in tagged:
        # Verbs        
        if (i[1][0:2] == "VB"):
            lemmatizedTokens.append(lemmatizer.lemmatize(i[0], pos="v")\
                .lower())
        # Adjectives
        elif (i[1][0:2] == "JJ"):
            lemmatizedTokens.append(lemmatizer.lemmatize(i[0], pos="a")\
                .lower())
        # Adverbs
        elif (i[1][0:2] == "RB"):
            lemmatizedTokens.append(lemmatizer.lemmatize(i[0], pos="r")\
                .lower())
        # Nouns (and everything else)
        else:
            lemmatizedTokens.append(lemmatizer.lemmatize(i[0]).lower())
    
    # Calculate the number of unique tokens for every 50 tokens.
    uniqueTokensInWindow = []
    if len(lemmatizedTokens) > 50:
        for i in range(len(lemmatizedTokens)-50):
            uniqueTokensInWindow.append(len(Counter(lemmatizedTokens\
                [i:50+i]).values()))            
    else:
        uniqueTokensInWindow.append(len(Counter(lemmatizedTokens)\
            .values()))     

    # Get the three most common words out of the text.
    # This is for the feedback.
    mostCommon = [word[0] for word in Counter(lemmatizedTokens).most_common(3)]

    # Take average of unique tokens.
    uniqueTokens = sum(uniqueTokensInWindow)/len(uniqueTokensInWindow)

    # Size of window (in case the text is smaller than the window)
    windowSize = len(lemmatizedTokens)
    if len(lemmatizedTokens) > 50:
        windowSize = 50

    # Calculate the score.
    # (average of) unique tokens / window length
    # Then we round the result to 2 decimals.
    TTRScore = round(uniqueTokens/windowSize*10, 2)
    
    # Return calculated TTR score and 3 most common words.
    return TTRScore, mostCommon