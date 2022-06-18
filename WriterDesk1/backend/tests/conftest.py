from config import Config
import pytest
from app import create_app, db
from app.models import Files, User
import os
from datetime import datetime
import shutil
import nltk
from nltk.corpus import stopwords

class TestConfig(Config):
    '''
        Config for the test class, 
        Defines: 
            UPLOAD_FOLDER: location of the upload folder, called saved_documents. 
            SQLALCHEMY_DATABASE_URI: Location of an sqlite database called app_test.db.
    '''
    BASEDIR = os.path.abspath(os.path.dirname(__file__))

    UPLOAD_FOLDER = os.path.join(BASEDIR, "saved_documents")
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.abspath(os.path.join(BASEDIR, 'app_test.db'))

@pytest.fixture(scope='module')
def newFile():
    '''
        This is a new example file, not added to the database.
        The file has the following attributes:
            path: C:/Users/20192435/Downloads/SEP2021/WriterDesk1/backend/saved_documents/URD_Group3_vers03_Rc.pdf
            filename: URD_Group3_vers03_Rc.pdf
            date: 2018-5-20
            userId: 256
            courseCode: 2ILH0
    '''
    file = Files(path='C:/Users/20192435/Downloads/SEP2021/WriterDesk1/backend/saved_documents/URD_Group3_vers03_Rc.pdf', filename='URD_Group3_vers03_Rc.pdf', 
    date=datetime(2018, 5, 20), userId = 256, courseCode = '2ILH0', fileType=".pdf")
    return file

@pytest.fixture(scope='module')
def newUser():
    '''
        This is an example user.
        The user attributes:
            username: m.l.langedijk@student.tue.nl
            password (unhashed, will be hashed when ininitailized): wachtwoord
    '''
    user = User('m.l.langedijk@student.tue.nl', 'wachtwoord')
    return user


@pytest.fixture(scope='module')
def testClient():
    '''
        Creates a new instance of the flask application, as testing client. Firstly, the UPLOAD_Folder directory is removed including files if required
        and a new directory is created, since this is normally done in the config file of the application. Then the testing_client is created, 
        using the TestConfig configuration, and the tests are then executed. 
    '''
    # Create an app with this configuration:
    app = create_app(TestConfig())
    # Remove the test-directory with the saved files and create this folder again, which is usually done at the first run of the application:
    if os.path.isdir(app.config['UPLOAD_FOLDER']):
        shutil.rmtree(app.config['UPLOAD_FOLDER'])
    os.makedirs(app.config['UPLOAD_FOLDER'])
    # Create a test client using the Flask application configured for testing
    with app.test_client() as testing_client:
        # Establish an application context
        with app.app_context():
            yield testing_client  # this is where the testing happens!

@pytest.fixture(scope='function')
def initDatabase(testClient):
    '''
        Creates a database, with tables such as defined in the models of the application. Adds two files to this database, 
        The attributes of file 1 are:
            path: C:/Users/20192435/Downloads/SEP2021/WriterDesk1/backend/saved_documents/URD_Group3_vers03_Rc.pdf
            filename: URD_Group3_vers03_Rc.pdf
            date: 2018-5-20
            userId: 256
            courseCode: 2ILH0
        The attributes of file 2 are:
            path: C:/Users/20192435/Downloads/SEP2021/WriterDesk1/backend/saved_documents/SEP.pdf
            filename: SEP.pdf
            date: 2020-10-2
            userId: 567
            courseCode: 3NAB0
        Afterwards, the database is empties again, so no entries can influence a next test run. This is run each time
        a test case is run, so that one test case does not influence the database of another test case. 
    '''
    # Create the database:
    db.drop_all()
    db.create_all()

    # Add the 2 files:
    file1 = Files(path='C:/Users/20192435/Downloads/SEP2021/WriterDesk1/backend/saved_documents/URD_Group3_vers03_Rc.pdf', 
    filename='URD_Group3_vers03_Rc.pdf', date=datetime(2019, 2, 12), userId = 123, courseCode = '2IPE0', fileType = '.pdf')
    file2 = Files(path='C:/Users/20192435/Downloads/SEP2021/WriterDesk1/backend/saved_documents/SEP.pdf', 
    filename='SEP.pdf', date=datetime(2020, 10, 2), userId = 567, courseCode = '3NAB0', fileType = '.pdf')
    db.session.add(file1)
    db.session.add(file2)

    user1 = User("Pietje", "Bell")
    user2 = User("Donald", "Duck")
    admin = User('ad', 'min')
    db.session.add(user1)
    db.session.add(user2)
    db.session.add(admin)
    
    # change adminRole to admin
    admin.role = 'admin'

    db.session.commit()

    yield   # This is where the testing happens!
    
    # Empties the database after the application has finished testing:
    db.session.close()
    db.drop_all()
    

@pytest.fixture(scope='function')
def initDatabaseEmpty(testClient):
    '''
        Creates a database, with tables such as defined in the models of the application. Doesn't add any files to the database.
        Afterward the test case, the database is empties again, so no entries can influence a next test run. This is run each time
        a test case is run, so that one test case does not influence the database of another test case. 
    '''
    # Create the database:
    db.create_all()

    yield   # This is where the testing happens!
    
    # Empties the database after the application has finished testing:
    db.session.commit()
    db.drop_all()

@pytest.fixture(scope='module')
def englishStopwords():
    '''
        Downloads the nltk stopwords and punkt and returns englishStopwords, the english stopwords.
    '''
    nltk.download('stopwords')
    nltk.download('punkt')
    english_stopwords = stopwords.words('english')
    return english_stopwords

@pytest.fixture(scope='module')
def englishStopwords():
    '''
        Downloads the nltk stopwords and punkt and returns englishStopwords, the english stopwords.
    '''
    nltk.download('stopwords')
    nltk.download('punkt')
    english_stopwords = stopwords.words('english')
    return english_stopwords
