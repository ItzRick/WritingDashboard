from app import app


@app.route('/')
@app.route('/index')
def index():
    return "Hello, World!"


@app.route('/profile')
def my_profile():
    response_body = {
        "name": "Nagato",
        "about": "Hello! I'm a full stack developer that loves python and javascript"
    }

    return response_body


@app.route('/text')
def my_text():
    background = "0,1,2,3,4,12,13,14,15,16"
    text_file = open("Test text.txt", "r")
    text = text_file.read()
    text_file.close()
    response_body = {
        "text": text,
        "background": background,
    }

    return response_body
