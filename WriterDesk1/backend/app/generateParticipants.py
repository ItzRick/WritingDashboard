from app import db
from app.models import User
from app.database import postParticipant, postParticipantToProject
import random, string

def generateParticipants(nrOfParticipants, projectId):
    '''
        Creates participants for a research project, adding them to the User table
        and creating the corresponding entries in the ParticipantToProject table. 
        Attributes:
            PASSWORD_LENGTH: length of generated passwords
            password: generated password for a participant
            user: User object for a new participant
        Arguments:
            nrOfParticipants: the number of participants to be generated
            projectId: id of the project the participants belong to
        Return:
            Returns a dictionary with usernames and passwords of new participants.
    '''

    PASSWORD_LENGTH = 10
    data = []
    for participant in range(nrOfParticipants):

        # Generate password
        password = generateParticipantPassword(PASSWORD_LENGTH)

        # Post participant, raise error if this fails
        try:
            user = postParticipant("username", password)
            user.username = generateParticipantUsername(user.id)
            db.session.flush()
            postParticipantToProject(user.id, projectId)
            data.append({'username': user.username, 'password': password})
        except Exception as e:
            db.session.rollback()
            raise e
    # No exception raised so changes can be committed
    db.session.commit()
    return data

def generateParticipantUsername(id):
    '''
        Creates a username string using the given id.
        Arguments:
            id: the user id of the user this username is made for
        Return:
            Returns the username string
    '''

    return "par_" + str(id)

def generateParticipantPassword(length):
    '''
        Creates a random but valid password, so it contains at least 1 uppercase and lowercase character and a number
        and is at least 8 characters long.
        Attributes:
            characters: list of characters that will form the password
        Arguments:
            length: the length of the generated password
        Return:
            Returns the password string
    '''

    if length < 8:
        raise Exception('Password should be at least 8 characters long')

    characters = [random.choice(string.ascii_lowercase),
                    random.choice(string.ascii_uppercase),
                    random.choice(string.digits)] + [random.choice(string.ascii_letters + string.digits) for letter in range(length-3)]
    random.shuffle(characters)
    return ''.join(characters)