from app.models import Files, User
from datetime import datetime

def testNewUser(newUser):
    '''
        Test if new user is correct and if password is hashed
        Arguments:
            newUser: the user of which the parameters should be checked 
    '''
    assert newUser.type == "user"
    assert newUser.username == "m.l.langedijk@student.tue.nl"
    assert newUser.passwordHash != "wachtwoord"

def testNewFile(newFile):
    '''
        Test if the file as created in the setup is indeed correct.
        Arguments:
            newFile: the file of which the parameters should be checked.
    '''
    assert newFile.filename =='URD_Group3_vers03_Rc.pdf'
    assert newFile.path =='C:/Users/20192435/Downloads/SEP2021/WriterDesk1/backend/saved_documents/URD_Group3_vers03_Rc.pdf'
    assert newFile.date == datetime(2018, 5, 20)
    assert newFile.userId == 256
    assert newFile.courseCode == "2ILH0"
    assert newFile.fileType == '.pdf'

def testFileId(newFile):
    '''
        Test if we can change the id of the file created in the setup to a certain value.
        Arguments: 
            newFile: file of which we can test if we can indeed change the id.
    '''
    newFile.id = 235
    assert newFile.id == 235