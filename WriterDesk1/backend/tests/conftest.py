import pytest
from config import Config
import pytest 
from app import app, db
from app.models import User, Student, Participant
import os #? nodig?

class TestConfig(Config):
    '''
        Config for the test class, 
        Defines: 
            SQLALCHEMY_DATABASE_URI: Location of an sqlite database called app_test.db.
    '''
    BASEDIR = os.path.abspath(os.path.dirname(__file__))

    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.abspath(os.path.join(BASEDIR, 'app_test.db'))

    @pytest.fixture(scope='module')
    def testClient():
        yield

    @pytest.fixture(scope='function')
    def initDatabase(testClient):
        yield