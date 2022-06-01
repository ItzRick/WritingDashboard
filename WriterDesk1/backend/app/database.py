from app import db
from app import models

def initialSetup():
    db.session.commit()
    db.drop_all()
    db.create_all()
    # create initial user
    u = models.User(id='123', username='john', email='john@example.com')
    uploadToDatabase(u)

    #don't forget to comment out ... existing files in models.py 


def uploadToDatabase(toUpload):
    
    db.session.add(toUpload)
    db.session.commit()

def removeFromDatabase(document):
    db.session.delete(document)
    db.session.commit()

# Retrieves all files of user,
# Orders on sortingAttribute
# Returns list of Files objects as dictionary
def getFilesByUser(user, sortingAttribute):
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
