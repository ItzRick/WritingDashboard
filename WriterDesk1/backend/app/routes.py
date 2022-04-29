from app import app

@app.route('/')
@app.route('/index')
def index():
    return "Hello, World!"

@app.route('/profile')
def my_profile():
    response_body = {
        "name": "Nagato",
        "about" :"Hello! I'm a full stack developer that loves python and javascript"
    }

    return response_body