from app import db

def uploadToDatabase(toUpload):
    db.create_all()
    db.session.add(toUpload)
    db.session.commit()