import io
import os
from datetime import date, datetime
from app.models import Files
from werkzeug.utils import secure_filename

def testUploadTextStream(testClient, initDatabase):
    fileName = 'fake-text-stream.txt'
    data = {
        'files': (io.BytesIO(b"some initial text data"), fileName),
        'fileName': 'fake-text-stream.txt',
        'courseCode': '2IPE0',
        'userId': 123,
        'date': date(2022, 5, 11)
    }
    response = testClient.post('/fileapi/upload', data=data)
    assert response.data == b'success'
    assert response.status_code == 200
    file = Files.query.filter_by(filename=fileName).first()
    assert file.filename == fileName
    assert os.path.isfile(file.path)
    assert file.courseCode == '2IPE0'
    assert file.userId == 123
    assert file.date == datetime(2022, 5, 11)

def testUploadTextFile(testClient, initDatabase):
    fileName = 'test.txt'
    BASEDIR = os.path.abspath(os.path.dirname(__file__))
    fileDir = os.path.join(BASEDIR, fileName)
    data = {
        'files': (open(fileDir, 'rb'), fileName),
        'fileName': 'test.txt',
        'courseCode': '2WBB0',
        'userId': 256,
        'date': date(1998, 10, 30)
    }
    response = testClient.post('/fileapi/upload', data=data)
    assert response.data == b'success'
    assert response.status_code == 200
    file = Files.query.filter_by(filename=secure_filename(fileName)).first()
    assert file.filename == secure_filename(fileName)
    assert os.path.exists(file.path)
    assert file.courseCode == '2WBB0'
    assert file.userId == 256
    assert file.date == datetime(1998, 10, 30)
    assert Files.query.filter_by(userId=256).first() == Files.query.filter_by(filename= secure_filename(fileName)).first()

def testUploadPDFFile(testClient, initDatabase):
    fileName = 'SEP intro.pdf'
    BASEDIR = os.path.abspath(os.path.dirname(__file__))
    fileDir = os.path.join(BASEDIR, fileName)
    data = {
        'files': (open(fileDir, 'rb'), fileName),
        'fileName': fileName,
        'courseCode': '1ABC2',
        'userId': 789,
        'date': date(2007, 1, 1)
    }
    response = testClient.post('/fileapi/upload', data=data)
    assert response.data == b'success'
    assert response.status_code == 200
    file = Files.query.filter_by(filename=secure_filename(fileName)).first()
    assert file.filename == secure_filename(fileName)
    assert os.path.exists(file.path)
    assert file.courseCode == '1ABC2'
    assert file.userId == 789
    assert file.date == datetime(2007, 1, 1)
    assert Files.query.filter_by(userId=789).first() == Files.query.filter_by(filename= secure_filename(fileName)).first()

def testUploadPDFFileExtra(testClient, initDatabase):
    fileName = 'Air_Pollution_Sources_Identification_Precisely_Based_on_Remotely_Sensed_Aerosol_and_Glowworm_Swarm_Optimization.pdf'
    BASEDIR = os.path.abspath(os.path.dirname(__file__))
    fileDir = os.path.join(BASEDIR, fileName)
    data = {
        'files': (open(fileDir, 'rb'), fileName),
        'fileName': fileName,
        'courseCode': '5ABCBDHEH8',
        'userId': 564527,
        'date': date(2005, 2, 27)
    }
    response = testClient.post('/fileapi/upload', data=data)
    assert response.data == b'success'
    assert response.status_code == 200
    file = Files.query.filter_by(filename=secure_filename(fileName)).first()
    assert file.filename == fileName
    assert secure_filename(fileName) == fileName
    assert os.path.exists(file.path)
    assert file.courseCode == '5ABCBDHEH8'
    assert file.userId == 564527
    assert file.date == datetime(2005, 2, 27)
    assert Files.query.filter_by(userId=564527).first() == Files.query.filter_by(filename= secure_filename(fileName)).first()

def testUploadDOCXFile(testClient, initDatabase):
    fileName = 'test.docx'
    BASEDIR = os.path.abspath(os.path.dirname(__file__))
    fileDir = os.path.join(BASEDIR, fileName)
    data = {
        'files': (open(fileDir, 'rb'), fileName),
        'fileName': fileName,
        'courseCode': '9ABCEHJDHD20',
        'userId': 78267,
        'date': date(2016, 11, 8)
    }
    response = testClient.post('/fileapi/upload', data=data)
    assert response.data == b'success'
    assert response.status_code == 200
    file = Files.query.filter_by(filename=secure_filename(fileName)).first()
    assert file.filename == fileName
    assert secure_filename(fileName) == fileName
    assert os.path.exists(file.path)
    assert file.courseCode == '9ABCEHJDHD20'
    assert file.userId == 78267
    assert file.date == datetime(2016, 11, 8)
    assert Files.query.filter_by(userId=78267).first() == Files.query.filter_by(filename= secure_filename(fileName)).first()

def testUploadDOCFile(testClient, initDatabase):
    fileName = 'test.doc'
    BASEDIR = os.path.abspath(os.path.dirname(__file__))
    fileDir = os.path.join(BASEDIR, fileName)
    data = {
        'files': (open(fileDir, 'rb'), fileName),
        'fileName': fileName,
        'courseCode': '5ABCBDHEH8',
        'userId': 564527,
        'date': date(2005, 2, 27)
    }
    response = testClient.post('/fileapi/upload', data=data)
    assert response.data == b'success'
    assert response.status_code == 200
    file = Files.query.filter_by(filename=secure_filename(fileName)).first()
    assert file.filename == fileName
    assert secure_filename(fileName) == fileName
    assert os.path.exists(file.path)
    assert file.courseCode == '5ABCBDHEH8'
    assert file.userId == 564527
    assert file.date == datetime(2005, 2, 27)
    assert Files.query.filter_by(userId=564527).first() == Files.query.filter_by(filename= secure_filename(fileName)).first()

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

