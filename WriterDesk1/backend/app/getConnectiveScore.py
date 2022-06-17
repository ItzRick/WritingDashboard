# Import natural language toolkit.
import nltk

def getConnectiveScore(text):
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
            indexScore: float, calculated by dividing numberOfConnectives by
                    the size of tokens (the total number of tokens/words) in 
                    the text.
            connectivesScore: float, connectives score calculated as follows: 
                    -3.5 + 300*indexScore - 1666.667*indexScore^2. We take the
                    max of this result and 0, then we round the result to 2 
                    decimals.
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

    # Array containing a list of connectives, from the TAACO user guide.
    connectivesCheck = ['actually', 'admittedly', 'after', 'again', 
    'all in all', 'all this time', 'also', 'alternatively', 'although', 'and',
    'anyhow', 'anyway', 'arise', 'arises', 'arising', 'arose', 'as', 'at last', 
    'at least', 'at once', 'at the same time', 'at this moment', 
    'at this point', 'because', 'before', 'besides', 'but', 'by', 'cause', 
    'caused', 'causes', 'causing', 'condition', 'conditional upon', 
    'conditions', 'consequence', 'consequences', 'consequent', 'consequently', 
    'contrasted with', 'correspondingly', 'desire', 'desired', 'desires', 
    'desiring', 'despite the fact that', 'due to', 'enable', 'enabled', 
    'enables', 'enabling', 'except that', 'finally', 'first', 'follow that',
    'follow the', 'follow this', 'followed that', 'followed the', 
    'followed this', 'following that', 'follows the', 'follows this', 
    'fortunately', 'from now on', 'further', 'furthermore', 'goal', 'goals',
    'hence', 'however', 'if', 'immediately', 'in actual fact', 'in addition',
    'in any case', 'in any event', 'in case', 'in conclusion', 'in contrast',
    'in fact', 'in order', 'in other words', 'in short', 'in sum', 
    'in the end', 'in the meantime', 'incidentally', 'instead', 
    'it followed that', 'it follows', 'it follows that', 'likewise', 'made',
    'make', 'makes', 'making', 'meanwhile', 'moreover', 'nevertheless', 'next',
    'nonetheless', 'nor', 'notwithstanding that', 'now that', 
    'on another occasion', 'on one hand', 'on the contrary', 'on the one hand',
    'on the other hand', 'once more', 'or', 'otherwise', 'presently', 
    'previously', 'provided that', 'purpose of which', 'pursuant to', 'rather',
    'secondly', 'similarly', 'simultaneously', 'since', 'so', 'summarizing', 
    'summing up', 'that is', 'the last time', 'the previous moment', 'then', 
    'therefore', 'thereupon', 'this time', 'though', 'throughout', 'thus', 
    'to conclude', 'to return to', 'to sum up', 'to summarize', 
    'to take an example', 'to that end', 'to these ends', 'to this end', 
    'to those ends', 'too', 'unless', 'until', 'up till that time', 
    'up to now', 'well at any rate', 'whenever', 'whereas', 'while', 'yet']  

    # Function that splits text into tokens.
    tokens = nltk.word_tokenize(text.lower())

    # Check how many connectives are in the text by checking if each token is 
    # in connectivesCheck. 
    # There are also connectives consisting of multiple words, this is at most
    # 4 words.
    numberOfConnectives = 0
    for i in tokens:
        if i in connectivesCheck:
            numberOfConnectives += 1
    # Check for connectives consisting of 2 tokens/words.
    if len(tokens) > 1:
        for i in range(len(tokens)-1):            
            if tokens[i] + ' ' + tokens[i+1] in connectivesCheck:
                numberOfConnectives += 1
    # Check for connectives consisting of 3 tokens/words.
    if len(tokens) > 2:
        for i in range(len(tokens)-2):            
            if tokens[i] + ' ' + tokens[i+1] + ' ' + tokens[i+2] in connectivesCheck:
                numberOfConnectives += 1
    # Check for connectives consisting of 4 tokens/words.
    if len(tokens) > 3:
        for i in range(len(tokens)-3):            
            if tokens[i] + ' ' + tokens[i+1] + ' ' + tokens[i+2] + ' ' + tokens[i+3] in connectivesCheck:                
                numberOfConnectives += 1

    # Only keep words in token list.
    # (get rid of things like dots or comma's)
    for i in tokens:
        if i.isalpha() == False:
            tokens.pop(tokens.index(i))

    # Calculate index score by dividing the number of connectives in the text
    # by the total number of tokens (words) in the text.
    indexScore = numberOfConnectives/len(tokens)

    # Calculate the connectives score by putting the indexScore into the 
    # following 2nd order polynomial: y = -3.5 + 300*x - 1666.667*x^2, where 
    # y is the connectives score and x is the indexScore. 
    # We take the max of this result and 0, since we grade in the range [0,10].
    # Then we round the result to 2 decimals.
    connectivesScore = round(max(-3.5 + 300*indexScore - 1666.667*indexScore**\
        2, 0), 2)
    
    # Return the calculated connectives score and indexScore.
    return connectivesScore, indexScore