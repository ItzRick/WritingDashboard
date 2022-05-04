from werkzeug.utils import secure_filename
from app import app
import os

def fileUpload(data, file):
    # print(data.keys())
    # Check if we have received the correct file:
    filename = secure_filename(data.get('fileName'))
    filename1 = secure_filename(file.filename)
    if (filename == filename1):
        file_location = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        print(file_location)
        file.save(file_location)
        print("hi")
