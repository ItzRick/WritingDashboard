from app.models import Files

def testNewFile(newFile):
    assert newFile.filename=='URD_Group3_vers03_Rc.pdf'
    assert newFile.path=='C:/Users/20192435/Downloads/SEP2021/WriterDesk1/backend/saved_documents/URD_Group3_vers03_Rc.pdf'

def testFileId(newFile):
    newFile.id = 235
    assert newFile.id == 235