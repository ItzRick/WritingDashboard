from bs4 import BeautifulSoup
import requests


def downloadDoi(url, filePath):
    '''
        Download a pdf file, corresponding to the paper from the doi link to filePath using sci-hub.
        Attributes:
            sci_hub_url: Base url of hte sci-hub site.
            headers: Headers for the request.
            r: Request of this sci-hub site to retrieve the paper link from and the pdf file. 
            soup: BeautifulSoup object of the sci-hub page.
            embed: Find the element with the id of pdf from the page.
            link: Link if there is a pdf on the page.
            fd: File to write the pdf file to.
            chunk: Chunk of the pdf file to be saved to the disk.
        Arguments: 
            url: Url of the doi of which we need to download the paper.
            filePath: Path we need to save the pdf to.
        Returns:
            True if a pdf file has been downloaded and saved to filePath, else False.
    '''
    sci_hub_url = 'https://sci-hub.se/'
    # Use headers, so act like we are a firefox browser:
    headers = {
        'User-Agent': 'Mozilla/5.0',
    }
    # Get the url, which consists of the sci_hub_url and then the doi url:
    url = sci_hub_url + url
    # Fetch this page and create a BeautifulSoup object:
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.content, 'html.parser')
    # Get the pdf embed elementL
    embed = soup.find(id='pdf')
    if embed:
        # If it exists, get the link:
        link = embed.get('src')
        if link:
            # If it exists, add https: in front:
            link = 'https:' + link
            # Retrieve this pdf file:
            r = requests.get(link, headers=headers)
            if r.status_code == 200:
                # If we have retrieved a pdf, save this to the filePath location:
                with open(filePath, 'wb') as fd:
                    for chunk in r.iter_content(chunk_size=128):
                        fd.write(chunk)
                # Return true, since we have written a file to the correct location:
                return True
    # Return false if we have not saved a file to the correct location:
    return False

def scrapePage(url):
    '''
        Scrape the page corresponding to the url and return the text.
        Attributes:
            headers: Headers for the request.
            r: Request of this sci-hub site to retrieve the paper link from and the pdf file. 
            soup: BeautifulSoup object of the sci-hub page.
            text: Html text form this webpage.
            blacklist: Elements from the html page we do not want in the output.
            t: Elements from the html text we might remove or we add to the output.
        Arguments:
            url: Url we scrape the page from. 
        Returns:
            output: Output of the text on the site corresponding to url. 
    '''
    # Create the headers, which correspond to a firefox browser:
    headers = {
        'User-Agent': 'Mozilla/5.0',
    }
    # Retrieve the page corresponding to url:
    r = requests.get(url, headers=headers)
    # Create the BeautifulSoup object:
    soup = BeautifulSoup(r.content, 'html.parser')
    # Retrieve all text from this object:
    text = soup.find_all(text=True)
    # Create a output element:
    output = ''
    # Blacklist of HTML elements we do not want the text from:
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

    # For all object in the HTML source:
    for t in text:
        # If this element is not in the blacklist, add the text from this element to output:
        if t.parent.name not in blacklist:
            output += '{} '.format(t)

    return output