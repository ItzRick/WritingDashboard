# Import natural language toolkit.
import nltk
from nltk.stem import WordNetLemmatizer
from collections import Counter

def getTTRscore(text):
    """
        Calculates the score of the Type-Token Ratio, this score is in the 
        range [0,1]. This is calculated by dividing the number of unique lemmas
        in a text by the total number of lemmas in a text. This is done in a
        window of 50 tokens.
        Attributes:
            tokens: list containing the text split up into tokens as strings.
            tagged: list containing tokens from text with an assigned 
                    part-of-speach tag as tuples consisting of two strings.
            lemmatized_tokens: list containing all the words from the text in
                    their lemmatized form as strings.
            unique_tokens_in_window: list containing the number of unique 
                    tokens in every window of window_size as integers.
            unique_tokens: float that is the average number of unique tokens 
                    per window_size.
            window_size: integer that decides the size of the window mentioned
                    before; initially this is 50, if there are less than 50 
                    tokens then it is the number of tokens.
            TTR_score: float, (average of) unique tokens / window length.
        Arguments:
            text: string, the text on which the TTR score should be calculated.
        Return:
            TTR_score: float, TTR score calculated as follows: (average of) 
                    unique tokens / window length.
    """
    
    # Function from nltk that lemmatizes tokens/words.
    lemmatizer = WordNetLemmatizer()

    # Function that splits text into tokens.
    tokens = nltk.word_tokenize(text)
    # Function that assigns a part-of-speach tag to each token.
    tagged = nltk.pos_tag(tokens)

    # Create list with all tokens lemmatized.
    # (and in lowercase for comparison)
    lemmatized_tokens = []
    for i in tagged:
        # Verbs        
        if (i[1][0:2] == "VB"):
            lemmatized_tokens.append(lemmatizer.lemmatize(i[0], pos="v")\
                .lower())
        # Adjectives
        elif (i[1][0:2] == "JJ"):
            lemmatized_tokens.append(lemmatizer.lemmatize(i[0], pos="a")\
                .lower())
        # Adverbs
        elif (i[1][0:2] == "RB"):
            lemmatized_tokens.append(lemmatizer.lemmatize(i[0], pos="r")\
                .lower())
        # Nouns (and everything else)
        else:
            lemmatized_tokens.append(lemmatizer.lemmatize(i[0]).lower())

    # Only keep words in token list.
    # (get rid of things like dots or comma's)
    for i in lemmatized_tokens:
        if i.isalpha() == False:
            lemmatized_tokens.pop(lemmatized_tokens.index(i))

    # Calculate the number of unique tokens for every 50 tokens.
    unique_tokens_in_window = []
    if len(lemmatized_tokens) > 50:
        for i in range(len(lemmatized_tokens)-50):
            unique_tokens_in_window.append(len(Counter(lemmatized_tokens\
                [i:50+i]).values()))
    else:
        unique_tokens_in_window.append(len(Counter(lemmatized_tokens)\
            .values()))
    
    # Take average of unique tokens.
    unique_tokens = sum(unique_tokens_in_window)/len(unique_tokens_in_window)

    # Size of window (in case the text is smaller than the window)
    window_size = len(lemmatized_tokens)
    if len(lemmatized_tokens) > 50:
        window_size = 50

    # Calculate the score.
    # (average of) unique tokens / window length
    TTR_score = unique_tokens/window_size

    # Return calculated TTR score.
    return TTR_score