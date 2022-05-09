from config import Config
import pytest
from app import create_app, db
from app.models import Files
import os

class TestConfig(Config):
    BASEDIR = os.path.abspath(os.path.dirname(__file__))

    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.abspath(os.path.join(BASEDIR, 'app_test.db'))

@pytest.fixture(scope='module')
def newFile():
    file = Files(path='C:/Users/20192435/Downloads/SEP2021/WriterDesk1/backend/saved_documents/URD_Group3_vers03_Rc.pdf', filename='URD_Group3_vers03_Rc.pdf')
    return file


@pytest.fixture(scope='module')
def testClient():
    app = create_app(TestConfig())
    # Create a test client using the Flask application configured for testing
    with app.test_client() as testing_client:
        # Establish an application context
        with app.app_context():
            yield testing_client  # this is where the testing happens!



@pytest.fixture(scope='function')
def initDatabase(testClient):
    db.create_all()

    file1 = Files(path='C:/Users/20192435/Downloads/SEP2021/WriterDesk1/backend/saved_documents/URD_Group3_vers03_Rc.pdf', filename='URD_Group3_vers03_Rc.pdf')
    file2 = Files(path='C:/Users/20192435/Downloads/SEP2021/WriterDesk1/backend/saved_documents/SEP.pdf', filename='SEP.pdf')
    db.session.add(file1)
    db.session.add(file2)
    db.session.commit()

    yield
    
    db.drop_all()


