from app.models import Files, Scores

def testFiles(testClient, initDatabase):
    '''
        Test if we get the correct display if we run Files.query.all(), so the representation of '<File <filename>>'. 
        Attributes: 
            files: all files of the type Files in the database.
        Arguments:
            testClient:  The test client we test this for.
            initDatabase: the database instance we test this for. 
    '''
    del testClient, initDatabase
    files = Files.query.all()
    assert str(files[0]) == '<Files URD_Group3_vers03_Rc.pdf>'
    assert str(files[1]) == '<Files SEP.pdf>'

def testScore():
    '''
        Test if the score model works properly
        Attributes: 
            score: score model
    '''
    score = Scores(
        fileId = 12,
        scoreStyle = 0.01,
        scoreCohesion = 2,
        scoreStructure = 3,
        scoreIntegration = 10.0,
    )
    assert score.fileId == 12
    assert score.scoreStyle == 0.01
    assert score.scoreCohesion == 2
    assert score.scoreStructure == 3
    assert score.scoreIntegration == 10.0