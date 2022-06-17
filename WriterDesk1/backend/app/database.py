from app import db
from app import models
import csv

# helper function, TODO remove before deploy
def initialSetup():
    db.session.commit()
    db.drop_all()
    db.create_all()
    # create initial user
    u = models.User(username='john', password_plaintext='password')
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

def recordsToCsv(path, records, columns=[]):
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
    with open(path, 'w', newline='') as outFile:
        # Use specified column names or names from table 
        fieldNames = [column[0] for column in records[0].items()]

        outCsv = csv.DictWriter(outFile, fieldnames=fieldNames)
        outCsv.writeheader()
        [outCsv.writerow(record) for record in records]