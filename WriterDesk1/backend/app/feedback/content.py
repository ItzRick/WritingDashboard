import re
import nltk
# nltk.download('stopwords')
# nltk.download('punkt')
# english_stopwords = stopwords.words('english')
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from bs4 import BeautifulSoup
import requests
from flask import current_app
import os
from app.feedback.convertPdfToText import getPDFText



def sourceIntegration(text, references, englishStopwords, userId):
    
    links, links_doi, numSources = getUrlsSources(references)
    wordsReferences, numSourcesUsed = getWordsSources(links, links_doi, englishStopwords, userId)
    wordsFromText, numWordsText = wordsText(text, englishStopwords)
    numParagraphs = countParagraphs(text)
    if numSourcesUsed > 0: 
        score, explanation = calcScoreAndExplanationSourcesDownloaded(wordsReferences, wordsFromText, numWordsText, numSources, numParagraphs)
    else: 
        score, explanation = calcScoreAndExplanationSourcesNotDownloaded(numSources, numParagraphs)
    return score, explanation

    
def calcScoreAndExplanationSourcesDownloaded(wordsReferences, wordsFromText, numWordsText, numSources, numParagraphs):
    if numParagraphs // numSources  > 3:
        score = 1
        explanation = (f'Your score for source integration and content is {score}. You only used {numSources} ' + 
        f'in {numParagraphs} of text. Try adding more sources.' )
        return score, explanation
    elif numParagraphs // numSources  > 5:
        score = 0
        explanation = (f'Your score for source integration and content is {score}. You only used {numSources} ' + 
        f'in {numParagraphs} of text. Try adding more sources.' )
        return score, explanation
    else:
        percentageWordsInText = calcPercentageUsed(wordsFromText, wordsReferences, numWordsText)
        score = max(1 + round(percentageWordsInText*9, 2), 10)
        if score == 10:
            explanation = (f'Your score for source integration and content is {score}. You used {numSources} sources ' + 
            f'in {numParagraphs} of text. You used {percentageWordsInText *100}% of the words used in the sources in your text. ' +  
            f'This gives a perfect score, you could try adding more words used in the sources in your text.')
        else:
            explanation = (f'Your score for source integration and content is {score}. You used {numSources} sources ' + 
            f'in {numParagraphs} of text. You used {percentageWordsInText *100}% of the words used in the sources in your text. ' +  
            f'For a higher score, you could try adding more words used in the sources in your text.')
        return score, explanation

def calcScoreAndExplanationSourcesNotDownloaded(numSources, numParagraphs):
    if numParagraphs // numSources  > 5:
        score = 0
        explanation = (f'Your score for source integration and content is {score}. You only used {numSources} ' + 
        f'in {numParagraphs} of text. Try adding more sources.' )
        return score, explanation
    elif numParagraphs // numSources  > 4:
        score = 2
        explanation = (f'Your score for source integration and content is {score}. You only used {numSources} ' + 
        f'in {numParagraphs} of text. Try adding more sources. Writing Dashboard Could not check if text from the sources ' + 
        f'are actually used in the text.' )
        return score, explanation
    elif numParagraphs // numSources  > 3:
        score = 4
        explanation = (f'Your score for source integration and content is {score}. You only used {numSources} ' + 
        f'in {numParagraphs} of text. Try adding more sources. Writing Dashboard Could not check if text from the sources ' + 
        f'are actually used in the text.' )
        return score, explanation
    elif numParagraphs // numSources  > 2:
        score = 6
        explanation = (f'Your score for source integration and content is {score}. You only used {numSources} ' + 
        f'in {numParagraphs} of text. Try adding more sources. Writing Dashboard Could not check if text from the sources ' + 
        f'are actually used in the text.' )
        return score, explanation
    elif numParagraphs // numSources  > 1:
        score = 8
        explanation = (f'Your score for source integration and content is {score}. You only used {numSources} ' + 
        f'in {numParagraphs} of text. Try adding more sources. Writing Dashboard Could not check if text from the sources ' + 
        f'are actually used in the text.' )
        return score, explanation
    else:
        score = 10
        explanation = (f'Your score for source integration and content is {score}. You only used {numSources} ' + 
        f'in {numParagraphs} of text. Try adding more sources. Writing Dashboard Could not check if text from the sources ' + 
        f'are actually used in the text.' )
        return score, explanation 


def calcPercentageUsed(wordsFromText, wordsReferences, numWordsText):
    percentage = 0
    for word in wordsFromText:
        if word in wordsReferences:
            percentage += wordsFromText[word] / numWordsText
    return percentage



def getWordsSources(links, links_doi, englishStopwords, userId):
    wordsReferences = set()
    count = 0
    for link in links:
        text = scrapePage(link)
        wordsReferences = wordsSource(text, wordsReferences, englishStopwords)
        count += 1
    for link_doi in links_doi:
        text = textDoi(link_doi, userId)
        if text != '':
            count += 1
            wordsReferences = wordsSource(text, wordsReferences, englishStopwords)
    
    return wordsReferences, count

def wordsSource(text, wordsWoStopwords, englishStopwords):
    text = re.sub('[,\.!?]', '', text)
    tokens = word_tokenize(text.lower())
    for t in tokens:
        if t not in englishStopwords:
            wordsWoStopwords.add(t)
    return wordsWoStopwords

def wordsText(text, englishStopwords):
    '''
        Get the words inside the text (without English stopwords as in the nltk library stopwords corpus)
        inside a dictionary with the number of occurrences of each words. Counts the total number of words 
        without stopwords in the text. 
        Attributes:
            tokens: Tokens of the words inside the text, that is each word individually. 
        Arguments:
            text: Text we want to find the words with occurences from.
            englishStopwords: Corpus of all the english stopwords, as taken from the nltk library.
        Returns:
            wordsWoStopwords: Dictionary with the words without stopwords in the text as key and their occurences as value.
            count: The number of words without stopwords inside the text.
    '''
    count = 0
    wordsWoStopwords = dict()
    text = re.sub('[,\.!?]', '', text)
    
    tokens = word_tokenize(text.lower())
    for t in tokens:
        if t not in englishStopwords:
            count += 1
            if t not in wordsWoStopwords.keys():
                wordsWoStopwords[t] = 1
            else:
                wordsWoStopwords[t] += 1

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
    basePath = os.path.join(current_app.config['UPLOAD_FOLDER'], userId)
    # TODO: Remove:
    # BASEDIR = os.path.abspath(os.path.dirname(__file__))
    # basePath = os.path.join(BASEDIR, str(userId))
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
            url_doi = re.search('.*doi.org.*', url1)
            if url_doi != None:
                links_doi.append(url_doi.group(0))
            else: 
                links.append(url1)
    # Find the number of sources and return everything:
    numSources = len(sources)
    return links, links_doi, numSources

def downloadDoi(url, filePath):
    sci_hub_url = 'https://sci-hub.se/'
    headers = {
        'User-Agent': 'Mozilla/5.0',
    }
    url = sci_hub_url + url
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.content, 'html.parser')
    embed = soup.find(id='pdf')
    if embed:
        link = embed.get('src')
        if link:
            link = 'https:' + link
            r = requests.get(link, headers=headers)
            if r.status_code == 200:
                with open(filePath, 'wb') as fd:
                    for chunk in r.iter_content(chunk_size=128):
                        fd.write(chunk)
                return True
    return False

def scrapePage(url):
    headers = {
        'User-Agent': 'Mozilla/5.0',
    }
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.content, 'html.parser')
    text = soup.find_all(text=True)
    output = ''
    blacklist = [
        '[document]',
        'noscript',
        'style'
        'header',
        'html',
        'meta',
        'head', 
        'input',
        'script',
        'link',
        'button',
        'form',
        'label',
        'amp-state', 
        'footer',
        # there may be more elements you don't want, such as "style", etc.
    ]

    for t in text:
        if t.parent.name not in blacklist:
            output += '{} '.format(t)

    return output