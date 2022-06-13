import re
from nltk.tokenize import word_tokenize
from flask import current_app
import os
from app.feedback.retrieveText.convertPdfToText import getPDFText
from app.feedback.pageDownload import scrapePage, downloadDoi
from math import ceil

def sourceIntegration(text, references, englishStopwords, userId):
    '''
        Calculate the score for the source-integration and content, by retrieving the sources, looking 
        if there are enough sources and looking if words in the text are also used in the sources. 
        Attributes: 
            links: Links from the sources which are not papers, so no sources containing doi.org. 
            links_doi: Links from the sources which are papers, so have links containing doi.org.
            numSources: Total number of sources in references.
            numWordsText: Total number of words in the text without stopWords.
            numSourcesUsed: Number of sources that are used by the application, so of which the words could be retrieved.
            numParagraphs: The number of paragraphs in the text.
        Arguments: 
            text: The text we calculate the source-integration and content for.
            references: References ofr this text, for which we calculate the source integration and content.
            englishStopwords: Corpus of all the english stopwords, as taken from the nltk library.
            userId: userId of the current user, we calculate this score for.
        Returns:
            score: Score of the source-integration and content for this text.
            explanation: explanation of the source-integration and content corresponding to this score.
    '''
    # Retrieve the links, links_doi and number of sources from the references string:
    links, links_doi, numSources = getUrlsSources(references)
    # Retrieve the words in a set that occur in at least one reference and are not in englishStopwords, 
    # and the number of source which could be looked at:
    wordsReferences, numSourcesUsed = getWordsSources(links, links_doi, englishStopwords, userId)
    # Get the dictionary of the words, which are not in englishStopwords and the number of words in the text:
    wordsFromText, numWordsText = wordsText(text, englishStopwords)
    # Count the number of paragraphs in the text:
    numParagraphs = countParagraphs(text)
    # If the words of at least one source could be retrieved:
    if numSourcesUsed > 0: 
        # Calculate the score and get the explanation using the calcScoreAndExplanationSourcesDownloaded method:
        score, explanation = calcScoreAndExplanationSourcesDownloaded(wordsFromText, wordsReferences, numWordsText, numSources, numParagraphs)
    else: 
        # Else, calculate the score and get the explanation using the calcScoreAndExplanationSourcesNotDownloaded method:
        score, explanation = calcScoreAndExplanationSourcesNotDownloaded(numSources, numParagraphs)
    return score, explanation

    
def calcScoreAndExplanationSourcesDownloaded(wordsFromText, wordsReferences, numWordsText, numSources, numParagraphs):
    '''
        Calculate the score and create the explanation if the text from the sources could be downloaded.
        For the score, if you use 1 source per 3 paragraphs you only get a score of 1, if this is 1 source per 4 paragraphs this is 0.5
        and if you use 1 source per 5 paragraphs this is a 0. If you use at least 1 source per 3 paragraphs, you need a percentage 
        of 25% of words in the text also occurring in the sources for a 10, which goes down to the 1 if no words in the text are also 
        contained in the sources. 
        Arguments:
            wordsFromText: Dictionary of words without stopWords occurring in the text.
            wordsReferences: Set of words without stopwords occurring in the references.
            numWordsText: Number of words in the text.
            numSources: Number of sources for this text.
            numParagraphs: Number of paragraphs in this text.
        Returns: 
            score: Score for this number of sources, the number of paragraphs and the percentage of words also occurring in the sources.
            explanation: General explanation for this score as string.
    '''
    # If there are not at least 1 source per 3 paragraphs, set the score according to the number of paragraphs per source:
    if ceil(numParagraphs / numSources)  > 3:
        if ceil(numParagraphs / numSources) > 5:
            score = 0
        elif ceil(numParagraphs / numSources)  > 4:
            score = 0.5
        elif ceil(numParagraphs / numSources)  > 3:
            score = 1
        # Add the explanation and return:
        explanation = (f'Your score for source integration and content is {score}. You only used {numSources} sources ' + 
        f'in {numParagraphs} paragraphs of text. Try adding more sources.' )
    else:
        # If there is at least one source per 3 paragraphs, calculate the percentage of words from the text also in the references:
        percentageWordsInText = calcPercentageWordsUsed(wordsFromText, wordsReferences, numWordsText)
        # Calculate the score, where the score can be at most 10 and a 25% occurrence in the sources is a 10:
        score = min(1 + round(percentageWordsInText*36, 2), 10)
        # If you have a 10 indicate that you have a perfect score, otherwise say that you can improve the score:
        if score == 10:
            stringPart = 'This gives a perfect score'
        else:
            stringPart = 'For a higher score'
        # Add the explanation:
        explanation = (f'Your score for source integration and content is {score}. You used {numSources} sources ' + 
        f'in {numParagraphs} paragraphs of text. You used {round(percentageWordsInText *100, 2)}% of the words used in the sources in your text. ' +  
        f'{stringPart}, you could try adding more words used in the sources in your text.')
    return score, explanation

def calcScoreAndExplanationSourcesNotDownloaded(numSources, numParagraphs):
    '''
        Calculate the score and create the explanation if no sources could be downloaded. 
        This score is based on the number of sources per paragraph, where less than 1 source per 5 paragraphs is a 0
        and 1 score per paragraph is a 10, and everything inbetween. So the score increments by 2 for paragraph 
        per source that is added. 
        Arguments: 
            numSources: Total number of sources in this text.
            numParagraphs: Total number of paragraphs in this text.
        Returns: 
            score: Score for this number of sources and number of paragraphs.
            explanation: General explanation for this score as string.
    '''
    # Calculate the score:
    if ceil(numParagraphs / numSources)  > 5:
        score = 0
    elif ceil(numParagraphs / numSources)  > 4:
        score = 2
    elif ceil(numParagraphs / numSources)  > 3:
        score = 4
    elif ceil(numParagraphs / numSources)  > 2:
        score = 6
    elif ceil(numParagraphs / numSources)  > 1:
        score = 8
    else:
        score = 10
    # Create the explanation and return:
    explanation = (f'Your score for source integration and content is {score}. You only used {numSources} sources ' + 
    f'in {numParagraphs} paragraphs of text. Try adding more sources. Writing Dashboard Could not check if text from the sources ' + 
    f'are actually used in the text.' )
    return score, explanation


def calcPercentageWordsUsed(wordsFromText, wordsReferences, numWordsText):
    '''
        Calculate the percentage of words from the text also in the references. That is, 
        calculate which percentage of words in wordsFromText is also in wordsReferences.
        Attributes:
            word: Single word from wordsFromText. 
        Arguments:
            wordsFromText: All words in the dictionary from the text.
            wordsReferences: Set with all words from the references. 
            numWordsText: The amount of words in the original text.
        Returns:
            percentage: Percentage of words in wordsFromText also in numWordsText.
    '''
    percentage = 0
    # For each word in wordsFromText:
    for word in wordsFromText:
        # If this word is also in wordsReferences:
        if word in wordsReferences:
            # Add the amount of time this word occurs divided by the total number of words to the percentage:
            percentage += wordsFromText[word] / numWordsText
    return percentage

def getWordsSources(links, links_doi, englishStopwords, userId):
    '''
        Get the words from the sources as given in links and links_doi by applying the 
        wordsSource, scrapePage and textDoi methods.
        Attributes:
            link: single link from the links list.
            link_doi: single link from the links_doi list.
            text: text as retrieved from either a single link or single link_doi.
        Arguments: 
            englishStopwords: Corpus of all the english stopwords, as taken from the nltk library.
        Returns:
            wordReferences: set of the words without stopwords of all sources in links and links_doi.
            count: Number of sources actually retrieved the words from.
    '''
    wordsReferences = set()
    count = 0
    # For each link in links:
    for link in links:
        # Scrape the text of the page from this link:
        text = scrapePage(link)
        # Add the words from this text if they are not in englishStopwords and not in the set already and increment the count:
        wordsReferences = wordsSource(text, wordsReferences, englishStopwords)
        count += 1
    # For each link_doi in links_doi:
    for link_doi in links_doi:
        # Get the text of the pdf from this link via the textDoi method:
        text = textDoi(link_doi, userId)
        # If there is an actual test returned increment the count and add the words not in the set already and not in englishStopwords:
        if text != '':
            count += 1
            wordsReferences = wordsSource(text, wordsReferences, englishStopwords)
    
    return wordsReferences, count

def wordsSource(text, wordsWoStopwords, englishStopwords):
    '''
        Gets the words without stopwords as in the nltk stopwords english library 
        from a single source, as given in text and add this to the wordsWoStopwords set.
        Attributes: 
            t: Single token inside the for-loop.
            tokens: Tokens of the words inside the text, that is each word individually. 
        Arguments:
            text: Text we want to find the words with occurrences from.
            englishStopwords: Corpus of all the english stopwords, as taken from the nltk library.
            wordsWoStopwords: Set with the words without stopwords in the texts that have already been processed.
        Returns:
            wordsWoStopwords: Set with the words without stopwords added to the wordsWoStopwords set, if not there yet.
    '''
    # Remove punctuation from the text:
    text = re.sub(r'[^\w\s]', '', text)

    # Retrieve each word separately:
    tokens = word_tokenize(text.lower())
    # For each word, if it is not in englishStopwords:
    for t in tokens:
        if t not in englishStopwords:
            # Add this word to the text:
            wordsWoStopwords.add(t)
    return wordsWoStopwords

def wordsText(text, englishStopwords):
    '''
        Get the words inside the text (without English stopwords as in the nltk library stopwords corpus)
        inside a dictionary with the number of occurrences of each words. Counts the total number of words 
        without stopwords in the text. 
        Attributes:
            t: Single token inside the for-loop.
            tokens: Tokens of the words inside the text, that is each word individually. 
        Arguments:
            text: Text we want to find the words with occurrences from.
            englishStopwords: Corpus of all the english stopwords, as taken from the nltk library.
        Returns:
            wordsWoStopwords: Dictionary with the words without stopwords in the text as key and their occurrences as value.
            count: The number of words without stopwords inside the text.
    '''
    # Variable for the wordcount:
    count = 0
    # Dictionary for the words in the text:
    wordsWoStopwords = dict()
    # Remove punctuation from the text:
    text = re.sub(r'[^\w\s]', '', text)
    
    # Retrieve each word separately:
    tokens = word_tokenize(text.lower())
    # For each word, if it is not in englishStopwords:
    for t in tokens:
        if t not in englishStopwords:
            # Count this word:
            count += 1
            # If the word is not in the dictionary yet, set the count to 1, else increment the count by 1:
            if t not in wordsWoStopwords.keys():
                wordsWoStopwords[t] = 1
            else:
                wordsWoStopwords[t] += 1
    # Return the words and count:
    return wordsWoStopwords, count

def countParagraphs(text):
    '''
        Function to count the number of paragraphs in the text.
        Arguments:
            text: Text to count the number of paragraphs from.
        Returns:
            The number of paragraphs in the text, where each paragraph is divided by 
                2 newline characters.
    '''
    return text.count('\n\n') + 1

def textDoi(doi, userId):
    '''
        Method to extract the text from urls containing doi.org, which are generally papers. 
        Used the downloadDoi and getPDFText functions.
        Attributes:
            basePath: Path consisting of joining the UPLOAD_FOLDER in the flask config and the current userId.
            tempPath: Path consisting of joining the basePath and 'temp', to create a temp folder.
            filePath: Path consisting of joining this tempPath and 'temp.pdf' to create a temporary filepath.
        Arguments:
            doi: doi link of the document we want to get the text from.
        Returns:
            text: Text from the document the link in the doi variable points to, empty string if no document could be found.
    '''
    text = ''
    # Get (and join) the paths:
    basePath = os.path.join(current_app.config['UPLOAD_FOLDER'], str(userId))
    tempPath = os.path.join(basePath, 'temp')
    filePath = os.path.join(tempPath, 'temp.pdf')
    # If this folder does not yet exist, create it:
    if not os.path.isdir(tempPath):
        os.makedirs(tempPath)
    # Try to download the file via the downloadDoi method, if this is possible extract the text using the getPDFText method. 
    if downloadDoi(doi, filePath):
        text = getPDFText(filePath)
    # Delete the file if it exists and delete the folder(s), so temp folder and user folder if it is empty:
    if os.path.exists(filePath):
        os.remove(filePath)
        if not os.listdir(tempPath):
            os.rmdir(tempPath)
            if not os.listdir(basePath):
                os.rmdir(basePath)
    # Return the text:
    return text

def getUrlsSources(sourceString):
    '''
        Gets the urls of sources from a string with sources and returns the number of sources.
        Attributes:
            sources: All separate sources in an array, so sourceString split on the newline character.
            source: Individual element of the sources array.
            url: Search for https:// inside the string, so a re.match element of each link.
            url1: Retrieved the text of each url match element if there is a string in the source.
            url_doi: Search for the doi.org text inside a link, to see if we are working with a doi link.
        Arguments: 
            sourceString: String with all sources, where each source is split by a newline character.
        Returns:
            links: array with the links which do not contain the text "doi.org".
            links_doi: array with the links which do contain the text "doi.org" and therefore should be papers.
            numSources: the number of sources.
    '''
    # Get all the individual sources:
    sources = sourceString.split('\n\n')
    # Create arrays to store the results:
    links = []
    links_doi =[]
    # For each source:
    for source in sources:
        # Find the url:
        url = re.search('https?://.*', source)
        # If there is an url, look if this contains doi.org, if yes add to links_doi, else add to links:
        if url != None:
            url1 = url.group(0)
            url1 = re.sub(r'^\s+|\s+$', '', url1)
            url_doi = re.search('.*doi.org.*', url1)
            if url_doi != None:
                links_doi.append(url_doi.group(0))
            else: 
                links.append(url1)
    # Find the number of sources and return everything:
    numSources = len(sources)
    return links, links_doi, numSources