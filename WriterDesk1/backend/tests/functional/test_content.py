from app.feedback.content import countParagraphs

def testCountParagraphsOne(testClient):
    '''
    Test the countParagraphs method, which counts the number of paragraphs where each paragraph is divided by 
    2 newline characters. Test this for a text with 1 paragraph.
    Attributes:  
        text: The text we run the method on, containing 1 paragraph.
    Arguments:
        testClient:  The test client we test this for.
    '''
    del testClient
    text = "this is a very nice text with 1 paragraph."
    assert countParagraphs(text) == 1

def testCountParagraphsTwo(testClient):
    '''
    Test the countParagraphs method, which counts the number of paragraphs where each paragraph is divided by 
    2 newline characters. Test this for a text with 2 paragraphs.
    Attributes:  
        text: The text we run the method on, containing 2 paragraphs.
    Arguments:
        testClient:  The test client we test this for.
    '''
    del testClient
    text = ('this is a very nice text with 2 paragraphs. \n\n' + 
    'This is the second paragraph.')
    assert countParagraphs(text) == 2

def testCountParagraphsThree(testClient):
    '''
    Test the countParagraphs method, which counts the number of paragraphs where each paragraph is divided by 
    2 newline characters. Test this for a text with 3 paragraphs.
    Attributes:  
        text: The text we run the method on, containing 3 paragraphs.
    Arguments:
        testClient:  The test client we test this for.
    '''
    del testClient
    text = ('this is a very nice text with 3 paragraphs. \n\n' + 
    'This is the second paragraph. \n\n This is the third paragraph.' )
    assert countParagraphs(text) == 3