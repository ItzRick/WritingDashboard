from flask import request
from app import app
from app import uploadFile
from app import signUp

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
    data = request.form
    file = request.files['file']
    uploadFile.fileUpload(data, file)

    return "Success!"

@app.route('/signUpStudent', methods = ['POST'])
def signUpStudent():
    data = request.get_json()
    signUp(data)
    return "Success!"