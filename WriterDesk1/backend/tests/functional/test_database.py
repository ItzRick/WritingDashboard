from app.models import Files
from app.database import uploadToDatabase, getFilesByUser
from app import db
from datetime import datetime

def testValidFile(testClient, initDatabase):
    files = Files.query.all()
    file = files[0]
    assert file.filename=='URD_Group3_vers03_Rc.pdf'
    assert file.path=='C:/Users/20192435/Downloads/SEP2021/WriterDesk1/backend/saved_documents/URD_Group3_vers03_Rc.pdf'
    assert file.date == datetime(2019, 2, 12)
    assert file.userId == 123
    assert file.courseCode == "2IPE0"
    file = files[1]
    assert file.filename=='SEP.pdf'
    assert file.path=='C:/Users/20192435/Downloads/SEP2021/WriterDesk1/backend/saved_documents/SEP.pdf'
    assert file.date == datetime(2020, 10, 2)
    assert file.userId == 567
    assert file.courseCode == "3NAB0"

def testUploadToDatabase(testClient, initDatabase):
    # db.create_all()
    file = Files(path='C:/Users/20192435/Downloads/SEP2021/WriterDesk1/backend/saved_documents/ScrumAndXpFromTheTrenchesonline07-31.pdf', 
    filename='ScrumAndXpFromTheTrenchesonline07-31.pdf', date=datetime(2019, 2, 12), userId = 123, courseCode = '2IPE0')
    db.session.add(file)
    db.session.commit()
    file = Files.query.filter_by(filename='ScrumAndXpFromTheTrenchesonline07-31.pdf').first()
    assert file.filename =='ScrumAndXpFromTheTrenchesonline07-31.pdf'
    assert file.path =='C:/Users/20192435/Downloads/SEP2021/WriterDesk1/backend/saved_documents/ScrumAndXpFromTheTrenchesonline07-31.pdf'
    assert file.date == datetime(2019, 2, 12)
    assert file.userId == 123
    assert file.courseCode == "2IPE0"
    file = Files.query.all()[2]
    assert file.filename=='ScrumAndXpFromTheTrenchesonline07-31.pdf'
    assert file.path=='C:/Users/20192435/Downloads/SEP2021/WriterDesk1/backend/saved_documents/ScrumAndXpFromTheTrenchesonline07-31.pdf'
    assert file.date == datetime(2019, 2, 12)
    assert file.userId == 123
    assert file.courseCode == "2IPE0"

def testGetFilesByUser(testClient, initDatabase):
    db.session.commit()
    file = Files(path='C:/normal/path/File-1.pdf', filename='File-1.pdf', date=datetime(2019, 2, 12), userId = 200, courseCode = '2IPE0')
    db.session.add(file)
    file2 = Files(path='C:/normal/path/File-2.pdf', filename='File-2.pdf', date=datetime(2019, 2, 12), userId = 201, courseCode = '2IPE0')
    db.session.add(file2)
    file3 = Files(path='C:/normal/path/File-3.pdf', filename='File-3.pdf', date=datetime(1999, 2, 12), userId = 200, courseCode = '2IPE0')
    db.session.add(file3)
    db.session.commit()
    
    files = getFilesByUser(200, 'date.asc')
    assert len(files) == 2
    assert files[0].get('filename') == 'File-3.pdf'
    assert files[0].get('userId') == 200

def testCreateDatabase(testClient):
    db.create_all()

def testFiles(testClient, initDatabase):
    files = Files.query.all()
    assert str(files[0]) == '<File URD_Group3_vers03_Rc.pdf>'
    assert str(files[1]) == '<File SEP.pdf>'