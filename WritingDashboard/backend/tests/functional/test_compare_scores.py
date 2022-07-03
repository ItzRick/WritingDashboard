from app.scoreapi.scores import compareScores

def testCompareScoresNull(testClient):
    '''
        Test the compareScores method where we have to get the NULL_VALUE.
        Arguments:
            testClient:  The test client we test this for.
    '''
    del testClient
    assert compareScores(1, -2, 'NULL_VALUE') == 'NULL_VALUE'

def testCompareScoresNew(testClient):
    '''
        Test the compareScores method where we have to get the new value.
        Arguments:
            testClient:  The test client we test this for.
    '''
    del testClient
    assert compareScores(1, 2, 'NULL_VALUE') == 2

def testCompareScoresOld(testClient):
    '''
        Test the compareScores method where we have to get the current value.
        Arguments:
            testClient:  The test client we test this for.
    '''
    del testClient
    assert compareScores(1, -1, 'NULL_VALUE') == 1