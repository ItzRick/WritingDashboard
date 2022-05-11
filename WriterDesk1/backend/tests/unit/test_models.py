from app.models import Files
from datetime import datetime

def testNewFile(newFile):
    assert newFile.filename =='URD_Group3_vers03_Rc.pdf'
    assert newFile.path =='C:/Users/20192435/Downloads/SEP2021/WriterDesk1/backend/saved_documents/URD_Group3_vers03_Rc.pdf'
    assert newFile.date == datetime(2018, 5, 20)
    assert newFile.userId == 256
    assert newFile.courseCode == "2ILH0"

def testFileId(newFile):
    newFile.id = 235
    assert newFile.id == 235