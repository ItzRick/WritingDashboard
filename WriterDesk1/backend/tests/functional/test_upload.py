import io
import os
from datetime import date, datetime
from app.models import Files
from werkzeug.utils import secure_filename
import shutil

def generalTestStuff(testClient, fileName, userId, courseCode, date1):
    BASEDIR = os.path.abspath(os.path.dirname(__file__))
    fileDir = os.path.join(BASEDIR, fileName)
    data = {
        'files': (open(fileDir, 'rb'), fileName),
        'fileName': fileName,
        'courseCode': courseCode,
        'userId': userId,
        'date': date1
    }
    response = testClient.post('/fileapi/upload', data=data)
    assert response.data == b'success'
    assert response.status_code == 200
    file = Files.query.filter_by(filename=secure_filename(fileName)).first()
    assert file.filename == secure_filename(fileName)
    assert os.path.exists(file.path)
    assert file.courseCode == courseCode
    assert file.userId == userId
    assert file.date == datetime.combine(date1, datetime.min.time())
    assert Files.query.filter_by(filename= secure_filename(fileName)).first() in Files.query.filter_by(userId=userId).all()

def testUploadTextStream(testClient, initDatabase):
    fileName = 'fake-text-stream.txt'
    userId = 123
    courseCode = '2IPE0'
    date1 = date(2022, 5, 11)
    data = {
        'files': (io.BytesIO(b"some initial text data"), fileName),
        'fileName': 'fake-text-stream.txt',
        'courseCode': courseCode,
        'userId': userId,
        'date': date1
    }
    response = testClient.post('/fileapi/upload', data=data)
    assert response.data == b'success'
    assert response.status_code == 200
    file = Files.query.filter_by(filename=fileName).first()
    assert file.filename == fileName
    assert os.path.isfile(file.path)
    assert file.courseCode == courseCode
    assert file.userId == userId
    assert file.date == datetime.combine(date1, datetime.min.time())
    assert Files.query.filter_by(filename= secure_filename(fileName)).first() in Files.query.filter_by(userId=userId).all()

def testUploadTxtMultile(testClient, initDatabase):
    fileName = 'test.txt'
    userId = 256
    courseCode = '2WBB0'
    date1 = date(1998, 10, 30)
    generalTestStuff(testClient, fileName, userId, courseCode, date1)
    fileName = 'test1.txt'
    userId = 256
    courseCode = '2WBB0'
    date1 = date(2008, 10, 30)
    generalTestStuff(testClient, fileName, userId, courseCode, date1)
    
def testUploadTxtAgain(testClient, initDatabase):
    fileName = 'test.txt'
    userId = 256
    courseCode = '2WBB0'
    date1 = date(1998, 10, 30)
    generalTestStuff(testClient, fileName, userId, courseCode, date1)
    date2 = date(2000, 10, 30)
    generalTestStuff(testClient, fileName, userId, courseCode, date2)

def testUploadTextFile(testClient, initDatabase):
    fileName = 'test.txt'
    userId = 256
    courseCode = '2WBB0'
    date1 = date(1998, 10, 30)
    generalTestStuff(testClient, fileName, userId, courseCode, date1)
  

def testUploadPDFFile(testClient, initDatabase):
    fileName = 'SEP intro.pdf'
    userId = 789
    courseCode = '1ABC2'
    date1 = date(2007, 1, 1)
    generalTestStuff(testClient, fileName, userId, courseCode, date1)

def testUploadPDFFileExtra(testClient, initDatabase):
    fileName = 'Air_Pollution_Sources_Identification_Precisely_Based_on_Remotely_Sensed_Aerosol_and_Glowworm_Swarm_Optimization.pdf'
    userId = 564527
    courseCode = '5ABCBDHEH8'
    date1 = date(2005, 2, 27)
    generalTestStuff(testClient, fileName, userId, courseCode, date1)

def testUploadPDFMultiple(testClient, initDatabase):
    fileName = 'SEP intro.pdf'
    userId = 789
    courseCode = '1ABC2'
    date1 = date(2007, 1, 1)
    generalTestStuff(testClient, fileName, userId, courseCode, date1)
    fileName = 'SEP_1.pdf'
    userId = 789
    courseCode = '1ABC2'
    date1 = date(2008, 2, 1)
    generalTestStuff(testClient, fileName, userId, courseCode, date1)

def testUploadPDFAgain(testClient, initDatabase):
    fileName = 'SEP intro.pdf'
    userId = 789
    courseCode = '1ABC2'
    date1 = date(2007, 1, 1)
    generalTestStuff(testClient, fileName, userId, courseCode, date1)
    date2 = date(2008, 2, 1)
    generalTestStuff(testClient, fileName, userId, courseCode, date2)

def testUploadDOCXFile(testClient, initDatabase):
    fileName = 'test.docx'
    userId = 78267
    courseCode = '9ABCEHJDHD20'
    date1 = date(2016, 11, 8)
    generalTestStuff(testClient, fileName, userId, courseCode, date1)

def testUploadDOCXFileMultiple(testClient, initDatabase):
    fileName = 'test.docx'
    userId = 78267
    courseCode = '9ABCEHJDHD20'
    date1 = date(2016, 11, 8)
    generalTestStuff(testClient, fileName, userId, courseCode, date1)
    fileName = 'test_1.docx'
    userId = 78267
    courseCode = '9ABCEHJDHD20'
    date1 = date(2018, 11, 8)
    generalTestStuff(testClient, fileName, userId, courseCode, date1)

def testUploadDOCXFileAgain(testClient, initDatabase):
    fileName = 'test.docx'
    userId = 78267
    courseCode = '9ABCEHJDHD20'
    date1 = date(2016, 11, 8)
    generalTestStuff(testClient, fileName, userId, courseCode, date1)
    date2 = date(2018, 11, 8)
    generalTestStuff(testClient, fileName, userId, courseCode, date2)

def testUploadDOCFile(testClient, initDatabase):
    fileName = 'test.doc'
    userId = 12345
    courseCode = '3ASE0'
    date1 = date(2009, 12, 27)
    generalTestStuff(testClient, fileName, userId, courseCode, date1)

def testUploadDOCFileMultiple(testClient, initDatabase):
    fileName = 'test.doc'
    userId = 12345
    courseCode = '3ASE0'
    date1 = date(2009, 12, 27)
    generalTestStuff(testClient, fileName, userId, courseCode, date1)
    fileName = 'test_1.doc'
    userId = 12345
    courseCode = '3ASE0'
    date1 = date(2018, 3, 27)
    generalTestStuff(testClient, fileName, userId, courseCode, date1)

def testUploadDOCFileAgain(testClient, initDatabase):
    fileName = 'test.doc'
    userId = 12345
    courseCode = '3ASE0'
    date1 = date(2009, 12, 27)
    generalTestStuff(testClient, fileName, userId, courseCode, date1)
    date2 = date(2018, 3, 27)
    generalTestStuff(testClient, fileName, userId, courseCode, date2)

def testDirsCreated(testClient, initDatabase):
    fileName = 'test.txt'
    userId = 578900
    courseCode = '2WBB0'
    date1 = date(1998, 10, 30)
    data = {
        'files': (io.BytesIO(b"some initial text data"), fileName),
        'fileName': fileName,
        'courseCode': courseCode,
        'userId': userId,
        'date': date1
    }
    assert not os.path.isdir(os.path.join(testClient.application.config['UPLOAD_FOLDER'], str(userId)))
    response = testClient.post('/fileapi/upload', data=data)
    assert response.data == b'success'
    assert response.status_code == 200
    assert os.path.isdir(testClient.application.config['UPLOAD_FOLDER'])
    assert os.path.isdir((os.path.join(testClient.application.config['UPLOAD_FOLDER'], str(userId))))

def testUploadTextFileIncorrect(testClient, initDatabase):
    BASEDIR = os.path.abspath(os.path.dirname(__file__))
    fileDir = os.path.join(BASEDIR, 'SEP202122Q4.xlsx')
    data = {
        'files': (open(fileDir, 'rb'), fileDir)
    }
    response = testClient.post('/fileapi/upload', data=data)
    assert response.data == b'Incorrect filetype 1'
    assert response.status_code == 400

def testUploadTextFileNoFile(testClient, initDatabase):
    data = {
        'files': '',
    }
    response = testClient.post('/fileapi/upload', data=data)
    assert response.data == b'No file uploaded'
    assert response.status_code == 400

