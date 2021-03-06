from app.feedback.retrieveText.pageDownload import scrapePage, downloadDoi
import os
from flask import current_app

def testScrapePage(testClient):
    '''
        Test the scrapePage method on a url.
        Attributes:
            url: The url we scrape the page from.
            isSuccesful: Boolean to indicate if the scrapepage was succesful.
            text: The text from the page we scraped.
            textShould: what the text that is returned should be.
        Arguments:
            testClient:  The test client we test this for. 
    '''
    del testClient
    url = 'https://www2.latech.edu/~acm/helloworld/python.html'
    isSuccessful, text = scrapePage(url)
    textShould = ('Hello World in Python Python print "Hello world!"\n while True: \xa0 \n\xa0print "Hello world!" submitted by: ')
    assert isSuccessful == True
    assert text == textShould

def testScrapePageFailed(testClient):
    '''
        Test the scrapePage method if we cannot scrape an url.
        Attributes:
            url: The url we scrape the page from.
            isSuccessful: Boolean to indicate if the scrapepage method was successful.
            text: The text from the page we scraped.
            textShould: what the text that is returned should be.
        Arguments:
            testClient:  The test client we test this for. 
    '''
    del testClient
    url = 'http://www.xxxxxx'
    isSuccessful, text = scrapePage(url)
    assert isSuccessful == False
    assert"HTTPConnectionPool(host='www.xxxxxx', port=80): Max retries exceeded with url:" in text

def testDownloadDoiSucces(testClient):
    '''
        Test the downloadDoi method for a link containing a paper.
        Attributes:
            filepath: Temporary filepath.
            url: Url pointing to a doi of a paper.
            isDownloaded: Return of the downloadDOi function.
        Arguments:
            testClient:  The test client we test this for. 
    '''
    del testClient
    filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], 'temp.pdf')
    assert not os.path.isfile(filepath)
    url = 'https://doi.org/10.1038/nphys1170'
    isDownloaded = downloadDoi(url, filepath)
    assert os.path.isfile(filepath)
    assert isDownloaded
    # Remove the file:
    os.remove(filepath)

def testDownloadDoiFail(testClient):
    '''
        Test the downloadDoi method for a link containing a paper.
        Attributes:
            filepath: Temporary filepath.
            url: Url pointing to a doi of a paper.
            isDownloaded: Return of the downloadDOi function.
        Arguments:
            testClient:  The test client we test this for. 
    '''
    del testClient
    filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], 'temp.pdf')
    assert not os.path.isfile(filepath)
    url = 'https://doi.org/10.1038/nphys11'
    isDownloaded = downloadDoi(url, filepath)
    assert not os.path.isfile(filepath)
    assert not isDownloaded