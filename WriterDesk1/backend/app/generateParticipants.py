from app.models import User
from app.database import postParticipant, postParticipantToProject
import random, string

def generateParticipants(count, projectId):
    PASSWORD_LENGTH = 10

    lastParticipantNumber = None
    for participant in range(count):

        if lastParticipantNumber is None:
            lastParticipantNumber = getLastParticipantNumber()

        # Generate username and password
        username = generateParticipantUsername(lastParticipantNumber)
        password = generateParticipantPassword(PASSWORD_LENGTH)

        # Post participant, raise error if this fails
        try:
            userId = postParticipant(username, password)
        except Exception as e:
            raise e

        postParticipantToProject(userId, projectId)

        lastParticipantNumber += 1

def getLastParticipantNumber():
    return max([0, *(int(r.username[4:]) for r in User.query.filter(User.username.startswith("par_")))])

def generateParticipantUsername(lastParticipantNumber):
    return "par_" + str(lastParticipantNumber + 1)

def generateParticipantPassword(length):
    characters = [random.choice(string.ascii_lowercase),
                    random.choice(string.ascii_uppercase),
                    random.choice(string.digits)] + [random.choice(string.ascii_letters + string.digits) for letter in range(length-3)]
    random.shuffle(characters)
    return ''.join(characters)