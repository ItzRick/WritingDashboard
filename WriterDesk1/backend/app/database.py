from app import db
from app import models
from app.models import User, Scores, Files, Projects, ParticipantToProject

# helper function, TODO remove before deploy

def initialSetup():
    db.session.commit()
    db.drop_all()
    db.create_all()
    
	# create admin user
    u = User(username='admin', password_plaintext='admin')
    u.role = 'admin'
    uploadToDatabase(u)

    # comment out:
    #   - loginapi > create_token() > initialSetup()

# Upload the given file to the database of this session
def uploadToDatabase(toUpload):
    db.session.add(toUpload)
    db.session.commit()

# Remove the given file from the database of this session
def removeFromDatabase(document):
    db.session.delete(document)
    db.session.commit()

# Retrieves all files of user,
# Orders on sortingAttribute
# Returns list of Files objects as dictionary
def getFilesByUser(user, sortingAttribute):
    '''
        This function handles the query for retrieving a user's files and orders them according to the given sorting attribute.
        Attributes:
            files: result of the query, containing the files of the given user
        Arguments:
            user: id of the user whose files need to be retrieved
            sortingAttribute: attribute on which the query result should be ordered
        Return:
            Returns list of files of the given user, ordered on the given sorting attribute
    '''

    files = db.session.query(Files).filter_by(userId=user)

    if sortingAttribute == "filename.asc":
        files = files.order_by(Files.filename)
    elif sortingAttribute == "filename.desc":
        files = files.order_by(Files.filename.desc())
    elif sortingAttribute == "course.asc":
        files = files.order_by(Files.courseCode)
    elif sortingAttribute == "course.desc":
        files = files.order_by(Files.courseCode.desc())
    elif sortingAttribute == "date.asc":
        files = files.order_by(Files.date)
    elif sortingAttribute == "date.desc":
        files = files.order_by(Files.date.desc())
    return Files.serializeList(files.all())

def getUsers() :
    users = db.session.query(User).filter(User.role != 'participant').all()
    return User.serializeList(users)

# Registers new user with username and password
def postUser(username, password):
    '''
        This function handles the signup query. When there is no user present in the database with the given username,
        a new user is posted in the database with a unique id, the given username, the student role and a hash of the given password.
        Attributes:
            user: user object that is to be added to the database
        Arguments:
            username: username as given in frontend
            password: password as given in frontend
        Return:
            Returns True when a new user was added to the database and False when there already was a user with the given username
    '''

    # Check if there is already a user with this username
    if db.session.query(User).filter_by(username=username).count() > 0:
        return False

    # Add user to the database with student role
    user = User(username=username, password_plaintext=password, role="student")
    uploadToDatabase(user)
    return True


