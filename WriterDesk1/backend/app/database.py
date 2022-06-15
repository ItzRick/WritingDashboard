from app import db
from app import models

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
            user: id of the user who's files need to be retrieved
            sortingAttribute: attribute on which the query result should be ordered
        Return:
            Returns list of files of the given user, ordered on the given sorting attribute
    '''

    files = db.session.query(models.Files).filter_by(userId=user)

    if sortingAttribute == "filename.asc":
        files = files.order_by(models.Files.filename)
    elif sortingAttribute == "filename.desc":
        files = files.order_by(models.Files.filename.desc())
    elif sortingAttribute == "course.asc":
        files = files.order_by(models.Files.courseCode)
    elif sortingAttribute == "course.desc":
        files = files.order_by(models.Files.courseCode.desc())
    elif sortingAttribute == "date.asc":
        files = files.order_by(models.Files.date)
    elif sortingAttribute == "date.desc":
        files = files.order_by(models.Files.date.desc())

    return models.Files.serializeList(files.all())

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
    if db.session.query(models.User).filter_by(username=username).count() > 0:
        return False

    # Add user to the database with student role
    user = models.User(username=username, password_plaintext=password, role="student")
    uploadToDatabase(user)
    return True

def postParticipant(username, password):
    '''
        This function handles the query that generates a partipant account. When there is no participant present in the database with the given username,
        a new participant is posted in the database with a unique id, the given username, the participant role and a hash of the given password.
        Attributes:
            user: user object that is to be added to the database
        Arguments:
            username: username as given in frontend
            password: password as given in frontend
        Return:
            Returns the user when a new user was added to the database
    '''

    # Check if there is already a user with this username
    if db.session.query(models.User).filter_by(username=username).count() > 0:
        raise Exception('User exists already')

    # Add user to the database with participant role
    user = models.User(username=username, password_plaintext=password, role="participant")
    db.session.add(user)
    db.session.flush()
    return user

def postParticipantToProject(userId, projectId):
    '''
        This function handles the query that creates an entry in ParticipantToProject, to link a participant to a research project. 
        Attributes:
            project: query result to check if there exists a project with the given id
            dataTuple: object that is to be added to the database
        Arguments:
            userId: id of the participant
            projectId: id of the research project
    '''
    project = models.Projects.query.filter_by(id=projectId).all()
    if len(project) == 0:
        raise Exception('Project does not exist')

    dataTuple = models.ParticipantToProject(userId=userId, projectId=projectId)
    db.session.add(dataTuple)
    db.session.flush()