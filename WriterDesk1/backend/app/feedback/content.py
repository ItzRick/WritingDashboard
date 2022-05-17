import re
import nltk
# nltk.download('stopwords')
# nltk.download('punkt')
from nltk.corpus import stopwords
stopwords.words('english')
from nltk.tokenize import word_tokenize
from bs4 import BeautifulSoup
from requests_html import HTMLSession
import requests
from bs4 import BeautifulSoup



def sourceIntegration(text, input_words):
    counts = {}
    for word in input_words:
        counts[word] = (len(re.findall(word, text)))
    return counts


def findWords(text):
    text = re.sub('[,\.!?]', '', text)
    english_stopwords = stopwords.words('english')
    
    # text = text.lower()
    tokens = word_tokenize(text.lower())
    tokens_wo_stopwords = set()
    for t in tokens:
        if t not in english_stopwords:
            tokens_wo_stopwords.add(t)

    
    return tokens_wo_stopwords

def scrape_page(url):
    # session = HTMLSession()
    # r = session.get(url)
    # page = urlopen(url)
    # html = urlopen(url).read()
    # soup = BeautifulSoup(html, "html.parser")
    # for script in soup(["script", "style"]):
    #     script.extract()  
    # text = soup.get_text()
    # return r.text
    # link = "https://www.architecture.com/FindAnArchitect/FAAPractices.aspx?display=50"

    # url = "http://www.rockefeller.edu/research/areas/summary.php?id=1"
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
   
    # word = soup.find_all("span", {"class": "hw dhw"})
    # definition = soup.find_all("div", {"class": "pos-body"})

    # for t in word:
    #     if t.parent.name not in blacklist:
    #         output += '{} '.format(t)

    # for t in definition:
    #     if t.parent.name not in blacklist:
    #         output += '{} '.format(t)
    # html = requests.get(url).text
    # return set([t.parent.name for t in text]), output
    # return word,  definition

    return output

print(sourceIntegration("This is some nice text, is this the correct format?",findWords("This is some nice text, is this the correct format?, some more formatting is required as is the followng format.")))
# print(findWords(scrape_page("https://dictionary.cambridge.org/dictionary/english/multitasking")))
print(scrape_page("https://www.pewresearch.org/internet/2013/01/28/tracking-for-health/"))
