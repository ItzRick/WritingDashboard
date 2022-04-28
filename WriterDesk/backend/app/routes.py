from app import app
from flask import render_template
'''
@app.route('/')
@app.route('/index')
def index():
    return "Hello, World!"'''

@app.route('/', methods=['GET'])
def root():
    return render_template('index.html')