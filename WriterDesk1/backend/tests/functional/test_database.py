from app.models import Files
from app.database import uploadToDatabase
from app import db

def testValidFile(testClient, initDatabase):
    files = Files.query.all()
    file = files[0]
    assert file.filename=='URD_Group3_vers03_Rc.pdf'
    assert file.path=='C:/Users/20192435/Downloads/SEP2021/WriterDesk1/backend/saved_documents/URD_Group3_vers03_Rc.pdf'
    file = files[1]
    assert file.filename=='SEP.pdf'
    assert file.path=='C:/Users/20192435/Downloads/SEP2021/WriterDesk1/backend/saved_documents/SEP.pdf'

def testUploadToDatabase(testClient, initDatabase):
    db.create_all()
    file = Files(path='C:/Users/20192435/Downloads/SEP2021/WriterDesk1/backend/saved_documents/ScrumAndXpFromTheTrenchesonline07-31.pdf', filename='ScrumAndXpFromTheTrenchesonline07-31.pdf')
    db.session.add(file)
    db.session.commit()
    file = Files.query.filter_by(filename='ScrumAndXpFromTheTrenchesonline07-31.pdf').first()
    assert file.filename=='ScrumAndXpFromTheTrenchesonline07-31.pdf'
    assert file.path=='C:/Users/20192435/Downloads/SEP2021/WriterDesk1/backend/saved_documents/ScrumAndXpFromTheTrenchesonline07-31.pdf'
    file = Files.query.all()[2]
    assert file.filename=='ScrumAndXpFromTheTrenchesonline07-31.pdf'
    assert file.path=='C:/Users/20192435/Downloads/SEP2021/WriterDesk1/backend/saved_documents/ScrumAndXpFromTheTrenchesonline07-31.pdf'

def testCreateDatabase(testClient):
    db.create_all()

def testFiles(testClient, initDatabase):
    files = Files.query.all()
    assert str(files[0]) == '<File URD_Group3_vers03_Rc.pdf>'
    assert str(files[1]) == '<File SEP.pdf>'