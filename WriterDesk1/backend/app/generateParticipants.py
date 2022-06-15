from app import db
from app.models import User
from app.database import postParticipant, postParticipantToProject
import random, string

def generateParticipants(count, projectId):
    PASSWORD_LENGTH = 10

    for participant in range(count):

        # Generate password
        password = generateParticipantPassword(PASSWORD_LENGTH)

        # Post participant, raise error if this fails
        try:
            user = postParticipant("username", password)
            user.username = generateParticipantUsername(user.id)
            db.session.flush()
            postParticipantToProject(user.id, projectId)
        except Exception as e:
            db.session.rollback()
            raise e
    # No exception raised so changes can be committed
    db.session.commit()

def generateParticipantUsername(id):
    return "par_" + str(id)

def generateParticipantPassword(length):
    characters = [random.choice(string.ascii_lowercase),
                    random.choice(string.ascii_uppercase),
                    random.choice(string.digits)] + [random.choice(string.ascii_letters + string.digits) for letter in range(length-3)]
    random.shuffle(characters)
    return ''.join(characters)