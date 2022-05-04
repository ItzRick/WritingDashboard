from flask import request
from app import app
from app import uploadFile

@app.route('/')
@app.route('/index')
def index():
    return "Hello, World!"

@app.route('/profile')
def myProfile():
    response_body = {
        "name": "Nagato",
        "about" :"Hello! I'm a full stack developer that loves python and javascript"
    }

    return response_body

@app.route('/fileUpload', methods = ['POST'])
def fileUpload():
    # Retrieve the files as send by the react frontend and give this to the fileUpload function, 
    # which does all the work:
    files = request.files.getlist('files')
    uploadFile.fileUpload(files)

    return "success"
