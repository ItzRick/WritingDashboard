from app import db
from app.models import User, Scores, Files, Projects, ParticipantToProject
import csv, os

# helper function, TODO remove before deploy

def initialSetup():
    db.session.close()
    db.drop_all()
    db.create_all()
    # create admin user
    u = User.query.filter_by(username='admin').first()
    if u is None:
        u = User(username='admin', password_plaintext='admin')
    u.role = 'admin'
    uploadToDatabase(u)

    # comment out:
    #   - loginapi > create_token() > initialSetup()

# Upload the given file to the database of this session
def uploadToDatabase(toUpload):
    '''
        This functions adds data to the database.
        Arguments:
            toUpload: the data to upload to the database.
    '''
    # add the data to the database
    db.session.add(toUpload)
    # commit the changes in the database
    db.session.commit()

def removeFromDatabase(toRemove):
    '''
        This functions removes data from the database.
        Arguments:
            toRemove: the data to be removed from the database.
    '''
    # remove the data from the database
    db.session.delete(toRemove)
    # commit the changes in the database
    db.session.commit()

def getFilesByUser(user, sortingAttribute):
    '''
        This function handles the query for retrieving a user's files and sorts 
        them according to the given sorting attribute. The function then returns
        a sorted list of Files objects as a dictionary.
        Attributes:
            files: result of the query, containing the files of the given user.
        Arguments:
            user: id of the user who's files need to be retrieved.
            sortingAttribute: attribute on which the query result is ordered.
        Return:
            Returns list of files of the user, ordered on the sorting attribute.
    '''

    files = db.session.query(Files).filter_by(userId=user)

    # sort files by ascending filename
    if sortingAttribute == "filename.asc":
        files = files.order_by(Files.filename)
    # sort files by descending filename
    elif sortingAttribute == "filename.desc":
        files = files.order_by(Files.filename.desc())
    # sort files by ascending course name
    elif sortingAttribute == "course.asc":
        files = files.order_by(Files.courseCode)
    # sort files by descending course name
    elif sortingAttribute == "course.desc":
        files = files.order_by(Files.courseCode.desc())
    # sort files by ascending date
    elif sortingAttribute == "date.asc":
        files = files.order_by(Files.date)
    # sort files by descending date
    elif sortingAttribute == "date.desc":
        files = files.order_by(Files.date.desc())
    return Files.serializeList(files.all())

def getUsers() :
    users = db.session.query(User).filter(User.role != 'participant').all()
    return User.serializeList(users)

# Registers new user with username and password
def postUser(username, password, trackable=True):
    '''
        This function handles the signup query. When there is no user present in
        the database with the given username, a new user is posted in the 
        database with a unique id, the given username, the student role and a 
        hash of the given password.
        Attributes:
            user: user object that is to be added to the database.
        Arguments:
            username: username as given in frontend.
            password: password as given in frontend.
            trackable: whether the user wants to be tracked or not.
        Return:
            True: when a new user was added to the database.
            False: when there already was a user with the given username.
    '''

    # Check if there is already a user with this username
    if db.session.query(User).filter_by(username=username).count() > 0:
        return False

    # Add user to the database with student role
    user = User(username=username, password_plaintext=password, role="student", 
        trackable=trackable)
    uploadToDatabase(user)
    return True

def recordsToCsv(path, records):
    '''
        Writes data from records into a csv at path.
        Attributes:
            outFile: file at path to write data to
            outCsv: csv file to put the data in
            fieldNames: list of names of the columns of the csv file
        Arguments:
            path: path of the created csv file
            records: data in dictionary form that is put into the csv file
    '''
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w+', newline='') as outFile:
        # Get column names from data
        fieldNames = [column[0] for column in records[0].items()]

        # Give csv file the same header names as the columns of the records
        outCsv = csv.DictWriter(outFile, fieldnames=fieldNames)
        outCsv.writeheader()
        # Write every record in records to outCsv as a new row
        for record in records:
            outCsv.writerow(record)

def postParticipant(username, password):
    '''
        This function handles the query that generates a partipant account. When
        there is no participant present in the database with the given username,
        a new participant is posted in the database with a unique id, the given 
        username, the participant role and a hash of the given password.
        Attributes:
            user: user object that is to be added to the database.
        Arguments:
            username: username as given in frontend.
            password: password as given in frontend.
        Return:
            user: when a new user was added to the database. 
            Exception: When there was already a user with the given username.
    '''
    # Check if there is already a user with this username
    if User.query.filter_by(username=username).count() > 0:
        raise Exception('User exists already')

    # Add user to the database with participant role
    user = User(username=username, password_plaintext=password,
        role="participant")
    db.session.add(user)
    db.session.flush()
    return user

def postParticipantToProject(userId, projectId):
    '''
        This function handles the query that creates an entry in 
        ParticipantToProject, to link a participant to a research project. When 
        the project with projectId does not exist in the database, the function 
        raises an exception.
        Attributes:
            project: query result to check if there exists a project with the 
            given id.
            dataTuple: object that is to be added to the database.
        Arguments:
            userId: id of the participant.
            projectId: id of the research project.
    '''
    project = Projects.query.filter_by(id=projectId).all()
    if len(project) == 0:
        # Project does not exist in the database
        raise Exception('Project does not exist')

    dataTuple = ParticipantToProject(userId=userId, projectId=projectId)
    db.session.add(dataTuple)
    db.session.flush()

def getProjectsByResearcher(user):
    '''
        This function handles the query for retrieving a user's projects.
        Attributes:
            projectIds: List of project ids of the given user.
        Arguments:
            user: id of the user whose projects need to be retrieved
        Return:
            projectIds: List of project ids of the given user.
    '''
    # Retrieve the projects of the user
    projectList = Projects.query.filter_by(userId=user).all()
    projects = [dict(userId = proj.userId, projectName = proj.projectName, id = proj.id) for proj in projectList]
    return projects 

def getParticipantsByResearcher(user):
    '''
        This function handles the query for retrieving a user's participants.
        Attributes:
            userList: a query that gets the user information
            projectList: a query that gets the projects of the user
            participantIdList: a query that gets the participant ids of the projects of the user
            participantList: retrieve the list of participants
            participants: result of the query, containing the participants of the given user
        Arguments:
            user: id of the user whose participants need to be retrieved
        Return:
            Returns list of participants of the given user
    '''
    # Get the query that gets the user information
    userList = User.query.filter_by(id=user).subquery()
    # Get the query that gets the projects of the user
    projectList = Projects.query.join(userList, Projects.userId == userList.c.id).subquery()
    # Get the query that gets the participant ids of the projects of the user
    participantIdList = ParticipantToProject.query.join(projectList, ParticipantToProject.projectId == projectList.c.id).subquery()
    # Get the participants of the projects of the user
    participantList = User.query.join(participantIdList, User.id == participantIdList.c.userId).all()
    participants = [dict(role = part.role, id = part.id, username = part.username, passwordHash = part.passwordHash) for part in participantList]
    # Return the information of the participants in all projects of the user
    return participants
    
def getParticipantsWithProjectsByResearcher(user):
    '''
        This function handles the query for retrieving a user's participants, including the projects they correspond to.
        Attributes:
            projectParticipantConnection: the connection between the participant and the project
            projectid: the id of the project that the participant is in
            project: the project that the participant is in
            projectname: the name of the project that the participant is in
            participants: result of the query, containing the participants of the given user
        Arguments:
            user: id of the user whose participants need to be retrieved
        Return:
            Returns list of participants of the given user including the projects they correspond to
    '''
    participants = getParticipantsByResearcher(user)
    
    for participant in participants:
        projectParticipantConnection = ParticipantToProject.query.filter_by(userId=participant['id']).all()
        projectid = projectParticipantConnection[0].projectId
        project = Projects.query.filter_by(id=projectid).all()
        projectname = project[0].projectName
        participant['projectid'] = projectid
        participant['projectname'] = projectname

    # Return the information of the participants in all projects of the user
    return participants
