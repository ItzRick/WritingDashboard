from app import db
from app.models import User, Scores, Files 

# helper function, TODO remove before deploy
def initialSetup():
    db.session.commit()
    db.drop_all()
    db.create_all()
    # create initial user
    u = User(username='john', password_plaintext='password')
    uploadToDatabase(u)

    # comment out:
    #   - fileapi > fileUpload() > initialSetup()
    #   - models > Users > __init__() > self.id ...


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
