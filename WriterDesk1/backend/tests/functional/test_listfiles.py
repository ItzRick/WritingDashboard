from datetime import datetime
from app.models import Files
from app import db
import json
import urllib

# Generate request to test routes.fileRetrieve()
def listFiles(testClient, initDatabase, sortingAttribute, firstFilename):
    file1 = Files(path='C:/normal/path/A-File.pdf', filename='A-File.pdf', date=datetime(1999, 1, 1), userId = 0, courseCode = 'ABCDE')
    db.session.add(file1)
    file2 = Files(path='C:/normal/path/Z-File.pdf', filename='Z-File.pdf', date=datetime(2022, 1, 1), userId = 0, courseCode = 'ZYXWV')
    db.session.add(file2)
    db.session.commit()
    data = {'sortingAttribute': sortingAttribute}
    response = testClient.get('/fileapi/fileretrieve?' + urllib.parse.urlencode(data))
    assert response.status_code == 200
    files = json.loads(response.data)
    assert len(files) == 2
    assert files[0]['filename'] == firstFilename
    assert files[0]['userId'] == 0

# Call listFiles() with different sorting attributes
def testListFilesFilenameAsc(testClient, initDatabase):
    listFiles(testClient, initDatabase, 'filename.asc', 'A-File.pdf')

def testListFilesFilenameDesc(testClient, initDatabase):
    listFiles(testClient, initDatabase, 'filename.desc', 'Z-File.pdf')

def testListFilesCourseAsc(testClient, initDatabase):
    listFiles(testClient, initDatabase, 'course.asc', 'A-File.pdf')

def testListFilesCourseDesc(testClient, initDatabase):
    listFiles(testClient, initDatabase, 'course.desc', 'Z-File.pdf')

def testListFilesDateAsc(testClient, initDatabase):
    listFiles(testClient, initDatabase, 'date.asc', 'A-File.pdf')

def testListFilesDateDesc(testClient, initDatabase):
    listFiles(testClient, initDatabase, 'date.desc', 'Z-File.pdf')

#def testListFilesNoUser(testClient, initDatabase):
#    data = {'sortingAttribute': sortingAttribute}
#    response = testClient.get('/fileapi/fileretrieve?' + urllib.parse.urlencode(data))
#    assert response.status_code == 400