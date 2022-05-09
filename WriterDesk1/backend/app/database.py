from app import db
from app import models

def uploadToDatabase(toUpload):
    db.create_all()
    db.session.add(toUpload)
    db.session.commit()

# Retrieves all files of user,
# Order on sortingAttribute
def getFilesByUser(user, sortingAttribute):
    #TODO change userId to actual column name
    files = models.Files.query.filter_by(userId=user)

    if sortingAttribute == "filename.asc":
        files = files.order_by(models.Files.filename)
    elif sortingAttribute == "filename.desc":
        files = files.order_by(models.Files.filename.desc())
    elif sortingAttribute == "course.asc":
        files = files.order_by(models.Files.course)
    elif sortingAttribute == "course.desc":
        files = files.order_by(models.Files.course.desc())
    elif sortingAttribute == "date.asc":
        files = files.order_by(models.Files.date)
    elif sortingAttribute == "date.desc":
        files = files.order_by(models.Files.date.desc())
    
    return files
