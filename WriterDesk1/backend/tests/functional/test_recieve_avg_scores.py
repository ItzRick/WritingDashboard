from app import db
from app.models import Scores, Files
from datetime import datetime
import json

def generalGetAvgScore(testClient, userId, avgscoreStyle, avgscoreCohesion, avgscoreStructure, avgscoreIntegration):
    data = {
        'userId':userId,
    }

    # Retrieve the average scores from the specified user
    response = testClient.get('/scoreapi/getAvgScores', query_string=data)

    # Check if we get the correct status_code
    assert response.status_code == 200

    # Check response
    dataResponse = json.loads(response.data)
    assert float(dataResponse['scoreStyle']) == avgscoreStyle
    assert float(dataResponse['scoreCohesion']) == avgscoreCohesion
    assert float(dataResponse['scoreStructure']) == avgscoreStructure
    assert float(dataResponse['scoreIntegration']) == avgscoreIntegration

def testAverageScores(testClient, initDatabaseEmpty):
    del initDatabaseEmpty

    # we add files and scores to the database
    try:
        db.session.commit()
    except:
        db.session.rollback()
    try: 
        file = Files(path='', filename='', date=datetime(2018, 1, 1), userId = 200, courseCode = '', id=1)
        db.session.add(file)
        file2 = Files(path='', filename='', date=datetime(2019, 1, 1), userId = 200, courseCode = '', id=2)
        db.session.add(file2)
        file3 = Files(path='', filename='', date=datetime(2020, 1, 1), userId = 200, courseCode = '', id=3)
        db.session.add(file3)
        file4 = Files(path='', filename='', date=datetime(2021, 1, 1), userId = 200, courseCode = '', id=4)
        db.session.add(file4)
        file5 = Files(path='', filename='', date=datetime(2022, 1, 1), userId = 200, courseCode = '', id=5)
        db.session.add(file5)
        file6 = Files(path='', filename='', date=datetime(2000, 1, 1), userId = 200, courseCode = '', id=6)
        db.session.add(file6)
        db.session.commit()
    except:
        db.session.rollback()
    try: 
        score = Scores(fileId= 1, scoreStyle= 1, scoreCohesion= 5, scoreStructure= 2, scoreIntegration=7)
        db.session.add(score)
        score2 = Scores(fileId= 2, scoreStyle= 1, scoreCohesion= 2, scoreStructure= 1, scoreIntegration=6)
        db.session.add(score2)
        score3 = Scores(fileId= 3, scoreStyle= 5, scoreCohesion= 3, scoreStructure= 3, scoreIntegration=2)
        db.session.add(score3)
        score4 = Scores(fileId= 4, scoreStyle= 5, scoreCohesion= 5, scoreStructure= 1, scoreIntegration=7)
        db.session.add(score4)
        score5 = Scores(fileId= 5, scoreStyle= 3, scoreCohesion= 5, scoreStructure= 3, scoreIntegration=3)
        db.session.add(score5)
        score6 = Scores(fileId= 6, scoreStyle= 9, scoreCohesion= 9, scoreStructure= 9, scoreIntegration=9)
        db.session.add(score6)
        db.session.commit()
    except:
        db.session.rollback()
    
    userId = 200
    avgscoreStyle = 3
    avgscoreCohesion = 4
    avgscoreStructure = 2
    avgscoreIntegration = 5

    generalGetAvgScore(testClient, userId, avgscoreStyle, avgscoreCohesion, avgscoreStructure, avgscoreIntegration)