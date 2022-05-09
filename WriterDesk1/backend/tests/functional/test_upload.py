import io
import os

def test_upload_text_stream(testClient, initDatabase):
    fileName = 'fake-text-stream.txt'
    data = {
        'files': (io.BytesIO(b"some initial text data"), fileName)
    }
    response = testClient.post('/fileapi/upload', data=data)
    assert response.data == b'success'
    assert response.status_code == 200

def test_upload_text_file(testClient, initDatabase):
    BASEDIR = os.path.abspath(os.path.dirname(__file__))
    fileDir = os.path.join(BASEDIR, 'test.txt')
    data = {
        'files': (open(fileDir, 'rb'), fileDir)
    }
    response = testClient.post('/fileapi/upload', data=data)
    assert response.data == b'success'
    assert response.status_code == 200

def test_upload_text_file_1(testClient, initDatabase):
    BASEDIR = os.path.abspath(os.path.dirname(__file__))
    fileDir = os.path.join(BASEDIR, 'SEP202122Q4.xlsx')
    data = {
        'files': (open(fileDir, 'rb'), fileDir)
    }
    response = testClient.post('/fileapi/upload', data=data)
    assert response.status_code == 400
