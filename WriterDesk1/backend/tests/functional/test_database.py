from distutils.command.upload import upload
from app.models import Files
from app.database import uploadToDatabase, removeFromDatabase
from app import db
from datetime import datetime

def testValidFile(testClient, initDatabase):
    '''
        Test if the files which are added in the database during setup are valid and all attributes
        can be correctly retrieved:
    '''
    # Retrieve the files:
    files = Files.query.all()
    # Test if all attributes for the first file are still currently there:
    file = files[0]
    assert file.filename=='URD_Group3_vers03_Rc.pdf'
    assert file.path=='C:/Users/20192435/Downloads/SEP2021/WriterDesk1/backend/saved_documents/URD_Group3_vers03_Rc.pdf'
    assert file.date == datetime(2019, 2, 12)
    assert file.userId == 123
    assert file.courseCode == "2IPE0"
    # Test if all attributes for the file are still currently there: 
    file = files[1]
    assert file.filename=='SEP.pdf'
    assert file.path=='C:/Users/20192435/Downloads/SEP2021/WriterDesk1/backend/saved_documents/SEP.pdf'
    assert file.date == datetime(2020, 10, 2)
    assert file.userId == 567
    assert file.courseCode == "3NAB0"

def testUploadToDatabase(testClient, initDatabase):
    file = Files(path='C:/Users/20192435/Downloads/SEP2021/WriterDesk1/backend/saved_documents/ScrumAndXpFromTheTrenchesonline07-31.pdf', 
    filename='ScrumAndXpFromTheTrenchesonline07-31.pdf', date=datetime(2019, 2, 12), userId = 123, courseCode = '2IPE0')
    uploadToDatabase(file)
    file1 = Files.query.filter_by(filename='ScrumAndXpFromTheTrenchesonline07-31.pdf').first()
    assert file1.filename =='ScrumAndXpFromTheTrenchesonline07-31.pdf'
    assert file1.path =='C:/Users/20192435/Downloads/SEP2021/WriterDesk1/backend/saved_documents/ScrumAndXpFromTheTrenchesonline07-31.pdf'
    assert file1.date == datetime(2019, 2, 12)
    assert file1.userId == 123
    assert file1.courseCode == "2IPE0"
    file2 = Files.query.all()[2]
    assert file2.filename=='ScrumAndXpFromTheTrenchesonline07-31.pdf'
    assert file2.path=='C:/Users/20192435/Downloads/SEP2021/WriterDesk1/backend/saved_documents/ScrumAndXpFromTheTrenchesonline07-31.pdf'
    assert file2.date == datetime(2019, 2, 12)
    assert file2.userId == 123
    assert file2.courseCode == "2IPE0"

def testCreateDatabase(testClient):
    db.create_all()

def testFiles(testClient, initDatabase):
    files = Files.query.all()
    assert str(files[0]) == '<File URD_Group3_vers03_Rc.pdf>'
    assert str(files[1]) == '<File SEP.pdf>'

def testRemoveDatabase(testClient, initDatabase):
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
    removeFromDatabase(file)
    assert Files.query.filter_by(filename='ScrumAndXpFromTheTrenchesonline07-31.pdf').first() == None
